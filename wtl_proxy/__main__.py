import logging
logger = logging.getLogger(__name__)

#check if valid env
from os import environ
for ev in ["CAB_HOST","CAB_USER","CAB_PIN","CAB_TEMPLATE"]:
    if environ.get(ev) == None:
        logger.error("Missing %s in environment!", ev)
        quit()
#check if template readable
try:
    with open(environ.get("CAB_TEMPLATE")) as fp:
        fp.read()
except IOError:
    logger.error("Template unreadable")
    quit()

#run proxy
wtl.start_proxy()
logging.shutdown()
