import logging
logger = logging.getLogger(__name__)

import socket
from os import environ
from io import StringIO
from asyncio import Lock
import math

def send_printjob(job):
	logger.debug("Sending printjob...")
	ip = environ.get('CAB_HOST')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.settimeout(3)
		sock.connect((ip,9100))
		sock.sendall(job.encode('utf-8'))
		logger.debug("Sent printjob.")
		return True

def get_template_text_params(template):
	extracted_params=dict()
	valid_params=("CHAR_LINES","CHAR_MAX")
	template=template.split("\n")
	for raw_line in template: #check each line
		line=raw_line.upper().strip()
		for param in valid_params: #check each param
			if line.startswith("; "+param) or line.startswith(";"+param): #if line is comment with param
				startpos=line.index("=")+1 #find end of param name
				value_str=line[startpos:].strip() #cut off part before parameter, remove whitespace
				value=int(value_str) #convert string to int
				extracted_params[param]=value #add to dict
				break #line can't have multiple params, don't bother looking'
	return extracted_params

def string_to_lines(string_parts,max_char,max_lines):
	"""splits list of strings into smaller pieces while trying to meet the specified criteria"""
	logger.debug("splitting %s",str(string_parts))
	#figure out what char to split by
	splitchar=None
	splitchar_list=(" ", ":", "_", "-") #leftmost has highest priority
	raw_string="".join(string_parts)#join parts together for easier searching
	for c in splitchar_list:
		if c in raw_string:
			splitchar=c
			break
	logger.debug("splitchar: '%s'",str(splitchar))
	if splitchar == None: #if unsplittable by splitchar
		return string_parts #give up, TODO: implement splitting mid-word
	else: #split by splitchar
		new_string_parts=list()
		for part in string_parts:
			if len(part)>max_char: #if part to long
				idx=part.rfind(splitchar,0,max_char) #find last possible split location
				if idx<0: #check rest of string
					idx=part.find(splitchar)
				logger.debug("split idx: %d",idx)
				if idx>=0:#if split location found, add split parts to new part list
					new_string_parts.append(part[:idx])
					new_string_parts.append(part[idx+1:])
				else: #not splittable by this char, leave untouched
					new_string_parts.append(part)
			else:
				new_string_parts.append(part) #no need to split
		#check if split far enough
		for part in new_string_parts:
			if len(part)>max_char: #if a line is still too long
				return string_to_lines(new_string_parts,max_char,max_lines) #split again
		return new_string_parts #if all lines short enough, finished

def make_printjob(title,url):
	#check for invalid characters
	for badchar in ["\n","\r",";"]:
		if badchar in title or badchar in url:
			logger.warning("possible injection attempt")
			raise ValueError("invalid characters")
	#read template
	with open(environ.get('CAB_TEMPLATE'), "r") as tf:
		job=tf.read()
	params=get_template_text_params(job)
	n_lines=params.get("CHAR_LINES",1)
	max_char=params.get("CHAR_MAX",10)
	logger.debug(params)
	#fill in URL
	job=job.replace("%URL%",url)
	#fill in title
	title_parts=string_to_lines([title],max_char,n_lines)
	for n in range(n_lines): #fill in the (up to) n lines
		line=""
		if n<len(title_parts):
			part=title_parts[n]
			padding=math.floor((max_char-len(part))/2) #calculate padding for centering
			line=" "*padding + part #center text
		job=job.replace(f"%TITLE{n+1}%",line)
	logger.debug("Generated Printjob:\n" + job)
	return job
