import logging
logger = logging.getLogger(__name__)

from ftplib import FTP
from os import environ
from io import StringIO
from asyncio import Lock

ftp_lock = Lock()
async def send_printjob(job):
	logger.debug("Waiting for lock release...")
	async with ftp_lock:
		logger.debug("Sending printjob...")
		fp = StringIO(job)
		ip = environ.get('CAB_HOST')
		user = environ.get('CAB_USER')
		pin = environ.get('CAB_PIN')
		ftp = FTP(ip)
		ftp.login(user, pin, "")
		ftp.cwd("execute")
		ftp.storbinary("STOR job.txt", fp)
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
