"""
    CambotAPI for telegramAPI

    一个极其简单自造的API
    
    基于K.I.S.S.编写
"""
import os,sys,requests,asyncio \
       ,traceback,logging,threading
class bot(object):
    class scheduler(threading.Thread):
        #<TODO>
        pass
    def __init__(self,token):
        try:
            assert token is str
            self._token = token
        except AssertionError:
            #有必要么
            logging.critical("Bot token is not a string")
            pass
        
        