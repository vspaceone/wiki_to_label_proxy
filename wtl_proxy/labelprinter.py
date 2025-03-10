from ftplib import FTP
import os
from io import StringIO

def send_printfile(fp):
	ip = os.environ.get('CAB_HOST')
	user = os.environ.get('CAB_USER')
	pin = os.environ.get('CAB_PIN')
	ftp = FTP(ip)
	ftp.login(user, pin, "")
	ftp.cwd("execute")
	ftp.storbinary("STOR job.txt", fp)

def print_label(name,url):
	with open(os.environ.get('CAB_TEMPLATE'), "r") as tf:
		templ=tf.read()
	templ.replace("%NAME%",name)
	templ.replace("%URL%",url)
	buffer = StringIO(templ)
	send_printfile(buffer)
