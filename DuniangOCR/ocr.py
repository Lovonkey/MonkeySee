# coding=utf-8

import sys
import json
import base64
import requests
import ssl

# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 防止https证书校验不正确
ssl._create_default_https_context = ssl._create_unverified_context

""" OCR_URL """
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice"

"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'

""" 获取token """
def fetch_token(client_id="", client_secret=""):
    params = {'grant_type': 'client_credentials',
              'client_id': client_id,
              'client_secret': client_secret}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        result = json.loads(result_str)
        if ('access_token' in result.keys() and 'scope' in result.keys()):
            if not 'brain_all_scope' in result['scope'].split(' '):
                print ('please ensure has check the ability')
            return result['access_token']
        else:
            print ('please overwrite the correct API_KEY and SECRET_KEY')
    except URLError as err:
        print(err)
    return ""

""" 读取文件 """
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()

class ocr(object):
    def __init__(self):
        self.dict={"x":""}

    def install(self, API_KEY='', SECRET_KEY=''):
        s = fetch_token(client_id = API_KEY, client_secret = SECRET_KEY)
        if not s == "":
            self.image_url = OCR_URL + "?access_token=" + s
            self.headers = {'content-type': 'application/x-www-form-urlencoded'}
            return True

        return False
            
    def get(self, file=""):
        file_content =	 read_file(file)
        data = urlencode({'image': base64.b64encode(file_content)})
        response  = requests.post(self.image_url, data = data, headers = self.headers)
        result_json = response.json()
        try:
            words_result = result_json["words_result"]
            key = words_result["InvoiceNum"] + words_result["InvoiceCode"]
            if not key in self.dict:
                self.dict[key] = file
                return ("success", words_result)
            else:
                return("same", self.dict[key])
        except:
            return ("failed", None)

if __name__ == '__main__':
    API_KEY = ''
    SECRET_KEY = ''
    ocr = ocr(API_KEY, SECRET_KEY)
    words_result = ocr.get("../xxx.JPG")
    SellerName=words_result["SellerName"]
    print(SellerName)