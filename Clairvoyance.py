import requests
import time
import hashlib
import json
from urllib.parse import  quote
from pyquery import PyQuery as pq
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Clairvoyance():
    def __init__(self):
        self.session = requests.Session()
        self.cookies = ''
        self.token = ''

    def login(self):        
        r = self.session.get('https://www.tianyancha.com', verify=False)
        if r.ok:
            for cookie in r.cookies.items():
                self.cookies += '%s=%s; ' % cookie

        r = self.session.post('https://www.tianyancha.com/cd/login.json', headers={
            'Host': 'www.tianyancha.com',
            'Connection': 'keep-alive',
            'Content-Length': '105',
            'Accept': '*/*',
            'Origin': 'https://www.tianyancha.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Content-Type': 'application/json; charset=UTF-8',
            'Referer': 'https://www.tianyancha.com/',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookies

        }, data=json.dumps({
            "mobile": "13772032410",
            "cdpassword": "d2fdd87dfecd37cbec7e0f9f2b72c788",
            "loginway": "PL",
            "autoLogin": True
            }),
        verify=False
        )
        self.token = json.loads(r.text)['data']['token']
        self.cookies += '; auth_token='+self.token
        
        return r.ok

    def crawl(self, key):
        res = {}
        res['company'] = key
        r = self.session.get('https://www.tianyancha.com/search?key='+quote(key), headers={
            'Host': 'www.tianyancha.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.tianyancha.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookies
        })

        if r.ok:
            div = pq(r.text)('.search-item')[0]
            _id = pq(div)('.search-result-single   ').attr['data-id']
            primary_resp  = self.search('https://www.tianyancha.com/company/'+_id)
            primary = self.parse_search(primary_resp)
            shareholders = []
            for company, url in primary.items():
                secondary_resp = self.search(url)
                secondary = self.parse_search(secondary_resp)

                _shareholders = []
                for _company, _url in secondary.items():
                    third_resp = self.search(_url)
                    third = self.parse_search(third_resp)
                    
                    __shareholders = []
                    for __company, __url in third.items():
                        fourth_resp = self.search(__url)
                        fourth = self.parse_search(fourth_resp)
                        __shareholders.append({'company': __company, 'shareholders': 
                            {'company': ___company for ___company, ___url in fourth.items()}})
                    _shareholders.append({'company': _company, 'shareholders': __shareholders})
                shareholders.append({'company': company, 'shareholders': _shareholders})
            res['shareholders'] = shareholders

            print(res)

                        

    def search(self, url):
        print(url)
        r = self.session.get(url, headers={
            'Host': 'www.tianyancha.com',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://www.tianyancha.com',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': self.cookies
        }, verify=False)
        return r if r.ok else None

    def parse_search(self, resp):
        res = {}
        trs = pq(resp.text)('#_container_holder table tr')
        for _a in pq(trs)('td')('div .dagudong a'):
            res[pq(_a).text()] = pq(_a).attr['href']

        # print(res)
        return res
                


    def start(self):
        if self.login():
            key = '西安图迹信息科技有限公司'
            self.crawl(key)

if __name__ == '__main__':

    cy = Clairvoyance()
    cy.start()