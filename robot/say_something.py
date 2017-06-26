import time
from robot_kw_helper import keyword_func

@keyword_func
def say_hello():
    print 'say: '
    return say('hello')

@keyword_func
def say(word):
    print word
    time.sleep(0.01)
    return now()


@keyword_func
def now():
    print 'now time'
    return time.time()

if __name__ == '__main__':
    say_hello()