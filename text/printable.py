#-*-coding:UTF-8-*-
import pickle

WIDTH_LIMIT = 20
INDENTATION_WIDTH = 2
INGORE_EMPTY_FIELDS = True


#---------------------------------------
class Printable(object):
    def __str__(self):
        return self.to_str()

    def __repr__(self):
        return self.__str__()

    def __unicode__(self):
        return self.__str__()

    def to_str(self, level=0):
        return readable_str(self.__dict__, level)

    # def set_data(self, *initial_data, **kwargs):
    #     for dictionary in initial_data:
    #         for key in dictionary:
    #             setattr(self, key, dictionary[key])
    #     for key in kwargs:
    #         setattr(self, key, kwargs[key])


#---------------------------------------
def readable_str(data, level=0):
    if INGORE_EMPTY_FIELDS and not data:
        return
    if type(data) in [type(''), type(u'')]:
        return string_str(data, level)
    if type(data) == type({}):
        return dict_str(data, level)
    if type(data) == type([]):
        return list_str(data, level)
    if issubclass(type(data), Printable):
        return obj_str(data, level)
    return str(data)

def string_str(data, level):
    if INGORE_EMPTY_FIELDS and not data:
        return
    if INGORE_EMPTY_FIELDS and data == 'none':
        return
    quota = "'"
    data_str = str(data)
    if quota in data_str:
        quota = '"'
    return quota + data_str + quota

def dict_str(data, level=0):
    if len(str(data)) < WIDTH_LIMIT:
        return str(data)
    level += 1
    iden = identation(level)
    lines = []
    for key in data:
        key_str = readable_str(key, level)
        value_str = readable_str(data[key], level)
        if INGORE_EMPTY_FIELDS and (not key_str or not value_str):
            continue
        line = key_str + ': ' + value_str
        lines.append(line)
    return '{\n' + iden + (',\n' + iden).join(lines) + '\n' + identation(level - 1) + '}'

def list_str(data, level=0):
    if len(str(data)) < WIDTH_LIMIT:
        return str(data)
    level += 1
    iden = identation(level)
    lines = [readable_str(item, level) for item in data]
    return '[\n' + iden + (',\n' + iden).join(lines) + '\n' + identation(level - 1) + ']'

def obj_str(data, level=0):
    data_str = data.to_str(level)
    return readable_str(eval(data_str), level)

def identation(level):
    return ' ' * INDENTATION_WIDTH * level



#---------------------------------------
def save_text(file_name, data):
    with open(file_name, 'w') as f:
        f.write(readable_str(data))

def load_data(file_name):
    with open(file_name, 'r') as f:
        return pickle.load(f)

def save_data(file_name, data):
    with open(file_name, 'w') as f:
        pickle.dump(data, f)




#---------------------------------------
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


    # print C(A)
    # print C(B)

    data = [
      {
      'preconditionlist': [],
      'operationvalue': 'none',
      'value': 'UNIQUE',
      'preconditionvalue': 'none',
      'exp': '',
      'logic': '',
      'preflist': [
                  {
            'occurs': [],
            'optionalcls': '',
            'links': [
              {
                'source': [
                                      {
                      'name': 'RadioAccessTechnology',
                      'minOccurs': 'none',
                      'minIncl': 'none',
                      'maxIncl': 'none',
                      'value': 'none',
                      'alias': 'none',
                      'parentClass': 'none',
                      'scope': 'none',
                      'maxOccurs': 'none',
                      'typeclass': 'WDP',
                      'operation': 'none'
                    }
                ],
                'target': [
                                      {
                      'name': 'RadioAccessTechnology',
                      'minOccurs': 'none',
                      'minIncl': 'none',
                      'maxIncl': 'none',
                      'value': 'none',
                      'alias': 'none',
                      'parentClass': 'WSP',
                      'scope': 'SINGLE',
                      'maxOccurs': 'none',
                      'typeclass': 'WDP',
                      'operation': 'none'
                    }
                ]
              }
            ],
            'minOccurs': 'none',
            'minIncl': 'none',
            'mominOccurs': 'none',
            'maxIncl': 'none',
            'value': 'none',
            'optionalnum': '',
            'alias': 'none',
            'momaxOccurs': 'none',
            'parentClass': 'WSP',
            'maxOccurs': 'none',
            'modification': 'none',
            'typeclass': 'WDP',
            'operation': 'none',
            'scope': 'SINGLE',
            'name': 'ARFCN'
          }
      ]
    },
      {
      'preconditionlist': [],
      'operationvalue': 'none',
      'value': 'none',
      'preconditionvalue': 'none',
      'exp': '',
      'logic': '',
      'preflist': [
                  {
            'occurs': [],
            'optionalcls': '',
            'links': [],
            'minOccurs': 'none',
            'minIncl': '0',
            'mominOccurs': 'none',
            'maxIncl': '16383',
            'value': '1',
            'optionalnum': '',
            'alias': 'none',
            'momaxOccurs': 'none',
            'parentClass': 'none',
            'maxOccurs': 'none',
            'modification': 'none',
            'typeclass': 'WDP',
            'operation': 'none',
            'scope': 'none',
            'name': 'RadioAccessTechnology'
          }
      ]
    },
      {
      'preconditionlist': [],
      'operationvalue': 'none',
      'value': 'none',
      'preconditionvalue': 'none',
      'exp': '',
      'logic': '',
      'preflist': [
                  {
            'occurs': [],
            'optionalcls': '',
            'links': [],
            'minOccurs': 'none',
            'minIncl': '0',
            'mominOccurs': 'none',
            'maxIncl': '1023',
            'value': '2|3',
            'optionalnum': '',
            'alias': 'none',
            'momaxOccurs': 'none',
            'parentClass': 'none',
            'maxOccurs': 'none',
            'modification': 'none',
            'typeclass': 'WDP',
            'operation': 'none',
            'scope': 'none',
            'name': 'RadioAccessTechnology'
          }
      ]
    }
]

    print readable_str(data)