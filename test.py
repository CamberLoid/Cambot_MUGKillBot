import requests,requests_oauthlib
import asyncio,sys,os
from pprint import pprint
from base64 import b64encode,b64decode
import json
arcauth = "https://arcapi.lowiro.com/4/auth/login"
arcapi = "https://arcapi.lowiro.com/4/user/me"
async def getAuth(cred,pswd):
    toencode = cred+":"+pswd
    headers = {
          'Authorization': 'Basic ' + b64encode(
              toencode.encode('ascii')).decode(),
          'DeviceId': 'web',
          'AppVersion': 'web'
        }
    po = requests.post(arcauth,headers=headers)
    po.raise_for_status
    if po.json()['success']==True:  
        return po.json()['access_token']
    else:
        raise 
async def Datafetch(auth):
    headers = {}
    headers["authorization"] = "Bearer "+auth
    r=requests.get(arcapi,headers=headers)
    r.raise_for_status()
    return r.json()
async def getRecent(params=None):
