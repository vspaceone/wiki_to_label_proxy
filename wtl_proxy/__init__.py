import logging
import sys
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
import wtl_proxy.proxy as wtl
