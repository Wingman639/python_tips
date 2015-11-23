
import argparse
import requests
import bs4
import sys


from one_pronto_page_select import get_pronto_data_from_html

pronto_url = 'https://'
login_data = {'target' : pronto_url,
			 'SMENC' : 'ISO-8859-1',
			 'SMLOCALE' : 'US-EN',
			 'USER' : '',
			 'PASSWORD' : '',
			 'postpreservationdata' : ','
			}

login_url = 'https://'

BASE_URL = 'https://'

seperator = u'\n==========================\n'


def get_pronto_list_html(session):
	response = session.post(login_url, data=login_data)
	return response.text


def save_text(file_name, text):
	with open(file_name, 'w') as f:
		f.write(text)

def get_prontos_from_list_html(html, base_url):
	soup = bs4.BeautifulSoup(html, 'html.parser')
	even_list = soup.select('tr.even a[href^=./problemReport.html?]')
	odd_list = soup.select('tr.odd a[href^=./problemReport.html?]')
	items = even_list + odd_list
	return get_prontos_from_items(items, base_url)


def get_prontos_from_items(items, base_url):
	prontos = []
	for item in items:
		pronto = get_pronto_from_html_tag(item, base_url)
		if pronto:
			prontos.append(pronto)
	return prontos


def get_pronto_from_html_tag(tag, base_url):
	pronto = {}
	link = tag.attrs.get('href')
	pronto['url'] = base_url + link[1:]
	return pronto


def request_pronto_data_with_url(session, pronto):
	response = session.get(pronto['url'])
	html = response.text
	pronto['data'] = get_pronto_data_from_html(html)


def readable_dict_string(dict_data):
	text = u''
	for key, value in dict_data.items():
		text += u'%s : %s\n' % (readable_string(key), readable_string(value))
	return text

def readable_list_string(list_data):
	text = u''
	for item in list_data:
		text += seperator + readable_string(item)
	return text

def readable_string(data):
	text = u''
	if type(data) is type({}):
		text += readable_dict_string(data)
	elif type(data) is type([]):
		text += readable_list_string(data)
	else:
		try:
			data_text = str(data)
		except:
			data_text = str([data])

		text += data_text
	return text


def save_obj(obj_name, obj):
	with open(obj_name, 'w') as f:
		save_text(obj_name, str(obj))

def load_obj(obj_name):
	with open(obj_name, 'r') as f:
		text = f.read()
		return eval(text)


def get_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--user')
	parser.add_argument('-p', '--password')
	args = parser.parse_args()
	if args.user:
		login_data['USER'] = args.user
	if args.password:
		login_data['PASSWORD'] = args.password


def save_html(html):
	save_text('prontos.html', str([html])[3:-2])

def get_html():
	with open('prontos.html', 'r') as f:
		return f.read()


def main():
	get_args()
	DEBUG = False
	if DEBUG:
		html = get_html()
		prontos = load_obj('prontos')
	else:
		session = requests.Session()
		html = get_pronto_list_html(session)
		save_html(html)
		prontos = get_prontos_from_list_html(html, BASE_URL)
		for pronto in prontos:
			request_pronto_data_with_url(session, pronto)
		save_obj('prontos', prontos)
	save_text('prontos.txt', str(prontos))
	text = readable_string(prontos)
	#print text
	save_text('prontos_better.txt', text)



def test():
	get_args()

if __name__ == '__main__':
	main()
	#test()



