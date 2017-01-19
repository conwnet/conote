import asyncio, inspect, functools

def get(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    async def __call__(self, request):
        if request.method == 'POST' and request.content_type.lower().startswith('application/json'):
            try:
                params = await request.json()
                return await self._func(request, params)
            except:
                raise
                pass
        elif request.method == 'GET':
            params = {}
            for k, v in request.match_info.items():
                params[k] = v
            return await self._func(request, params)
        return ''


def add_routes(app, module_name):
    n = module_name.rfind('.')
    if n == (-1):
        mod = __import__(module_name, globals(), locals())
    else:
        name = module_name[n + 1:]
        mod = getattr(__import__(module_name[:n], globals(), locals(), [name]), name)
    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
                    fn = asyncio.coroutine(fn)
                app.router.add_route(method, path, RequestHandler(app, fn))
