from __future__ import print_function
from nanomsg import Socket, PAIR, PUB

s1 = Socket(PAIR)
s2 = Socket(PAIR)
s1.bind('inproc://bob')
s2.connect('inproc://bob')
s1.send(b'hello nanomsg')
print(s2.recv())
s1.close()
s2.close()



with Socket(PAIR) as s3:
	with Socket(PAIR) as s4:
		s3.bind('inproc://demo')
		s4.connect('inproc://demo')
		s3.send('hi, I use "with"')
		print(s4.recv())
		s4.send('Ok, I see.')
		print(s3.recv())


