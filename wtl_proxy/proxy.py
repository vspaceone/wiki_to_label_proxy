from labelprinter import print_label
from aiohttp import web

async def get_root(request):
	return web.Response(text="<html><head><title>Wiki-to-Label</title></head><body><form method='POST' action='/print'><label for='title'>Title</label>: <input name='title'><br><label for='url'>Wiki-URL</label>: <input name='url' type='url'><br><input type='submit'></form></body></html>", content_type="text/html")
async def get_ident(request):
	return web.Response(text="Wiki-to-Label")
async def post_print(request):
	await data=request.post()
	if "name" not in data or "url" not in data:
		return web.Response(status=400, text="missing field(s)")
	try:
		print_label(name=data["name"], url=data["url"])
	except Exception as e:
		return web.Response(status=500, text=e)
	return web.Response(text="OK")


wtl_proxy_app = web.Application()
wtl_proxy_app.add_routes([web.get('/', get_root), web.get("/ident", get_ident), web.post('/print', post_print)])

def start_proxy():
	web.run_app(wtl_proxy)
