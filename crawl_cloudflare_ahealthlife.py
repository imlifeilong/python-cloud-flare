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
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


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
    def __init__(self):
        super(CloudFlareCrawl, self).__init__()
        self.session = requests.Session()
        self.scraper = cfscrape.create_scraper(sess=self.session)
        self.config =  os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        # self.sockets = self.get_config('socket')
        self.proxies = self.get_config('proxy')
        self.agents = self.get_config('agent')
        self.url = 'https://ahealthlife.net/'
    
    @retry
    def crawl(self, n):
        payload = {}
        payload['headers'] = {'User-Agent': self._random(self.agents)}
        proxy = self._random(self.proxies)
        payload['proxies'] = {'http': 'http://%s' % proxy}
        payload['timeout'] = 20

        r = self.scraper.get(self.url, **payload)
        self.is_ok(r, proxy)

    def is_ok(self, response, proxy):
        if response.ok and response.status_code == 200:
            print('[%s] Access to success: %s' % (proxy, self.url))
        else:
            print('[%s] Access failure: %s, %s' % (proxy, self.url, response.status_code))

    def is_file(self, filename):
        return os.path.exists(filename) and os.path.isfile(filename)

    def is_path(self, pathname):
        return os.path.exists(pathname) and os.path.isdir(pathname)

    def _random(self, data):
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

    # def process(self):
    #     max_process = 4
    #     pool = ProcessPoolExecutor(max_workers=max_process)
    #     result = list(pool.map(self.thread, [i for i in range(max_process)]))


    def thread(self):
        # 线程数
        max_thread = 10
        pool = ThreadPoolExecutor(max_workers=max_thread)
        pool.map(self.crawl, (i for i in range(max_thread)))

    def start(self):
        self.thread()


# def main(argv):
#     try:
#         opts, args = getopt.getopt(argv, 'hu:m:P:T:_', ['help', 'url=', 'method=', 'process=', 'thread=', '_='])
#         print(opts, args)
#     except getopt.GetoptError as e:
#         print(e)
#         showUsage()
#         sys.exit(2)
#     url, method, max_process, max_thread = '', 'get', 1, 1
#     for opt, arg in opts:
#         if opt in ('-h', '--help'):
#             showUsage()
#             sys.exit(2)
#         elif opt in ('-u', '--url'):
#             if isinstance(arg, str):
#                 url = arg
#             else:
#                 print('Parameter [--url] must be a string and not to be empty!')
#                 sys.exit(2)
#         elif opt in ('-m', '--method'):
#             method = arg
#         elif opt in ('-P', '--process'):
#             arg = int(arg)
#             if isinstance(arg, int) and arg > 0:
#                 max_process = arg
#             else:
#                 print('Parameter [--process] must be an integer and not to be less than 1')
#                 sys.exit(2)
#         elif opt in ('-T', '--thread'):
#             arg = int(arg)
#             if isinstance(arg, int) and arg > 0:
#                 max_process = arg
#             else:
#                 print('Parameter [--thread] must be an integer and not to be less than 1')
#                 sys.exit(2)
#     print(url, method, max_process, max_thread)


if __name__ == '__main__':
    cf = CloudFlareCrawl()
    cf.start()
