"""
    <TODO> 自造轮子
    <TODO> 实现动态监控
    Cambot::ArcaeaMoniter_Simple 
"""

import telepot,telepot.aio
import os,sys,time,json,logging,asyncio
import Modules.arcaea.api as arc

arc_pool = {}
async def register(msg, *args, **kwargs):
    chatid,msgid,command = \
    msg['chat']['id'],msg['id'],msg['text']
    if chatid < 0: return "请不要在群组里登记你的信息\n如需向本bot注册请在私聊里发送"
    try:
        if command[0] == 'basic' and len(command) == 3:
            inst = arc.Data(cred=command[1],pswd=command[2])
            arc_pool[chatid]=inst
            pass
        elif command[0] == 'bearer' and len(command) == 2:
            pass
        else: return "指令格式不合法"
    except invalidCredException: return "id或者密钥不正确"
    except 
    return "**非常重要的信息**\n\n这个bot所使用的api是从lowiro网站上扒下来的\nlowiro官方未公布这个api\n过度使用有各种风险(我也不知道有什么)\n基于MIT协议(口胡)，开发者不对使用bot产生的后果负责\n如理解则请按照下文方法操作：\n1./register basic <your_id> <password>\n2./register bearer <your_auth>\n\n\n本Bot不会保存上述basic方法的id和密码\n当auth过期时请重新执行一遍这个方法"
    pass
async def show(msg, *args, **kwargs):
    pass
def about():
    pass
def start(msg):
    return 
async def msgHandler(msg):
    #See https://core.telegram.org/bots/api
    try:
        chatid,msgid,command = \
        msg['chat']['id'],msg['id'],msg['text']
    except KeyError:
        return
    if command[0] is not '/': return #非指令退出
    Command = command[1:].split(' ')
    if Command[0] is 'register': reply = await register(msg,command=Command)
    Bot.sendMessage(text=reply,chatid=chatid,reply_to_message_id=msgid)

token = sys.argv[1]
Bot = telepot.aio.Bot(token)
loop = asyncio.get_event_loop()
loop.create_task(telepot.loop.MessageLoop(Bot,handle=msgHandler).run_forever())
loop.run_forever()