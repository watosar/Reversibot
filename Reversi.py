# -*- coding: utf-8 -*-

import random
import string
import re
import unicodedata
import copy

class Reversi:
    
    #定数設定
    space=" "
    s_corumn_ind = ["a" ,"b" ,"c" ,"d" ,"e" ,"f" ,"g" ,"h" ]
    line_ind =map(str, [i for i in range(8)])
    p = re.compile('^[a-h][0-7]$')
    
    def __init__(self, pl0="GM",pl1="先攻",pl2="後攻", bo0="×",bo1= "●",bo2= "▲", bo3="△", bo4="○"):

        #変数設定
        self.spacenum=0
        self.fspacenum=0
        self.corumn_ind = [str(self.space*self.fspacenum),
                      "Ａ",str(self.space*self.spacenum),
                      "Ｂ",str(self.space*self.spacenum),
                      "Ｃ",str(self.space*self.spacenum),
                      "Ｄ",str(self.space*self.spacenum),
                      "Ｅ",str(self.space*self.spacenum),
                      "Ｆ",str(self.space*self.spacenum),
                      "Ｇ",str(self.space*self.spacenum),
                      "Ｈ"]
        self.playerlist=[pl0,pl1,pl2]
        self.chenger=[bo0,bo1,bo2,bo3,bo4]
        self.game_flg=True
        self.msg=""
        self.resultms=None
        self.f=1
        #おける升目リスト
        self.afpl=["hoge",[],[]]
        self.afpl_check=[]
        #初期ボード設定
        self.board=self.create_board()
        
        #初期配置可能取得
        self.f=1
        self.board_check()
        #print(f)
        #print(afpl)
        self.f=-1
        self.board_check()
        self.f=1
        
        self.pboard=self.printboard()
        
        

    #numボード作成(リスト)
    def create_board(self):
        board=[[0 for i in range(8)] for j in range(8)]
        board[3][3]=board[4][4] = -1;
        board[3][4]=board[4][3] = 1;
        
        return board

    #ボード化(リスト)
    def convertboard(self,board):
        def converter(line):
            def change(num):
                return self.chenger[num]
            return list(map(change, line))
        return list(map(converter, board))
                    
    #ボード化
    def joinboard(self,board):
        def joinline(line):
            #print(line)
            return "".join(line)
        strboardl=list(map(joinline, board))
        for ind, line in enumerate(strboardl):
            strboardl[ind]=line+str(ind)
        strboard="".join(self.corumn_ind)+"\n"+"\n".join(strboardl)
        return strboard                

    #ボードプリント処理まとめ
    def printboard(self):
        f=self.f
        #deep copyでないとリストの中が変わらないから汚染される。
        pboard=copy.deepcopy(self.board)
        for i in self.afpl[f]:
            pboard[i[1]][i[0]]=f*2
        pboard=self.convertboard(pboard)
        pboard=self.joinboard(pboard)
        #表示
        pboard=str("＞次は{0}さんの番です\n{1}".format(self.playerlist[f], pboard))
        #print(pboard)
        return pboard

    #ボードチェックver2
    def board_check(self):
        f=self.f
        self.afpl[f]=[]
        #ここのネストの深さはどうにかしたい
        for py in range(0, 8):
            pxlist = [i for i, n in enumerate(self.board[py]) if n == -f]
            for px in pxlist:
                for i in range(-1, 2):
                    for j in range(-1 ,2):
                        if  not(i == 0 and j == 0):
                            if 0 <= py+i and py+i <= 7 and 0 <= px+j and px+j <= 7:
                                if self.board[py+i][px+j]==0:
                                    if 0 <= py-i and py-i <= 7 and 0 <= px-j and px-j <= 7:
                                        if self.board[py-i][px-j]==f:
                                            self.afpl[f].append([px+j,py+i,j,i])
                                        elif self.board[py-i][px-j]==-f:
                                            li=i
                                            lj=j
                                            while 0 <= py-li and py-li <= 7 and 0 <= px-lj and px-lj <= 7:
                                                check= self.board[py-li][px-lj]
                                                if check == 0:
                                                    break
                                                elif check == f:
                                                    self.afpl[f].append([px+j, py+i, j,i])
                                                    break
                                                elif check== -f:
                                                    li=li+i
                                                    lj=lj+j
        pass
                                

    #めくり
    def mekuri(self, board, afpl_check ,key):
        f=self.f
        indl=[i for i, j in enumerate(afpl_check) if j == key]
        #print("indl=",indl)
        for ind in indl:
            #print("ind:",ind)
            #print(self.afpl)
            becter=[self.afpl[f][ind][2],self.afpl[f][ind][3]]  
            flipy=key[1]
            flipx=key[0]
            board[flipy][flipx]=f
            #print("becter", becter)
            flipy=flipy-becter[1]
            flipx=flipx-becter[0]
            while 0 <= flipy and flipy <= 7 and 0 <= flipx and flipx <= 7:
                #print("x",flipx,"\ny",flipy)
                if board[flipy][flipx]==f:
                    break
                board[flipy][flipx]=f
                flipy=flipy-becter[1]
                flipx=flipx-becter[0]
        pass
    


    def result(self):
        #リザルト
        line=[]
        for i in self.board:
            line.extend(i)
        #print(line)
        result=[len([i for i in line if i==1]),len([j for j in line if j==-1])]
        #print(str(result[0])+"対"+str(result[1])+"で")
        if result[0] > result[1]:
            #print(playerlist[1]+"の勝ち!")
            self.resultms="先攻："+self.playerlist[1]+"の勝ち!"
        elif result[0] < result[1]:
            #print(playerlist[-1]+"の勝ち!")
            self.resultms="後攻："+self.playerlist[-1]+"の勝ち!"
        else:
            #print("引き分け!")
            self.resultms="引き分け！"
        self.game_flg=False
        self.resultms="---リザルト---\n"+str(result[0])+"対"+str(result[1])+"で\n"+self.resultms
        return self.resultms

    def afplcheck(self):
        f=self.f
        return [list(k) for k in zip([list(i)[0] for i in [i for i in self.afpl[f]]], [list(j)[1] for j in [i for i in self.afpl[f]]])]

    def gaming2(self, key):
        #print("--g2--\n afpl_check:",self.afplcheck())
        self.mekuri(self.board ,self.afplcheck() ,key)
        
    def gaming(self, input_key=""):
        f=self.f
        self.msg=""
        if self.game_flg==True:
            #諸々設定
            key = None 
            #print("afpl:",afpl)
            self.afpl_check=self.afplcheck()
            #print(afpl_check)
            if len(self.afpl_check) != 0:
                if (bool(re.match(self.p, input_key))!=True):
                    #print(input_key)
                    self.msg="コマンドのフォーマットが違います"
                    print(input_key)
                else:
                    #print('キーを受け付けました。')
                    key=[i for i in input_key]
                    key[0]=self.s_corumn_ind.index(key[0])
                    key=list(map(int,key))
                    #print(key)
                    #keyは[x,y]
                    if (key not in self.afpl_check):
                        self.msg="そこには置けません"
                        input_key=None
                    else:
                        #めくり
                        self.msg=""
                        self.gaming2(key)
                        self.f=-self.f
                        self.board_check()
                        self.pboard=self.printboard()
                        if len(self.afpl)==0:
                            self.msg=self.result()
            else:
                self.msg="パスだよ"
                print(self.msg)
            

        else:
            self.msg="ゲームは終了しています"

        return self.msg
            
        

        
    def edit(self, **confgkey):
        if "pl0" in confgkey or "pl1"in confgkey or "pl2" in confgkey:
            pl0=confgkey.get("pl0",self.playerlist[0])
            pl1=confgkey.get("pl1",self.playerlist[1])
            pl2=confgkey.get("pl2",self.playerlist[-1])
            self.playerlist=[pl0,pl1,pl2]
        if "bo0"in confgkey or "bo1"in confgkey or"bo2"in confgkey or"bo3"in confgkey or"bo4" in confgkey:
            bo0=confgkey.get("bo0",self.chenger[0])
            bo1=confgkey.get("bo1",self.chenger[1])
            bo2=confgkey.get("bo2",self.chenger[2])
            bo3=confgkey.get("bo3",self.chenger[3])
            bo4=confgkey.get("bo4",self.chenger[4])
            self.chenger=[bo0,bo1,bo2,bo3,bo4]
        if "pboard" in confgkey:
            pboardn=confgkey.get("pboard",self.pboard)
            self.pboard=pboardn
        if "board" in confgkey:
            self.board=confgkey.get("board",self.board)
        if "space" or "fspace" or "corumn0" or "corumn1" or "corumn2" or "corumn3" or "corumn4" or "corumn5" or "corumn6" or "corumn7" in confgkey:
            try:
                self.spacenum=int(confgkey.get("space",self.spacenum))
                self.fspacenum=int(confgkey.get("fspace",self.fspacenum))
            except ValueError:
                self.spacenum=0
                self.fspacenum=0
            self.corumn_ind = [str(self.space*self.fspacenum),
                      confgkey.get("corumn0",self.corumn_ind[1]),str(self.space*self.spacenum),
                      confgkey.get("corumn1",self.corumn_ind[3]),str(self.space*self.spacenum),
                      confgkey.get("corumn2",self.corumn_ind[5]),str(self.space*self.spacenum),
                      confgkey.get("corumn3",self.corumn_ind[7]),str(self.space*self.spacenum),
                      confgkey.get("corumn4",self.corumn_ind[9]),str(self.space*self.spacenum),
                      confgkey.get("corumn5",self.corumn_ind[11]),str(self.space*self.spacenum),
                      confgkey.get("corumn6",self.corumn_ind[13]),str(self.space*self.spacenum),
                      confgkey.get("corumn7",self.corumn_ind[15])]
            print(self.corumn_ind)
        pass
