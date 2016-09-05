#-*-coding:UTF-8-*-
import requests

class RESTfulClient(object):
    def get(self, url, headers={'Content-Type':'application/json'}, params=None):
        return requests.get(url, headers=headers, params=params)

    def post(self, url, headers={'Content-Type':'application/json'}, payload=None):
        return requests.post(url, headers=headers, json=payload)

    def delete(self, url, headers={'Content-Type':'application/json'}):
        return requests.delete(url, headers=headers)



if __name__ == '__main__':
    r = RESTfulClient().get('http://bing.com')
    print r.status_code, len(r.text), r.text[:100]

    r = RESTfulClient().post('http://bing.com', payload=None)
    print r.status_code, len(r.text)
