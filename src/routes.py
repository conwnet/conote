
import models
from coroweb import get, post

@get('/')
async def index(request, params):
    return '{"god": "guoqing"}'

@post('/edit')
async def edit_post(request, params):
    print('sfdsf')
    return params

@get('/edit/{id}')
async def edit_get(request, params):
    return {'name': 'guoqing', 'age': 20}

@post('/user/add')
async def user_add(request, params):
    user = models.User()
    user.username = params['username']
    user.password = params['password']
    user.email = params['email']
    result = await user.save()
    return {"error": None if result else 'ERROR'}

@get('/user')
async def user_add(request, params):
    users = {}
    for user in await models.User.findAll():
        users[user.id] = {"username": user.username, "password": user.password, "email": user.email}
    return users


