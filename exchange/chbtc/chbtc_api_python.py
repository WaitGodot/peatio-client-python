import json, urllib2, hashlib,struct,sha,time

class chbtc_api():
    def __init__(self, mykey, mysecret):
        self.mykey    = mykey
        self.mysecret = mysecret

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb   = struct.pack("%ds" % len(aKey), aKey)
        value  = struct.pack("%ds" % len(aValue), aValue)
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()
        
        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value  = struct.pack("%ds" % len(aValue), aValue)
        print value
        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __api_call(self, path, params = ''):
        try:
            SHA_secret = self.__digest(self.mysecret)
            sign = self.__hmacSign(params, SHA_secret)
            reqTime = (int)(time.time()*1000)
            params+= '&sign=%s&reqTime=%d'%(sign, reqTime)
            # url = 'https://trade.chbtc.com/api/' + path + '?' + params
            url = path + '?' + params
            request = urllib2.Request(url)
            response = urllib2.urlopen(request, timeout=2)
            doc = json.loads(response.read())
            return doc
        except Exception,ex:
            print >>sys.stderr, 'chbtc request ex: ', ex
            return None
     def urlencode(self, params):
        keys = params.keys()
        keys.sort()
        query = ''
        for key in keys:
            value = params[key]
            if key != "orders":
                query = "%s&%s=%s" % (query, key, value) if len(query) else "%s=%s" % (key, value)
        return query

API_PATH_DICT = {
    'getAccountInfo': 'https://trade.chbtc.com/api/getAccountInfo',
    'markets': '%s/markets.json',
    'order': 'https://trade.chbtc.com/api/order',
    'k': 'http://api.chbtc.com/data/v1/kline',
    'delete_order': '%s/order/delete.json',
}

class Client():
    def __init__(self, access_key=None, secret_key=None):
        if access_key and secret_key:
            self.auth = chbtc_api(access_key, secret_key)
        else:
            from conf import ACCESS_KEY, SECRET_KEY
            self.auth = chbtc_api(ACCESS_KEY, SECRET_KEY)
    def time(self):
        return time.time();
    def get(self, path, params=None, send=True):
        query = ''
        if params:
            query = urlencode(params);
        SHA_secret = self.__digest(self.mysecret)
        sign = self.__hmacSign(query, SHA_secret)
        reqTime = (int)(time.time()*1000)
        query += '&sign=%s&reqTime=%d'%(sign, reqTime)
        
        apipath = API_PATH_DICT[path];
        url = apipath  + '?' + query
        #send = False
        print(url);
        if send:
            try :
                resp = urllib2.urlopen(url, timeout=60)
                # print resp
                if resp:
                    data = resp.readlines()
                    if len(data):
                        return json.loads(data[0])
                else:
                    print(url)
            except Exception:
                print 'http error!!, url:{0}'.format(url);
                return [];

