#-*-coding:UTF-8-*-

WIDTH_LIMIT = 80
INDENTATION_WIDTH = 2

class Printable(object):
    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def to_str(self, level=0):
        # level += 1
        class_str = str(self.__class__)
        data_str = readable_str(self.__dict__, level)
        if len(class_str) + len(data_str) < WIDTH_LIMIT:
            return '%s %s' % (class_str, data_str)
        iden = identation(level)
        return class_str + '\n' + iden + data_str



def readable_str(data, level=0):
    if type(data) in [type(''), type(u'')]:
        return string_str(data)
    if type(data) == type({}):
        return dict_str(data, level)
    if type(data) == type([]):
        return list_str(data, level)
    if issubclass(type(B()), Printable):
        return printable_obj_str(data, level)
    return str(data)

def string_str(data):
    return "'" + str(data) + "'"

def dict_str(data, level=0):
    if len(str(data)) < WIDTH_LIMIT:
        return str(data)
    level += 1
    iden = identation(level)
    lines = []
    for key in data:
        line = readable_str(key, level) + ': ' + readable_str(data[key], level)
        lines.append(line)
    return '{\n' + iden + (',\n' + iden).join(lines) + '\n' + identation(level - 1) + '}'

def list_str(data, level=0):
    if len(str(data)) < WIDTH_LIMIT:
        return str(data)
    level += 1
    iden = identation(level)
    lines = [readable_str(item, level) for item in data]
    return '[\n' + iden + (',\n' + iden).join(lines) + '\n' + identation(level - 1) + ']'

def printable_obj_str(data, level=0):
    if len(str(data)) < WIDTH_LIMIT:
        return str(data)
    level += 1
    # iden = identation(1)
    # return iden + data.to_str(level)
    return data.to_str(level)

def identation(level):
    return ' ' * INDENTATION_WIDTH * level



if __name__ == '__main__':
    class A(Printable):
        def __init__(self):
            self.a = 1
            self.b = [2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5]
            self.c = '3333333333333333333333333333'

    class B(Printable):
        def __init__(self):
            self.a = 1
            self.b = [2, 3]
            self.c = '3'

    class C(Printable):
        def __init__(self, class_name):
            a = class_name()
            self.data = [a, a, a, a]


    print C(A)
    print C(B)

