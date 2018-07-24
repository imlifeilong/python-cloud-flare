# -*- coding: UTF-8 -*-
import time
import os
import sys
import re
import getopt
import random
import requests
import cfscrape
import threadpool
import multiprocessing
from gevent import monkey; monkey.patch_all()
import gevent
from concurrent.futures import ThreadPoolExecutor


def retry(func):
    def wrapper(self, *args, **kwargs):
        flag = True
        while flag:
            try: 
                f = func(self, *args, **kwargs)
                flag = False
                return f
            except Exception as e:
                print('Error connecting：%s' % str(e))
                flag = True

        wrapper.__name__ = wrapper.__name__
    return wrapper


class CloudFlareCrawl(object):
    """docstring for CloudFlareCrawl"""
    # def __init__(self, url, method='get', protocol='http', max_process=10, max_thread=800):

    def __init__(self):
        super(CloudFlareCrawl, self).__init__()
        self.session = requests.Session()
        self.scraper = cfscrape.create_scraper(sess=self.session)
        self.config =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        self.sockets = self.get_config('socket')
        self.proxies = self.get_config('proxy')
        self.agents = self.get_config('agent')
        self.keywords = self.get_config('keyword')
        self.method = 'get'
        # self.max_process = max_process
        # self.max_thread = max_thread
        self.url = 'https://ahealthlife.net/'
        # self.url = 'https://www.baidu.com/'
        # self.url = url
        self.data = {}
        self.protocol = 'http'
    
    @retry
    def crawl(self, n):
        payload = self._random(self.keywords)
        agent = self._random(self.agents)
        proxy = self._random(self.proxies)
        headers = {'User-Agent': agent}
        # protocol = [socks5|http|https]
        # proxies = {'http':'%s://%s/' % (protocol1, proxy), 'https':'%s://%s/' % (protocol2, proxy)}
        proxies = {'%s' % self.protocol :'%s://%s/' % (self.protocol, proxy)}

        if self.method == 'get':
            r = self.scraper.get(self.url, headers=headers, proxies=proxies, timeout=20)
            self.is_ok(r, proxy)

        elif self.method == 'post':
            r = self.scraper.get(self.url, params=payload, data=self.data, headers=headers, proxies=proxies)
            self.is_ok(r, proxy)
        time.sleep(1)

    def is_ok(self, response, proxy):
        if response.ok and response.status_code == 200:
            print('[%s] Access to success: %s' % (proxy, self.url))
        else:
            print('[%s] Access failure: %s, %s' % (proxy, self.url, response.status_code))

    def is_file(self, filename):
        return os.path.exists(filename) and os.path.isfile(filename)

    def is_path(self, pathname):
        return os.path.exists(pathname) and os.path.isdir(pathname)
    
    def match_ip(self, ip):
        r = re.match('(\d+).(\d+).(\d+).(\d+):(\d+)', ip)

        return ip if r else None

    def _random(self, data):
        return data[random.randint(0, len(data)-1)]

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

    def allin(self, i):
        max_thread = 1
        pool = threadpool.ThreadPool(max_thread)
        job_list = []
        ths = threadpool.makeRequests(self.crawl, [i for i in range(max_thread)])
        for t in ths:
            pool.putRequest(t)
        pool.wait()

    def start(self):
        max_process = 4
        process = []
        for i in range(max_process):
            p = multiprocessing.Process(target=self.allin, args=(i,))
            p.start()
            process.append(p)

        for j in process:
            j.join()

    def get_e(self):
        tasks = []
        for i in range(5):
            tasks.append(gevent.spawn(self.allin, i))
        gevent.joinall(tasks)

    def get_t(self):
        pool = ThreadPoolExecutor(3)
        pool.map(self.crawl, [i for i in range(5)])

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hu:m:P:T:_', ['help', 'url=', 'method=', 'process=', 'thread=', '_='])
        print(opts, args)
    except getopt.GetoptError as e:
        print(e)
        showUsage()
        sys.exit(2)
    url, method, max_process, max_thread = '', 'get', 1, 1
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            showUsage()
            sys.exit(2)
        elif opt in ('-u', '--url'):
            if isinstance(arg, str):
                url = arg
            else:
                print('Parameter [--url] must be a string and not to be empty!')
                sys.exit(2)
        elif opt in ('-m', '--method'):
            method = arg
        elif opt in ('-P', '--process'):
            arg = int(arg)
            if isinstance(arg, int) and arg > 0:
                max_process = arg
            else:
                print('Parameter [--process] must be an integer and not to be less than 1')
                sys.exit(2)
        elif opt in ('-T', '--thread'):
            arg = int(arg)
            if isinstance(arg, int) and arg > 0:
                max_process = arg
            else:
                print('Parameter [--thread] must be an integer and not to be less than 1')
                sys.exit(2)
    print(url, method, max_process, max_thread)


def showUsage():
    pass


if __name__ == '__main__':
    cf = CloudFlareCrawl()
    # main(sys.argv[1:])
    cf.start()
    # cf.get_e()
    # cf.get_t()