import logging
logger = logging.getLogger(__name__)

import wtl_proxy.labelprinter as lp
from aiohttp import web
from os import environ
from html import escape as html_escape

async def get_root(request):
	logger.debug("root page")
	title=html_escape(request.query.get("title",""))
	url=html_escape(request.query.get("url",""))
    
	return web.Response(text=f"<html><head><title>Wiki-to-Label</title></head><body><form method='POST' action='/print'><label for='title'>Title</label>: <input name='title' value='{title}'><br><label for='url'>Wiki-URL</label>: <input name='url' type='url' value='{url}'><br><input type='submit'></form></body></html>", content_type="text/html")
async def get_ident(request):
	logger.debug("ident")
	return web.Response(text="Wiki-to-Label")
async def post_print(request):
	data = await request.post()
	logger.debug("Incoming print request: " + str(data))
	if "title" not in data or "url" not in data:
		logger.info("missing fields")
		return web.Response(status=400, text="missing field(s)")
	try:
		job = lp.make_printjob(title=data["title"], url=data["url"])
	except Exception as e:
		logger.error(e)
		return web.Response(status=500, text="error in making printjob")
	try:
		await lp.send_printjob(job)
	except Exception as e:
		logger.error(e)
		return web.Response(status=500, text="error in sending print")
	return web.Response(text="OK")


wtl_proxy_app = web.Application()
wtl_proxy_app.add_routes([web.get('/', get_root), web.get("/ident", get_ident), web.post('/print', post_print)])

def start_proxy():
	logger.info("Starting proxy...")
	web.run_app(wtl_proxy_app, port=int(environ.get('PROXY_PORT',8985)))
