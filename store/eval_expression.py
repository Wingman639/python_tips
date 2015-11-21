

a = [1, 2]
b = {1: True, 2: True, 3: False}
text = '''
b[a[0] + a[1]]
'''

print eval(text)

text = "__import__('os').system('ls')"

print eval(text)