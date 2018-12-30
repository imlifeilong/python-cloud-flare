# -*- coding: utf-8 -*-
import sys
import hashlib
import hmac
import binascii
import urllib
import requests
import random
import time
import json
import os

# def retry(func):
#     def wrapper(self, *args, **kwargs):
#         flag = True
#         while flag:
#             f = func(self, *args, **kwargs)
#             if f:
#                 flag = False
#                 return f
#             else:
#                 flag = True
#         wrapper.__name__ = wrapper.__name__
#     return wrapper



class EIP():
    def __init__(self, signature_method, secret_id, secret_key):
        self.uri = 'cvm.tencentcloudapi.com'
        self.request_method = 'GET'
        self.signature_method = signature_method
        self.secret_id = secret_id
        self.secret_key = secret_key
        

    def sign(self, secret_key, sign_str, sign_method):
        if sys.version_info[0] > 2:
            sign_str = sign_str.encode('utf-8')
            secret_key = secret_key.encode('utf-8')

        if sign_method.startswith('HmacSHA256'):
            digestmod = hashlib.sha256
        
        elif sign_method.startswith('HmacSHA1'):
            digestmod = hashlib.sha1

        hashed = hmac.new(secret_key, sign_str, digestmod)
        base_str = binascii.b2a_base64(hashed.digest())[:-1]

        return base_str.decode() if sys.version_info[0] > 2 else base_str


    def dict2str(self, data):
        tmp = []
        
        for k, v in data.items():
            tmp.append('%s=%s' % (k, v))

        return '&'.join(tmp)


    def singstr(self, data):
        tmp = []
        result = []
        tmp_dict = {}
        
        for key, value in data.items():
            key_low = key.lower()
            tmp.append(key_low)
            tmp_dict[key_low] = key
        tmp.sort()

        for x in tmp:
            value_str = str(tmp_dict[x]) + '=' + str(data[tmp_dict[x]])
            result.append(value_str)

        return '&'.join(result)


    def get_url(self, region='ap-beijing', action='AllocateAddresses', version='2017-03-12', params={}):
        sign_data = {
            'Action' : action,
            'Nonce' : int(random.random()*10000),
            'Region' : region,
            'SecretId' : self.secret_id,
            'SignatureMethod': self.signature_method,
            'Timestamp' : int(time.time()),
            'Version':version
        }
        sign_data.update(params)
        querystring = "%s%s%s%s%s"%(self.request_method, self.uri, "/", "?", self.singstr(sign_data))
        _sign = urllib.parse.quote(self.sign(self.secret_key, querystring, sign_data['SignatureMethod']))
        sign_data['Signature'] = _sign
        
        return 'https://%s/?%s' % (self.uri, self.dict2str(sign_data))


    def crawl(self, region, action, version, querystring):
        time.sleep(2)
        url = self.get_url(region, action, version, querystring)
        resp = requests.get(url)
        if resp.ok:
            result = json.loads(resp.text)
            if 'Error' in result['Response']:
                print(result['Response']['Error'])
                return
        
            return result
     

    def allocate(self, region, version, address_count=1):
        '''
        创建
        :param region 地域参数
        :param version API 的版本
        :param address_count 申请 EIP 数量，默认值为1
        '''
        querystring = {'AddressCount': address_count}
        result = self.crawl(region, 'AllocateAddresses', version, querystring)
        
        return result

    # @retry
    def associate(self, region, version, address_id, instance_id, *kargs):
        '''
        绑定
        :param region 地域参数
        :param version API 的版本
        :param address_id 标识 EIP 的唯一 ID
        :param instance_id 要绑定的实例 ID
        '''
        querystring = {'AddressId': address_id, 'InstanceId': instance_id}
        querystring.update(kargs)
        result = self.crawl(region, 'AssociateAddress', version, querystring)

        return result

    # @retry
    def disassociate(self, region, version, address_id, *kargs):
        '''
        解绑定
        :param region 地域参数
        :param version API 的版本
        :param address_id 标识 EIP 的唯一 ID
        '''
        querystring = {'AddressId': address_id}
        querystring.update(kargs)
        result = self.crawl(region, 'DisassociateAddress', version, querystring)

        return result
        
    # @retry
    def release(self, region, version, address_id, *kargs):
        '''
        释放
        :param region 地域参数
        :param version API 的版本
        :param address_id 标识 EIP 的唯一 ID
        '''
        querystring = {'AddressIds.0': address_id}
        querystring.update(kargs)
        result = self.crawl(region, 'ReleaseAddresses', version, querystring)

        return result

    def describe_addresses(self, region, version, address_id=None, *kargs):
        '''
        查询
        :param region 地域参数
        :param version API 的版本
        :param address_id 标识 EIP 的唯一 ID
        '''
        querystring = {}
        if address_id:
            querystring = {'AddressIds.0': address_id}
        querystring.update(kargs)
        result = self.crawl(region, 'DescribeAddresses', version, querystring)

        return result

    def parse_instance_id(self, address):
        '''
        获取实例旧EIP
        '''
        # address = {'Response': {'TotalCount': 2, 'AddressSet': [{'AddressType': 'EIP', 'NetworkInterfaceId': None, 'AddressStatus': 'CREATING', 'InstanceId': 'ins-1qaz3ee', 'IsEipDirectConnection': False, 'AddressName': None, 'IsBlocked': False, 'CascadeRelease': False, 'IsArrears': False, 'CreatedTime': '2018-11-30T12:34:41Z', 'AddressIp': None, 'AddressId': 'eip-12fjad4y', 'PrivateAddressIp': None}, {'AddressType': 'EIP', 'NetworkInterfaceId': None, 'AddressStatus': 'UNBIND', 'InstanceId': 'ins-1dwsdw', 'IsEipDirectConnection': False, 'AddressName': None, 'IsBlocked': False, 'CascadeRelease': False, 'IsArrears': False, 'CreatedTime': '2018-11-30T12:27:21Z', 'AddressIp': '119.29.83.148', 'AddressId': 'eip-83gronj6', 'PrivateAddressIp': None}], 'RequestId': 'e617b011-7ef1-431c-bbf8-3db210ca03fa'}}
        # address = {'Response': {'TotalCount': 1, 'AddressSet': [{'IsArrears': False, 'AddressIp': '129.204.46.160', 'AddressId': 'eip-jq8das9y', 'NetworkInterfaceId': None, 'InstanceId': 'ins-1qaz3ee', 'CascadeRelease': False, 'AddressName': None, 'CreatedTime': '2018-12-03T02:06:57Z', 'AddressStatus': 'UNBIND', 'IsEipDirectConnection': False, 'AddressType': 'EIP', 'IsBlocked': False, 'PrivateAddressIp': None}], 'RequestId': '496c5ba3-7577-400d-a62f-681bc8af15a2'}}
        instance_dict = {}
        for x in address['Response']['AddressSet']:
            instance_dict[x['InstanceId']] = (x['AddressId'], x['AddressIp'])

        return instance_dict


    def get_instances(self):
        instances = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instances')
        if os.path.exists(instances):
            with open(instances, 'r') as f:
                instances_ids = f.read().splitlines()
            return instances_ids
        else:
            print('实例配置文件不存在')

    def start(self, region, version):
        instances = self.get_instances()
        if instances:
            # 获取eip列表
            address = self.describe_addresses(region, version)
            instances_ids = self.parse_instance_id(address)
            for ins in instances:
                ins = ins.strip()
                
                # 申请eip
                eips = self.allocate(region, version)
                if not eips:
                    raise ('申请失败')
                new_eip = eips['Response']['AddressSet'][0]
                tmp = self.describe_addresses(region, version, address_id=new_eip)
                if tmp:
                    new_address = tmp['Response']['AddressSet'][0]['AddressIp']
                
                if ins in instances_ids:
                    old_eip = instances_ids[ins][0]
                    with open('result.txt', 'w') as f:
                        print('Instance: %s, Old_eip: %s, New_eip: %s' % (ins, instances_ids[ins][1], new_address), file=f)
                    # 解绑定旧的 EIP
                    resp = self.disassociate(region, version, old_eip)
                    if not resp:
                        raise ('解绑定失败')

                    # 绑定
                    inst = self.associate(region, version, new_eip, ins)
                    if not inst:
                        raise ('绑定失败')

                    # 释放旧EIP
                    rele = self.release(region, version, old_eip)
                    if not rele:
                        raise ('释放失败')
                    print('----替换成功----')
                else:
                    print('没有该实例: %s, 释放新EIP: %s' % (ins, new_eip))
                    self.release(region, version, new_eip)


if __name__ == '__main__':
    '''
    使用前需安装requests pip install requests
    https://console.cloud.tencent.com/capi获取secret_id和secret_key
    '''
    signature_method = 'HmacSHA256'
    secret_id = ''
    secret_key = ''
    eip = EIP(signature_method, secret_id, secret_key)
    # rele = eip.disassociate('ap-guangzhou', '2017-03-12', 'eip-8zb79m00')
    # rele = eip.associate('ap-guangzhou', '2017-03-12', 'eip-5frnvydc', 'ins-nso05olk')
    # eip.associate('ap-guangzhou', '2017-03-12', '')
    rele = eip.start('ap-guangzhou', '2017-03-12')
    # rele = eip.describe_addresses('ap-guangzhou', '2017-03-12', 'eip-jq8das9y')
    # rele = eip.disassociate('ap-guangzhou', '2017-03-12', 'eip-jq8das9y')
    print(rele)