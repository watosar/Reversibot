import copy


def rvAI(game):
    choselist=[]
    for i in game.afplcheck():
        AI=copy.deepcopy(game)
        AI.gaming2(i)
        choselist.append(len(AI.afplcheck()))
        AI=None

    
    if len(choselist)>0:
        key=game.afplcheck()[random.choice([j for j, x in enumerate(choselist) if x == max(choselist)])]
        #選択肢の増減を見る。
        #選択肢の減少が最も少ないkeyを選択してretuen
        #print(key)
        input_key=str(list(["a","b","c","d","e","f","g","h"])[key[0]])+str(key[1])
        #print("input_key:\n",input_key)
    else:
        input_key="error"
    return input_key
