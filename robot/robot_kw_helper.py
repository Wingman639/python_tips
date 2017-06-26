import sys
from robot.libraries.BuiltIn import BuiltIn

def keyword_func(func):
    def new_func(*args, **kw):
        if is_robot_running() and new_func.called_count <= 0:
            new_func.called_count += 1
            result = BuiltIn().run_keyword(func.__name__, *args, **kw)
            new_func.called_count -= 1
            return result
        else:
            return func(*args, **kw)

    new_func.called_count = 0
    return new_func

def is_robot_running():
    main_entry = sys.argv[0]   # /robot/run.py
    return 'robot' in main_entry and 'run.py' in main_entry


if __name__ == '__main__':
    import time
    @keyword_func
    def say_hello():
        print 'hello'
        time.sleep(0.01)
        return time.time()

    say_hello()