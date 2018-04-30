# -*- coding: utf-8 -*-

from Reversi import Reversi
import Reversi_AI 
import re
import random
import string
import json
import pickle
import bz2
import zlib
import discord
import copy
import sys
import os



data={}
games={}
cnfg={"bo0":"×","bo1": "●","bo2": "▲", "bo3":"△", "bo4":"○",
      "space":0 ,"fspace":0,
      "corumn0":"Ａ", "corumn1":"Ｂ","corumn2":"Ｃ","corumn3":"Ｄ","corumn4":"Ｅ","corumn5":"Ｆ","corumn6":"Ｇ","corumn7":"Ｈ"}
p=re.compile('\<@!?\d{18}>')

def binaryTOstr(binary):
    #print("-----------前---------",binary)
    binary=zlib.compress(binary)
    #print("-----------後---------",binary)
    tostr=",".join(list(map(str,list(binary))))
    return tostr

def strTObinary(string):
    tobyt=list(map(int,string.split(",")))
    tobyt2=b''
    for i in tobyt:
        tobyt2+=i.to_bytes(1, "big")
    tobyt2=zlib.decompress(tobyt2)
    return tobyt2

def save(obj):
    return binaryTOstr(pickle.dumps(obj))

def load(obj):
    return pickle.loads(strTObinary(obj))

def setting(msg):
    error=""
    #メッセージオブジェクト----------------
    message=msg.content
    server=msg.server.id
    channel=msg.channel.id
    author=msg.author.id
    #---------------------------------------
    if "confg" not in games:
        games["confg"]=cnfg
    if server not in games:
        games[server]={}
        data[server]={}
    if channel not in games[server]:
        games[server][channel]={}
        data[server][channel]={}
        games[server][channel]["confg"]={}
        data[server][channel]["confg"]={}
    pass
    
def vs(msg):
    error=""
    #メッセージオブジェクト----------------
    message=msg.content
    server=msg.server.id
    channel=msg.channel.id
    author=msg.author.id
    #---------------------------------------
    #メンションメッセージ
    pls=[str("<@!{}>".format(author))]
    if author=="AI":
        pls=[author]
    #---------------------------------------
    contents=message.split(" ")
    #---------------------------------------
    if not games[server][channel].get("gameflg", False):
        #あれだよ、まずあるかどうかの判別して無かったらデフォでFalse
        if re.match(p, contents[2]) or contents[2]=="AI":
            games[server][channel]["gameflg"]=True
            pls.append(contents[2].replace("<@","<@!"))
            random.shuffle(pls)
            games[server][channel]["game"]=Reversi(pl1=pls[0], pl2=pls[1])
            print(games[server][channel]["game"].playerlist)
            data[server][channel]["game"]=save(games[server][channel]["game"])
            refconfg(games[server][channel])
            error=0
        else:
            error="誰と？"
    else:
        if len(contents) > 3 and contents[3]=="-u":
            
            pls.append(contents[2])
            random.shuffle(pls)
            games[server][channel]["game"]=Reversi(pl1=pls[0], pl2=pls[1])
            data[server][channel]["game"]=save(games[server][channel]["game"])
            refconfg(games[server][channel])
            error=0
        else:    
            error="既にゲームがあります"

    return error

def opengame(msg):
    error=""
    #メッセージオブジェクト----------------
    message=msg.content
    server=msg.server.id
    channel=msg.channel.id
    author=msg.author.id
    #---------------------------------------
    #---------------------------------------
    contents=message.split(" ")
    #---------------------------------------
    if not games[server][channel].get("gameflg", False):
        games[server][channel]["gameflg"]=True
        games[server][channel]["game"]=Reversi(pl0=author)
        data[server][channel]["game"]=save(games[server][channel]["game"])
        refconfg(games[server][channel])
        error=0
    else:
        if len(contents) > 2 and contents[2]=="-u":
            games[server][channel]["game"]=Reversi(pl0=author)
            data[server][channel]["game"]=save(games[server][channel]["game"])
            refconfg(games[server][channel])
            error=0
        
        else:
            error="既にゲームがあります"
        
    return error

def confg(msg):
    error=""
    #メッセージオブジェクト----------------
    message=msg.content #open OR vs B OR vs AI OR confg
    server=msg.server.id
    channel=msg.channel.id
    author=msg.author.id
    #---------------------------------------
    contents=message.split(" ")
    #---------------------------------------
    if len(contents) > 2:
        print(contents[2])
        if contents[2]=="discord":
            contents="osero ::confg bo1=:black_circle\\: bo2=:black_square_button\\: bo3=:white_square_button\\: bo4=:white_circle\\: bo0=:o\\: fspace=1 space=0".split(" ")
            contents.extend(list(str("corumn0=:regional_indicator_a\\:{space} corumn1=:regional_indicator_b\\:{space} corumn2=:regional_indicator_c\\:{space} corumn3=:regional_indicator_d\\:{space} corumn4=:regional_indicator_e\\:{space} corumn5=:regional_indicator_f\\:{space} corumn6=:regional_indicator_g\\:{space} corumn7=:regional_indicator_h\\:{space}".format(space=u"\u200b")).split(" ")))
            print(json.dumps(contents,  sort_keys=True, indent=4, ensure_ascii=False))
        elif contents[2]=="clear":
            contents="osero ::confg space fspace bo0 bo1 bo2 bo3 bo4".split(" ")
        for i in contents[2:]:
            i=i.split("=")
            if i[0] in cnfg:
                 if len(i)<2:
                     games[server][channel]["confg"][i[0]]=None
                     data[server][channel]["confg"][i[0]]=None
                 else:
                     i[1]=i[1].replace("\\","")
                     games[server][channel]["confg"][i[0]]=str(i[1])
                     data[server][channel]["confg"][i[0]]=str(i[1])
        error=json.dumps(games[server][channel]["confg"],  sort_keys=True, indent=4, ensure_ascii=False)
    else:
        error=json.dumps(games[server][channel]["confg"],  sort_keys=True, indent=4, ensure_ascii=False)
    return error

