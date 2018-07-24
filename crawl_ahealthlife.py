import os
import re
import random
import time
import requests
import grequests
from copy import deepcopy
from urllib.parse import urlparse
import subprocess
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
'''
并发访问拿到js
{
'proxy':'139.224.24.26:8888', 
'agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',

]}
{'headers': 
    {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; 
            Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)', 
        'Referer': 'https://ahealthlife.net/'}, 
'proxy': {'http': 'http://39.134.161.14:8080/'}, 
'params': {'jschl_vc': 'b5e99db21d22dc1152d513f4f4f6774e', 'pass': '1531962981.552-LkfeYpkcoS', 'jschl_answer': 'console.log(require(\'vm\').runInNewContext(\'var s,t,o,p,b,r,e,a,k,i,n,g,f, elkNeoM={"nd":+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(+!![]))/+((!+[]+!![]+!![]+!![]+!![]+[])+(!+[]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]))};        ;elkNeoM.nd+=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(+!![]))/+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![])+(!+[]+!![])+(+!![])+(!+[]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![]));elkNeoM.nd-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]));elkNeoM.nd-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(+!![]))/+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+[])+(+[])+(!+[]+!![]+!![]+!![]));elkNeoM.nd-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![])+(!+[]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]));elkNeoM.nd-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]));elkNeoM.nd-=+((!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+[])+(+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![])+(!+[]+!![])+(!+[]+!![]+!![]+!![])+(!+[]+!![]+!![]))/+((!+[]+!![]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![])+(+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![])+(+[]));+elkNeoM.nd.toFixed(10) + 15\', Object.create(null), {timeout: 5000}));'}}

启动4个node进程处理所有js(cpu密集型)



'''


class Cloudflare():
    def __init__(self):
        self.session = requests.Session()
        self.config =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        self.proxies = self.get_config('proxy')
        self.agents = self.get_config('agent')
        self.url = 'https://ahealthlife.net/'
        self.response = []
        self.results = []
        self._kwargs = []


    def is_file(self, filename):
        return os.path.exists(filename) and os.path.isfile(filename)

    def is_path(self, pathname):
        return os.path.exists(pathname) and os.path.isdir(pathname)
    
    def is_ip(self, ip):
        r = re.match('(\d+).(\d+).(\d+).(\d+):(\d+)', ip)

        return ip if r else None

    def _random(self, data):
        # return data[random.randint(0, len(data)-1)]
        return random.choice(data)

    def get_config(self, name):
        config_file = os.path.join(self.config, name)
        proxies = []
        if self.is_file(config_file):
            with open(config_file, 'r') as f:
                for line in f.readlines():
                    if len(line.strip()) == 0:
                        continue
                    proxies.append(line.strip())
        else:
            raise Exception('No such file or directory: %s' % config_file)

        return proxies

    def is_cloudflare_challenge(self, resp):
        return (
            resp.status_code == 503
            and resp.headers.get("Server", "").startswith("cloudflare")
            and b"jschl_vc" in resp.content
            and b"jschl_answer" in resp.content
        )


    def crawl(self):
        s = time.time()
        tasks = []
        _o_kwargs = []
        for i in range(10):
            original_kwargs = {}
            original_kwargs['proxies'] = {'http': 'http://%s/' % self._random(self.proxies)}
            original_kwargs['headers'] = {'User-Agent': self._random(self.agents)}
            original_kwargs['timeout'] = 5
            # resp = grequests.get(self.url, headers=pyload['headers'], proxies=pyload['proxy'], timeout=5)
            resp = grequests.get(self.url, **original_kwargs)
            tasks.append(resp)
            _o_kwargs.append(original_kwargs)
        res = grequests.imap(tasks)
        x = 0
        for r in res:
            if self.is_cloudflare_challenge(r):
                self.solve_cf_challenge(r, **_o_kwargs[x])
            x += 1

    def solve_cf_challenge(self, resp, **original_kwargs):
        _kwargs = {}
        _kwargs['original_kwargs'] = original_kwargs
        _kwargs['body'] = resp.text
        _kwargs['parsed_url'] = urlparse(resp.url)
        _kwargs['domain'] = _kwargs['parsed_url'].netloc
        _kwargs['submit_url'] = "%s://%s/cdn-cgi/l/chk_jschl" % (_kwargs['parsed_url'].scheme, _kwargs['domain'])

        _kwargs['cloudflare_kwargs'] = deepcopy(original_kwargs)
        _kwargs['params'] = _kwargs['cloudflare_kwargs'].setdefault("params", {})
        _kwargs['headers'] = _kwargs['cloudflare_kwargs'].setdefault("headers", {})
        _kwargs['headers']['Referer'] = resp.url
        try:
            _kwargs['params']["jschl_vc"] = re.search(r'name="jschl_vc" value="(\w+)"', _kwargs['body']).group(1)
            _kwargs['params']["pass"] = re.search(r'name="pass" value="(.+?)"', _kwargs['body']).group(1)
        except Exception as e:
            raise ValueError("Unable to parse Cloudflare anti-bots page: %s" % (e.message))

        _kwargs['params']["jschl_answer"] = self.get_challenge(_kwargs['body'], _kwargs['domain'])
        _kwargs['cloudflare_kwargs']["allow_redirects"] = False

        self._kwargs.append(_kwargs)
    
    def nodejs(self, js):
        result = subprocess.check_output(["node", "-e", js['params']['jschl_answer']]).strip()
        js['params']['jschl_answer'] = float(result)
        return js

    def parse_js(self):
        max_process = 4
        pool = ProcessPoolExecutor(max_workers=max_process)
        self.results = list(pool.map(self.nodejs, self._kwargs))
    
    def get_challenge(self, body, domain):
        try:
            js = re.search(r"setTimeout\(function\(\){\s+(var "
                        "s,t,o,p,b,r,e,a,k,i,n,g,f.+?\r?\n[\s\S]+?a\.value =.+?)\r?\n", body).group(1)
        except Exception:
            raise ValueError("Unable to identify Cloudflare IUAM Javascript on website.")

        js = re.sub(r"a\.value = (.+ \+ t\.length).+", r"\1", js)
        js = re.sub(r"\s{3,}[a-z](?: = |\.).+", "", js).replace("t.length", str(len(domain)))

        js = re.sub(r"[\n\\']", "", js)

        if "toFixed" not in js:
            raise ValueError("Error parsing Cloudflare IUAM Javascript challenge.")

        js = "console.log(require('vm').runInNewContext('%s', Object.create(null), {timeout: 5000}));" % js

        return js

    def get_redirect(self, pyload):
        redirect = self.session.get(pyload['submit_url'], **pyload['cloudflare_kwargs'])
        redirect_location = urlparse(redirect.headers["Location"])
        if not redirect_location.netloc:
            redirect_url = "%s://%s%s" % (parsed_url.scheme, domain, redirect_location.path)
            return self.session.get(redirect_url, **pyload['original_kwargs'])
        return self.session.get(redirect.headers["Location"], **pyload['original_kwargs'])

    def start(self):
        self.crawl()
        self.parse_js()
        for i in self.results:
            print(self.get_redirect(i))


if __name__ == '__main__':
    cn = Cloudflare()
    cn.start()