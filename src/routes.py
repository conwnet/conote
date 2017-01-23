
import models
from coroweb import get, post
from aiohttp_session import get_session
from coverify import verity, check

@get('/')
async def index(request, params):
    session = await get_session(request)
    id = session.get('id')
    username = session.get('username')
    power = session.get('power')
    return { 'id': id, 'username': username, 'power': power }

@post('/login')
async def login(request, params):
    session = await get_session(request)
    username = params.get('username')
    password = params.get('password')
    verify_code = params.get('verify_code')
    if not check(session, verify_code):
        return { 'error': 'Bad verify_code!'}
    user = await models.User.fetchone(where=("`username`='%s'" % username))
    if user and user.get('password') == password:
        session['id'] = user.id
        session['username'] = user.username
        session['power'] = user.power
        return { 'error': None }
    return { 'error': 'Bad password' }

@get('/user/id/{id}')
async def get_user_by_id(request, params):
    session = await get_session(request)
    id = params.get('id')
    user = await models.User.fetchone(where=("`id`='%s'" % id))
    if user:
        if session.get('power') == user.power or session.get('power') == 0:
            return {'error': None, 'user': {'id': user.id, 'username': user.username}}
        return {'error': 'Permission denied'}
    return { 'error': 'Not found'}

@get('/user/username/{username}')
async def get_user_by_username(request, params):
    session = await get_session(request)
    username = params.get('username')
    user = await models.User.fetchone(where=("`username`='%s'" % username))
    if user:
        if session.get('power') == user.power or session.get('power') == 0:
            return {'error': None, 'user': { 'id': user.id, 'username': user.username } }
        return {'error': 'Permission denied'}
    return { 'error': 'Not found'}

@get('/user')
async def get_users(request, params):
    session = await get_session(request)
    if session.get('power') != 0:
        return { 'error': 'Permission denied' }
    users = {}
    for user in await models.User.fetchall():
        users[user.id] = {'username': user.username, 'password': user.password, "email": user.email}
    return {'error': None, 'users': users }

@post('/user')
async def user_adds(request, params):
    session = await get_session(request)
    username = params.get('username')
    password = params.get('password')
    email = params.get('email')
    verify_code = params.get('verify_code')
    if not (username and password and email):
        return { 'error': 'Bad submit!' }
    if len(username) < 3 or len(password) < 3 or '@' not in email:
        return { 'error': 'Bad input!' }
    if not check(session, verify_code):
        return { 'error': 'Bad verify_code!'}
    if await models.User.fetchone(where=("`username`='%s'" % username)):
        return { 'error': 'Duplicated username' }
    user = models.User()
    user.fill(username, password, email, 1)
    await user.save()
    return { 'error': None }

@get('/verify')
async def get_verify(request, params):
    session = await get_session(request)
    verify_code = await verity(session)
    return { 'error': None, 'verify_code': verify_code }

@get('/su')
async def super(request, params):
    session = await get_session(request)
    session['power'] = 0
    return { 'error': None, 'Tip': 'Your power is super now !!!' }

@get('/exit')
async def exit(request, params):
    session = await get_session(request)
    session['power'] = 1
    return { 'error': None, 'Tip': 'You have exited super power!!!' }