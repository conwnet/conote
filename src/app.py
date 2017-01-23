import asyncio
from aiohttp import web
from coroweb import add_routes
import orm, json, config, base64
from cryptography import fernet
from aiohttp_session import setup, cookie_storage, session_middleware


async def response_format(app, handler):
    async def response(request):
        r = await handler(request)
        if isinstance(r, dict):
            resp = web.Response(body=json.dumps(r).encode())
        else:
            resp = web.Response(body=str(r).encode())
        resp.content_type = 'application/json'
        for key in config.headers:
            resp.headers[key] = ', '.join(config.headers[key])
        return resp
    return response

async def init(loop):
    await orm.create_pool(loop, **config.db)
    app = web.Application(loop=loop)
    fernet_key = fernet.Fernet.generate_key()
    secret_key = base64.urlsafe_b64decode(fernet_key)
    setup(app, cookie_storage.EncryptedCookieStorage(secret_key))
    app.middlewares.append(response_format)
    add_routes(app, 'routes')
    srv = await loop.create_server(app.make_handler(), config.server['host'], config.server['port'])
    return srv

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()

if __name__ == '__main__':
    main()
