
import re
import bs4



#print soup.find(attrs={'id': 'description'}).string


fields_1 = {
			'pronto id' : {'attrs' : {'name': 'prID'}, 'value_attr': 'value'},
			'fault id' : {'attrs' : {'name': 'faultID'}, 'value_attr': 'value'},
			'pronto title' : {'attrs' : {'name': 'src_pridTitle'}, 'value_attr': 'value'},
			'pronto report date' : {'attrs' : {'name': 'probReportCreationDate'}, 'value_attr': 'value'},
			'currect status' : {'attrs' : {'class': 'current_status'}, 'value_attr': 'string'},
			'description' : {'attrs' : {'id': 'description'}, 'value_attr': 'string'},
			}

def get_field_1_tag(soup, field_attrs):
	return soup.find(attrs=field_attrs)

def get_field_1_value(soup, parameter):
	tag = get_field_1_tag(soup, parameter['attrs'])
	value_attr = parameter['value_attr']
	if tag:
		if value_attr in tag.attrs:
			return tag.attrs[value_attr]
		elif tag.string:
			return tag.string.strip()
	#print tag


def get_pronto_fields_1_values(soup, fields_1):
	values = {}
	for key, parameter in fields_1.items():
		values[key] = get_field_1_value(soup, parameter)
	return values



fields_2 = {
		'reported by' : {'attrs' : {'href': '#h_reportedby'}, 'next': 'div'},
		'author name' : {'attrs' : {'href': '#h_authorName'}, 'next': 'li'},
		'author group' : {'attrs' : {'href': '#h_authorGroup'}, 'next': 'li'},
		'group in charge' : {'attrs' : {'href': '#h_groupincharge'}, 'next': 'div'},
		'development fault coordinator' : {'attrs' : {'href': '#h_devcordinator'}, 'next': 'div'},
		'problem type' : {'attrs' : {'href': '#h_problemtype'}, 'next': 'div'},
		'seviority' : {'attrs' : {'href': '#h_seviority'}, 'next': 'div'},
		'priority' : {'attrs' : {'href': '#h_rdpriority'}, 'next': 'div'},
		'top importance' : {'attrs' : {'href': '#h_topimportance'}, 'next': 'div'},
		'test sub phase' : {'attrs' : {'href': '#h_testsubphase'}, 'next': 'div'},
		'repeatability' : {'attrs' : {'href': '#h_repeatability'}, 'next': 'div'},
		'product' : {'attrs' : {'href': '#h_product'}, 'next': 'div'},
		'status log' : {'attrs' : {'href': '#h_statusLog'}, 'next': 'input'},
		}

def get_field_2_tag(soup, field_attrs, next_tag_name):
	tag = soup.find(attrs=field_attrs)
	if next_tag_name:
		return tag.find_next(next_tag_name)
	#print tag

def get_field_2_value(soup, parameter):
	tag = get_field_2_tag(soup, parameter['attrs'], parameter['next'])
	if tag and tag.string:
		return tag.string.strip()
	#print tag

def get_pronto_fields_2_values(soup, fields):
	values = {}
	for key, parameter in fields.items():
		values[key] = get_field_2_value(soup, parameter)
	return values


def get_pronto_data_from_html(html):
	soup = bs4.BeautifulSoup(html, 'html.parser')
	pronto_data_1 = get_pronto_fields_1_values(soup, fields_1)
	pronto_data_2 = get_pronto_fields_2_values(soup, fields_2)
	return dict(pronto_data_1, **pronto_data_2)



def main():
	with open('one_pronto.html', 'r') as f:
		html = f.read()
	soup = bs4.BeautifulSoup(html, 'html.parser')
	#print get_pronto_fields_1_values(soup, fields_1)
	#print get_pronto_fields_2_values(soup, fields_2)




if __name__ == '__main__':
	main()

