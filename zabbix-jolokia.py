# coding: utf-8
import logging
import re
import json
from pprint import pformat, pprint
from pyjolokia import Jolokia

logging.basicConfig(level=logging.DEBUG)

class ZabbixData(object):
    def __init__(self, url, user, pwd, beans=['*.*']):
        self.j4p = Jolokia(url)
        self.j4p.auth(httpusername=user, httppassword=pwd)
        self.data = {}
        for bean in beans:
            d = JolokiaData(self.j4p, bean).get_data()
            self.data.update(d)

    def get_data(self):
        return self.data

class JolokiaData(object):
    def __init__(self, j4p, domain='*:*'):
        self.j4p = j4p
        self.beans = self.j4p.request(type='search', mbean=domain)['value']
        self.data = {}
        self.get_values()

    def get_values(self):
        for bean in self.beans:
            b,t = bean.split(':', 1)
            b_list = self.j4p.request(type = 'list', path='%s/%s' % (b,t))
            try:
                for a in b_list['value']['attr']:
                    if b_list['value']['attr'][a]['rw'] is False:
                        try:
                            data = self.j4p.request(type = 'read', mbean=bean,
                                                    attribute=a)['value']
                            self.set_data(bean, a, data)
                        except KeyError:
                            # has no value, so pass
                            pass
            except KeyError:
                # has no value, so pass
                pass

    def set_data(self, bean, attribute, data):
        if isinstance(data, dict):
            for d in data:
                self.set_data(bean, '.'.join([attribute, d]), data[d])
        elif isinstance(data, list):
            for d in data:
                self.set_data(bean, attribute, d)
        else:
            key = self._cleaner('%s.%s' % (bean, attribute))
            self.data[key] = data

    def get_data(self):
        return self.data

    def __repr__(self):
        return pformat(self.data, width=150)

    @staticmethod
    def _cleaner(data):
        data = re.sub(r'[:,]([^=]+)=', '.', data)
        data = re.sub(r' ', '', data)
        data = re.sub(r'"', '', data)
        return data


if __name__ == "__main__":
    zbx = json.dumps(ZabbixData('http://localhost:8089/jolokia', 'script', 'foo', ['java.lang:type=Memory', 'com.mycompany:*']).get_data())
    print(zbx)

