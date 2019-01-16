import requests,requests_oauthlib
import asyncio,sys,os
from pprint import pprint
from base64 import b64encode,b64decode
import json

arcauth = "https://arcapi.lowiro.com/4/auth/login"
arcapi = "https://arcapi.lowiro.com/4/user/me"
def getAuth(cred,pswd):
    toencode = cred+":"+pswd
    headers = {
          'Authorization': 'Basic ' + b64encode(
              toencode.encode('ascii')).decode(),
          'DeviceId': 'web',
          'AppVersion': 'web'
        }
    po = requests.post(arcauth,headers=headers)
    return po
headers = {}
Bearer = sys.argv[1]
headers["authorization"] = "Bearer "+"/6wiU25MYuHR1NvI0wlsq+Ufky13W2C0fh2mblBu7pQ="
r=requests.get(arcapi,headers=headers)
r.raise_for_status()
attr=r.json()