def refconfg(obj):
    for i in obj["confg"]:
        obj["game"].edit(**{i:obj["confg"][i]})
    obj["game"].edit(**{"pboard":obj["game"].printboard()})

def rvAI(game):
    return Reversi_AI.rvAI(game)

def game(msg):
    error=""
    #メッセージオブジェクト----------------
    message=msg.content 
    server=msg.server.id
    channel=msg.channel.id
    author=msg.author.id
    #---------------------------------------
    #メンションメッセージ
    pl=str("<@!{}>".format(author))
    print(pl)
    #---------------------------------------
    contents=message.split(" ")
    #---------------------------------------
    #print(games[server][channel]["game"].playerlist[games[server][channel]["game"].f])
    if games[server][channel].get("gameflg", False):
        if games[server][channel]["game"].playerlist[games[server][channel]["game"].f]=="AI":
                #AIの番
                key=rvAI(games[server][channel]["game"])
                #print(key)
                if key!="error":
                    error=games[server][channel]["game"].gaming(input_key=key)
                else:
                    games[server][channel]["game"].board_check()
                    error=games[server][channel]["game"].result()
                if error=="":
                    error=1 
        elif games[server][channel]["game"].playerlist[games[server][channel]["game"].f] == pl or games[server][channel]["game"].playerlist[1]=="先攻":
            key=contents[1][2:]
            #print(key)
            error=games[server][channel]["game"].gaming(input_key=key)
            #print(games[server][channel]["game"].playerlist)
            if error=="":
                error=1
        else:
            error="貴方の番ではありません\n"+"今の順番:"+games[server][channel]["game"].playerlist[games[server][channel]["game"].f]+"／貴方:"+pl
    else:
        error="ゲームがありません"
    return error

def aimove(msg):
    error=""
    #メッセージオブジェクト----------------
    message=msg.content 
    server=msg.server.id
    channel=msg.channel.id
    author=msg.author.id
    #---------------------------------------
    if games[server][channel]["game"].playerlist[games[server][channel]["game"].f]=="AI":
        #print("aimove")
        error=game(msg)
    return error

async def game_save(msg):
    await client.create_channel("386171440266870784",msg.channel.id)
    pass

def game_load(msg):
    
    pass

def commands(msg):
    error=""
    if msg.content.startswith("osero ::"):
        setting(msg)
        contents=msg.content.replace("osero ::","")
        #コマンド
        if contents.startswith("vs"):
            error=vs(msg)
        elif contents.startswith("open"):
            error=opengame(msg)
        elif contents.startswith("confg"):
            error=confg(msg)
        elif contents.startswith("print"):
            error=str("[\'{0}':[\'{1}\':[\'game\':{2}]]]".format(msg.server.id,msg.channel.id,data[msg.server.id][msg.channel.id]["game"]))
            error=error.replace("[","{")
            error=error.replace("]","}")
            print("data:\n",data,"\ngame:\n",game)
        elif re.match("^[a-h][0-7]",contents):
            print("key受付")
            error=game(msg)
        elif contents.startswith("help"):
            with open('help.txt', 'r', encoding="utf-8") as file:
                read=file.read()
            error=read
        elif contents.startswith("save"):
            error=game_save(msg)
        elif contents.startswith("load"):
            error=game_load(msg)
        else:
            pass

        #後処理
        if error=="":
            error="error"
        elif error==0:
            error="ゲームを開始しました\n"
            error+=games[msg.server.id][msg.channel.id]["game"].pboard
            #次がAIかどうか
            #print(aimove(msg))
            aiflg=aimove(msg)
            while aiflg==1:
                #print("------------------------------")
                error+="\nゲームが進行\n"+games[msg.server.id][msg.channel.id]["game"].pboard
                #print("\nゲームが進行\n"+games[msg.server][msg.channel]["game"].pboard)
                aiflg=aimove(msg)
            print(aiflg)
            print(str(aiflg))
            if str(aiflg).startswith("---リザルト"):
                error+="\n"+aiflg
            
        elif error==1:
            error="ゲームが進行\n"
            error+=games[msg.server.id][msg.channel.id]["game"].pboard
            print(error)
            #次がAIかどうか
            while aimove(msg)==1:
                error+="\nゲームが進行\n"+games[msg.server.id][msg.channel.id]["game"].pboard
    return error

#Discord 関連
client = discord.Client()

@client.event
async def on_ready():
    print('------')
    print('Logged in as')
    print("ユーザー名:",client.user.name)
    print("ユーザーID:",client.user.id)
    print('------')
    

    
@client.event
async def on_message(message):
    msg=message
    error=""
    error=commands(msg)
    if error!="":
        try:
            await client.send_message(msg.channel, error)
        except discord.errors.HTTPException:
            print("えらー！！！\n",error)
            escape_from_error=error.split("ゲームが進行")
            for i in escape_from_error:
                await client.send_message(msg.channel, "ゲームが進行"+i)

        
        
client.run(os.environ['token'])



#------------ゴミ置き場--------------------#
