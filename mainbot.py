"""
    <TODO> 自造轮子
    <TODO> 实现动态监控
    Cambot::ArcaeaMoniter_Simple 
"""

import telepot,telepot.aio
from telepot.aio.loop import MessageLoop
import os,sys,time,json,logging,asyncio,traceback
import Modules.arcaea as arc
from botCore import jsonHandle
from pprint import pprint

atBot = "@HikariissoKawaiiBot"
arc_pool = {}
async def register(msg ,*args, **kwargs):
    chatid,msgid,usrid,command = \
    msg['chat']['id'],msg['message_id'],msg['from']['id'],msg['text'].split(' ')
    username = msg['from'].get('username')
    if username == None: username = msg['from']['first_name']
    if chatid < 0: return """请不要在群组里登记你的信息
如需向本bot注册请在私聊里发送"""
    try:
        if command[1] == 'basic' and len(command) == 4:
            inst = arc.api.Data(cred=command[2],pswd=command[3])
            arc_pool[usrid]=inst
            with open('userDatas.json','r+') as f:
                ff=json.load(f)
                for fff in range(0,len(ff)):
                    if ff[fff]['user_id'] == usrid:
                        ff.remove(ff[fff])
                ff.append({'user_id':usrid,
                'username':username,
                "arc_user":inst._arcdisplay_name,
                "arc_id":inst._arcid,
                "bearer":inst._auth,
                'registered_to':None #备用 用于/send
                })
                f.seek(0,0)
                f.truncate()
                json.dump(ff,f)
            return "认证成功，欢迎 {} \n您的bearer auth 为 {}\n可以保存以备后续使用\n需要注意的是一个Telegram用户只能绑定一个Arcaea账户".format(inst._arcdisplay_name,inst._auth)
        elif command[1] == 'bearer' and len(command) == 3:
            inst = arc.api.Data(auth=command[2])
            arc_pool[usrid]=inst
            with open('userDatas.json','r+') as f:
                ff=json.load(f)
                for fff in range(0,len(ff)):
                    if ff[fff]['user_id'] == usrid:
                        ff.remove(ff[fff])
                        break
                ff.append({'user_id':usrid,
                'username':username,
                "arc_user":inst._arcdisplay_name,
                "arc_id":inst._arcid,
                "bearer":inst._auth,
                'registered_to':None})
                f.seek(0,0)
                f.truncate()
                json.dump(ff,f)
            return "认证成功，欢迎 {} \n您的bearer auth 为 {}\n可以保存以备后续使用\n需要注意的是一个Telegram用户只能绑定一个Arcaea账户".format(inst._arcdisplay_name,inst._auth)
    except arc.exceptions.invalidCredException: return "id或者密钥不正确\n{}".format(traceback.format_exc())
    except IndexError:pass
    
    return "**非常重要的信息**\n\n这个bot所使用的api是从lowiro网站上扒下来的\nlowiro官方未公布这个api\n过度使用有各种风险(我也不知道有什么)\n基于MIT协议(口胡)，开发者不对使用bot产生的后果负责\n如理解则请按照下文方法操作：\n1./register basic <your_id> <password>\n2./register bearer <your_auth>\n\n\n本Bot不会保存上述basic方法的id和密码\n当auth过期时请重新执行一遍这个方法"

async def showRecent(msg, *args, **kwargs):
    usrid = msg['from']['id']
    reply = None
    if arc_pool.get(usrid) is not None:
        d=arc_pool.get(usrid)
        return d.getRecent(msg['from']['first_name']+' / ')
    else:
        with open("userDatas.json",'r') as f:
            ff=json.load(f)
            for i in ff:
                if usrid==i['user_id']:
                    d = arc.api.Data(auth=i['bearer'])
                    arc_pool[usrid] = d
                    return d.getRecent(msg['from']['first_name']+' / ')
            return "哎呀找不到你的信息，记得私聊+/register"

def about():
    return """这里是 光酱超可爱 Bot(请不要吐槽头像) 基于MIT协议开源
项目源代码 at https://github.com/CamberLoid/Cambot_MUGKillBot/tree/simple_release, 欢迎各路大佬贡献代码

目前处于alpha测试阶段,只实现了基本功能
电脑开到六点,六点之后（或者抛出了异常）就会退出
"""
def start():
    reply = about()
    return reply
async def msgHandler(msg):
    print(msg['text'])
    reply = 'lol'
    #See https://core.telegram.org/bots/api
    try:
        chatid,msgid,command = \
        msg['chat']['id'],msg['message_id'],msg['text']
    except KeyError:
        print(traceback.format_exc)
        return
    try:
        if command[0] != '/': return #非指令退出
        Command = command.split(' ')
        if Command[0][-len(atBot):] == atBot: Command[0] = Command[0][:-len(atBot)] 
        pprint(Command)
        if Command[0] == '/start': reply = start()
        if Command[0] == '/register': reply = await register(msg,command=Command)
        if Command[0] == '/show': reply = await showRecent(msg)
        print(reply+'\n'+msg['from']['first_name'])
    except: return "不管怎样反正出错了\n{}".format(traceback.format_exc())
    await Bot.sendMessage(text=reply,chat_id=chatid,reply_to_message_id=msgid)

token = sys.argv[1]
Bot = telepot.aio.Bot(token)
loop = asyncio.get_event_loop()
loop.create_task(MessageLoop(Bot,handle=msgHandler).run_forever())
loop.run_forever()