import logging
logger = logging.getLogger(__name__)

#check if valid env
from os import environ
for ev in ["CAB_HOST","CAB_TEMPLATE"]:
    if environ.get(ev) == None:
        logger.error("Missing %s in environment!", ev)
        quit()
#check if template readable
from wtl_proxy.labelprinter import get_template_text_params
try:
    with open(environ.get("CAB_TEMPLATE")) as fp:
        templ=fp.read()
        param=get_template_text_params(templ)
        for p in ("CHAR_LINES","CHAR_MAX"):
            if p not in param:
                logger.error("Template missing param " + p)
                quit()
except IOError:
    logger.error("Template unreadable")
    quit()

#run proxy
import wtl_proxy.proxy as wtl
wtl.start_proxy()
logging.shutdown()
