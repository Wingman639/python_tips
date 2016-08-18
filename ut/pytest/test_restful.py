#-*-coding:UTF-8-*-
import pytest
import mock
import restful


def get_parameters(*args, **kwargs):
	return args, kwargs


@mock.patch('requests.get', mock.MagicMock(side_effect = get_parameters))
def test_restful_get_default_para_headers_shall_be_json():
	assert restful.RESTfulClient().get(url='a_url') == \
	(('a_url',), {'headers': {'Content-Type': 'application/json'}, 'params': None})


@mock.patch('requests.get', mock.MagicMock(side_effect = get_parameters))
def test_restful_get_full_parameter():
	assert restful.RESTfulClient().get(url='a_url', headers={'Content-Type':'application/a_xml'}, params='nameisliei') == \
	(('a_url',), {'headers':{'Content-Type':'application/a_xml'}, 'params':'nameisliei'})


@mock.patch('requests.post', mock.MagicMock(side_effect = get_parameters))
def test_restful_post_default_para_headers_shall_be_json():
	assert restful.RESTfulClient().post(url='a_url') == \
	(('a_url',), {'headers': {'Content-Type': 'application/json'}, 'json': None})


@mock.patch('requests.post', mock.MagicMock(side_effect = get_parameters))
def test_restful_post_full_para_playload_shall_assign_to_json():
	assert restful.RESTfulClient().post(url='a_url', headers={'Content-Type':'application/b_xml'}, payload={'nameislili':'female'}) == \
	(('a_url',), {'headers': {'Content-Type': 'application/b_xml'}, 'json': {'nameislili':'female'}})


@mock.patch('requests.delete', mock.MagicMock(side_effect = get_parameters))
def test_restful_delete_default_para_headers_shall_be_json():
	assert restful.RESTfulClient().delete(url='a_url') == \
	(('a_url',), {'headers': {'Content-Type': 'application/json'}})


@mock.patch('requests.delete', mock.MagicMock(side_effect = get_parameters))
def test_restful_delete_full_parameter():
	assert restful.RESTfulClient().delete(url='a_url', headers={'Content-Type':'application/c_xml'}) == \
	(('a_url',), {'headers': {'Content-Type': 'application/c_xml'}})




if __name__ == '__main__':
	import os
	import sys

	r = os.system('py.test')
	if r != 0:
		sys.exit(-1)

