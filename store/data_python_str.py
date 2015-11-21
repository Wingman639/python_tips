

text = '[1, 2, 3]'

with open('pronto', 'r') as f:
	text = f.read()

data = eval(text)

print type(data)
print data
print data[0]