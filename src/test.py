
import functools

def logined(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        print(*args, kw.get('a'))
        return func(*args, **kw)
    return wrapper

@logined
def f(a):
    pass

if __name__ == '__main__':
    f(a='good')
