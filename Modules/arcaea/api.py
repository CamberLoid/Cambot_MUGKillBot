import requests,requests_oauthlib
import asyncio,sys,os
from pprint import pprint
from base64 import b64encode,b64decode
from botCore import jsonHandle
import json
arcauth = "https://arcapi.lowiro.com/4/auth/login"
arcapi = "https://arcapi.lowiro.com/4/user/me"
props = json.load(open('arc.json',encoding='UTF-8'))
from . import exceptions
"""
    Cambot.modules.arcaea.api
    模块化bot框架<TODO> Cambot 的音游接入口之一
    大概是我第一个做出来的可自动导入模块
    <TODO>更加完整的url
"""
class Data(object):
    def __init__(self,auth=None,cred=None,pswd=None,**kwargs):
        self._auth = auth
        if self._auth is None:
            self._auth = self.getAuth(cred,pswd)
        raw = self.Datafetch()
        self._arcid = raw['user_code']
        self._arcdisplay_name = raw['display_name']
        #pprint(self.Datafetch())    
    @classmethod
    def getAuth(cls,cred,pswd):
        """
        在没有auth或auth过期的时候，使用该方法获取bearer auth
        该方法不存储用户敏感数据
        """
        toencode = cred+":"+pswd
        headers = {
              'Authorization': 'Basic ' + b64encode(
                  toencode.encode('ascii')).decode(),
              'DeviceId': 'web',
              'AppVersion': 'web'}
        po = requests.post(arcauth,headers=headers)
        po.raise_for_status()
        if po.json()['success']==True:  
            return po.json()['access_token']
        else:
            raise exceptions.invalidCredException()
    def Datafetch(self):
        """
        普通的拉取数据
        """
        headers = {}
        headers["authorization"] = "Bearer "+ self._auth
        r=requests.get(arcapi,headers=headers)
        r.raise_for_status()
        if r.json()['success']==False:
            raise exceptions.badAuthException('Auth is Expired')
        return r.json()['value']
    def getRecent(self,tgUser=None):
        raw=self.Datafetch()
        recent=raw['recent_score'][0]
        reply = \
"""用户 {}{}(Arcaea)
目前PTT为 {}
拉取的最后一次游戏数据为：
{} - {}
Score:    {}
Pure(+1): {}({})
Far:      {}
Lost:     {}""".format(tgUser,raw['display_name'],raw['rating']/100,props['difficulty'][recent['difficulty']],recent['song_id'],recent['score'],recent['perfect_count'],recent['shiny_perfect_count'],recent['near_count'],recent['miss_count'])
        return reply
        
    def getFriendRecent(self,friendID=None):
        raw=self.Datafetch()
        for f in raw['friends']:
            if f['name']==friendID or f['user_id']==friendID:
                recent = f['recent_score'][0]
                reply = \
"""玩家 {}(Arcaea)(好友关系)
目前PTT为 {}
拉取的最后一次游戏数据为：
{} - {}
Score:    {}
Pure(+1): {}({})
Far:      {}
Lost:     {}""".format(f['name'],f['rating']/100,props['difficulty'][recent['difficulty']],recent['song_id'],recent['score'],recent['perfect_count'],recent['shiny_perfect_count'],recent['near_count'],recent['miss_count'])
                return reply
        return "TA还不是你的好友哦，请先加TA为好友"
    def getFriendCode(self):
        return self._arcid
    async def listen(self,timeout=1200):
        pass