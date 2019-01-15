import requests,requests_oauthlib
import asyncio,sys,os
from pprint import pprint
import json
arcapi = "https://arcapi.lowiro.com/4/user/me"
headers = {}
Bearer = sys.argv[1]
headers["authorization"] = "Bearer "+"/6wiU25MYuHR1NvI0wlsq+Ufky13W2C0fh2mblBu7pQ="

r=requests.get(arcapi,headers=headers)
try:
    r.raise_for_status()
    attr=r.json()