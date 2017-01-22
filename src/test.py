# Test script by SpringHack

TestList = []

def Log(msg, color = '36'):
    print('\033[1;%s;40m=> %s\033[0m' % (color ,msg))

def TestCase(Prompt):
    def Wrapper(Func):
        TestList.append({
            'prompt' : Prompt,
            'func'   : Func
        })
        return Func
    return Wrapper


@TestCase('Demo test case')
def Demo():
    try:
        code = open('src/test.py').read()
        Log(code, '32')
        Log('Demo test successful !')
    except:
        Log('Demo test failed !')

@TestCase('Config test case')
def Config():
    json    =   __import__('json')
    try:
        obj     =   json.load(open('src/config.json'))
        Log(obj, '32')
        Log('Config read successful !')
    except:
        Log('Config read failed !')

@TestCase('App verify test case')
def AppVerify():
    os      =   __import__('os')
    os.chdir('./src')
    try:
        app     =   __import__('app')
        Log('App verify successful !')
    except:
        Log('App verify failed !')

def Test(Prompt, Func):
    Log('==> %s start ...' % Prompt, '31')
    Func()
    Log('==> %s end !' % Prompt, '31')
    print('\n')

def main():
    print('\n')
    for test in TestList:
        Test(test['prompt'], test['func'])

if __name__ == '__main__':
    main()
