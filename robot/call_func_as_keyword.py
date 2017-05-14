from robot.libraries.BuiltIn import BuiltIn

def kw(func_name, *args):
    if __name__ == '__main__':
        return eval(func_name)(*args)
    return BuiltIn().run_keyword(func_name, *args)

def show_hello():
    kw('show_word', 'hello')


def show_word(text):
    print(text)




if __name__ == '__main__':
    show_hello()
