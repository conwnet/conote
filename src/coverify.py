
import random

def update():
    return '0000'
    return '%04d' % int(random.random() * 10000)

async def verity(session):
    session['verify'] = update()
    return session.get('verify')

def check(session, verify_code):
    result = session.get('verify') == verify_code
    session['verify'] = update()
    return result