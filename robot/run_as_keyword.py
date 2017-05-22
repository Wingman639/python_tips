import functools
from robot.libraries.BuiltIn import BuiltIn


def keyword_func(func):
    def new_func(*args, **kw):
        if __name__ == '__main__' or new_func.called_as_keyword:
            return func(*args, **kw)
        else:
            new_func.called_as_keyword = True
            return BuiltIn().run_keyword(func.__name__, *args, **kw)

    new_func.called_as_keyword = False
    return new_func

@keyword_func
def show_good_morning():
    value = show('good morning')
    return 2 + value

@keyword_func
def show(text):
    print(text)
    return 1


if __name__ == '__main__':
    print show_good_morning()
    print show_good_morning.__name__
    print dir(show_good_morning)
    print show_good_morning.func_name
