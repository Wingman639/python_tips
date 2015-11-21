# coding: utf-8

import pickle

#data = {1:'a', '2':'B', '姓名':'小明'}
data = [1,2,3]

with open('data', 'w') as f:
	pickle.dump(data, f)



with open('data', 'r') as f:
	data_2 = pickle.load(f)

print data_2