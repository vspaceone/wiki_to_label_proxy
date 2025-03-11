import logging
logger = logging.getLogger(__name__)

import socket
from os import environ
from io import StringIO
from asyncio import Lock

async def send_printjob(job):
	logger.debug("Waiting for lock release...")

	logger.debug("Sending printjob...")
	ip = environ.get('CAB_HOST')
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
		sock.connect((ip,9100))
		sock.sendall(job.encode('utf-8'))
		logger.debug("Sent printjob.")
		return True

def make_printjob(title,url):
	for badchar in ["\n","\r",";"]:
		if badchar in title or badchar in url:
			logger.warning("possible injection attempt")
			raise ValueError("invalid characters")
	with open(environ.get('CAB_TEMPLATE'), "r") as tf:
		templ=tf.read()
	job=templ.replace("%TITLE%",title).replace("%URL%",url)
	logger.debug("Generated Printjob:\n" + job)
	return job
