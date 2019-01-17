"""
    <TODO> 自造轮子
    <TODO> 实现动态监控
    Cambot::ArcaeaMoniter_Simple 
"""

import telepot,telepot.aio
import os,sys,time,json,logging,asyncio
from Modules import *

async def CommandHandler(msg):
    chatid,userid,command = \
    msg['chat']['id'],msg[''],msg['text']

token = sys.argv[1]
Bot = telepot.aio.Bot(token)
loop = asyncio.get_event_loop()
loop.create_task(telepot.loop.MessageLoop(Bot,handle=CommandHandler).run_forever())
loop.run_forever()