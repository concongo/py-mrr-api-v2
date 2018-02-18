# -*- coding: utf-8 -*-
import hmac
import hashlib
import time
import urllib
import urllib2
import json
import sys
from pprint import pprint

__author__ = 'concongo'
__version__ = '0.1.0'

class mrr_api:

    __api_key = ''
    __api_secret = ''
    __nonce_v = ''
    __api_base = 'https://www.miningrigrentals.com/api/v2'
    
    # Init class
    def __init__(self, api_key, api_secret):
        self.__api_key = api_key
        self.__api_secret = api_secret
        
    #get timestamp as nonce
    def __nonce(self):
        self.__nonce_v = '{:.10f}'.format(time.time() * 1000).split('.')[0]
        
    def __signature(self, end_point):
        
        self.__nonce()
        string = self.__api_key+str(self.__nonce_v)+end_point
        signature = hmac.new(self.__api_secret, string, digestmod=hashlib.sha1).hexdigest()  #create signature

        return signature

    def __post(self, method, end_point, params={}):  #Post Request (Low Level API call)
        #params = urllib.urlencode(param)
        sign = self.__signature(end_point)
        headers = {
            'User-agent': 'Mozilla/4.0 (compatible; MRR API Python client; ' +
                str(sys.platform) + '; ' + str(sys.version).replace('\n', '') +
                ')',
            'x-api-key': self.__api_key,
            'x-api-sign': sign,
            'x-api-nonce': self.__nonce_v
        }
        #print headers
        data = urllib.urlencode(params)
        if len(data) > 0:
            req = urllib2.Request(self.__api_base+end_point+'?'+data, None, headers)
        else:
            req = urllib2.Request(self.__api_base+end_point, None, headers)
        req.get_method = lambda: method
        page = urllib2.urlopen(req).read()
        return page
        
    def api_call(self, method, end_point, param={}):  # api call (Middle level)
        answer = self.__post(method, end_point, param)  #Post Request
        return json.loads(answer) # generate dict and return  
        
    def getbalance(self):
        return self.api_call('GET','/account/balance')
        
    def gettransactions(self,q):
        res = self.api_call('GET','/account/transactions')
        return res["data"]["transactions"][:q]

    def getalgos(self):
        return self.api_call('GET','/info/algos')
        
    def getpools(self):
        return self.api_call('GET','/account/pool')
        
    def getrigmine(self): #get info about the rig
        return self.api_call('GET','/rig/mine')
        
    def getrigminehash(self): #get info about the rig
        return self.api_call('GET','/rig/mine',{'hashrate':'true'})   