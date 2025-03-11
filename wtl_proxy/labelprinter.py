import logging
logger = logging.getLogger(__name__)

import socket
from os import environ
from io import StringIO
from asyncio import Lock

async def send_printjob(job):
	logger.debug("Sending printjob...")
	ip = environ.get('CAB_HOST')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((ip,9100))
		sock.sendall(job.encode('utf-8'))
		logger.debug("Sent printjob.")
		return True

def make_printjob(title,url):
	#check for invalid characters
	for badchar in ["\n","\r",";"]:
		if badchar in title or badchar in url:
			logger.warning("possible injection attempt")
			raise ValueError("invalid characters")
	#read template
	with open(environ.get('CAB_TEMPLATE'), "r") as tf:
		job=tf.read()
	#fill in URL
	job=job.replace("%URL%",url)
	#figure out what char to split by
	splitchar=" "#default
	splitchar_list=(" ", ":", "_", "-") #leftmost has highest priority
	for c in splitchar_list:
		if c in title:
			splitchar=c
			break
	title_parts=title.split(splitchar)#split title into lines
	for n in range(4): #fill in the (up to) 4 lines
		line=""
		if n<len(title_parts):
			line=title_parts[n]
		job=job.replace(f"%TITLE{n+1}%",line)
	logger.debug("Generated Printjob:\n" + job)
	return job
