import logging
import sys
logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
import proxy as wtl
wtl.start_proxy()
logging.shutdown()
