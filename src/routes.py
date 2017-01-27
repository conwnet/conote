
import models, functools
from coroweb import get, post
from aiohttp_session import get_session
from coverify import verity, check

def logined(func):
    @functools.wraps(func)
    async def wrapper(*args, **kw):
        if (await get_session(args[0])).get('id'):
            return await func(*args, **kw)
        return {'error': 'Permission denied'}
    return wrapper

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
        return { 'error': 'Bad verify_code!' }

    user = await models.User.fetchone(where=("`username`='%s'" % username))
    if user and user.get('password') == password:
        session['id'] = user.id
        session['username'] = user.username
        session['power'] = user.power
        return { 'error': None }
    return { 'error': 'Bad password' }


@get('/login')
@logined
async def get_login(request, params):
    return { 'error': None }


@get('/user/id/{id}')
@logined
async def get_user_by_id(request, params):
    session = await get_session(request)
    id = params.get('id')
    user = await models.User.fetchone(where=("`id`='%s'" % id))

    if user:
        if session.get('id') == user.id or session.get('power') == 0:
            return { 'error': None, 'user': { 'id': user.id, 'username': user.username, "email":user.email}}
        return { 'error': 'Permission denied' }
    return { 'error': 'Not found' }


@get('/user/username/{username}')
@logined
async def get_user_by_username(request, params):
    session = await get_session(request)
    username = params.get('username')
    user = await models.User.fetchone(where=("`username`='%s'" % username))

    if user:
        if session.get('id') == user.id or session.get('power') == 0:
            return { 'error': None, 'user': { 'id': user.id, 'username': user.username } }
        return { 'error': 'Permission denied' }
    return { 'error': 'Not found' }


@get('/user')
async def get_users(request, params):
    session = await get_session(request)

    if session.get('power') != 0:
        return { 'error': 'Permission denied' }

    users = {}
    for user in await models.User.fetchall():
        users[user.id] = { 'username': user.username, 'password': user.password, "email": user.email}
    return { 'error': None, 'users': users }


@post('/user')
async def save_user(request, params):
    session = await get_session(request)
    username = params.get('username')
    password = params.get('password')
    email = params.get('email')
    verify_code = params.get('verify_code')

    if not (username and password and email):
        return { 'error': 'Bad submit!' }

    if len(username) < 3 or len(password) < 3 or '@' not in email:
        return { 'error': 'Invalid input!' }

    if not check(session, verify_code):
        return { 'error': 'Bad verify_code!' }

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

@post('/note')
@logined
async def save_note(request, params):
    session = await get_session(request)
    user_id = session.get('id')
    note_id = params.get('id')
    title = params.get('title')
    content = params.get('content')
    public = params.get('public')

    # check input
    if not (title and content and public):
        return { 'error': 'Bad submit' }

    ## check permission
    if note_id:
        note = await models.Note.find(note_id)
        if not ((note and note.author_id == user_id) or (note.public & 2)):
            return {'error': 'Permission denied'}

    ## create a new note
    new_note = models.Note()
    new_note.fill(user_id, note_id or '0', '0', title, content, public)
    await new_note.save()

    ## set old note's next_id
    if note_id:
        note.next_id = new_note.id
        await note.save()
    return {'error': None}

@get('/note')
@logined
async def get_notes(request, params):
    session = await get_session(request)
    id = session.get('id')
    notes = {}
    for note in await models.Note.fetchall("`author_id`=? and `next_id`=?", (id, '0')):
        notes[note.id] = { 'author_id: ': note.author_id}
    return { 'error': None, 'notes': notes }


@get('/note/id/{id}')
@logined
async def get_note_by_id(request, params):
    session = await get_session(request)
    id = session.get('id')


@get('/su')
async def super(request, params):
    session = await get_session(request)
    session['power'] = 0
    return { 'error': None, 'Tip': 'Your power is super now !!!' }


@get('/exit')
async def exit(request, params):
    session = await get_session(request)
    session['id'] = '0'
    session['power'] = 1
    return { 'error': None, 'Tip': 'You have exited super power!!!' }

@get('/test')
async def test(request, params):
    user = await models.User.find('40d8872ee44a11e69c646817294b73a4')
    user = await user.f(pk='40d8872ee44a11e69c646817294b73a4')
    return {'error': user.username}