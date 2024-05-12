from typing import List, Optional
from collections import Counter

import numpy as np

CardToNum = {
    'H2':0, 'H3':1, 'H4':2, 'H5':3, 'H6':4, 'H7':5, 'H8':6, 'H9':7, 'HT':8, 'HJ':9, 'HQ':10, 'HK':11, 'HA':12,
    'S2':13, 'S3':14, 'S4':15, 'S5':16, 'S6':17, 'S7':18, 'S8':19, 'S9':20, 'ST':21, 'SJ':22, 'SQ':23, 'SK':24, 'SA':25,
    'C2':26, 'C3':27, 'C4':28, 'C5':29, 'C6':30, 'C7':31, 'C8':32, 'C9':33, 'CT':34, 'CJ':35, 'CQ':36, 'CK':37, 'CA':38,
    'D2':39, 'D3':40, 'D4':41, 'D5':42, 'D6':43, 'D7':44, 'D8':45, 'D9':46, 'DT':47, 'DJ':48, 'DQ':49, 'DK':50, 'DA':51,
    'SB':52, 'HR':53
}

CardLevelToNum = {
    '2' : 1, '3' : 2, '4' : 3, '5' : 4, '6' : 5, '7' : 6, '8' : 7, '9' : 8, 'T' : 9, 'J' : 10, 'Q' : 11, 'K' : 12,
    'A' : 13, 'B' : 14, 'R': 15
}

CardNumToLevel = {
    1 : '2', 2 : '3', 3 : '4', 4 : '5', 5 : '6', 6 : '7', 7 : '8', 8 : '9', 9 : 'T', 10 : 'J', 11 : 'Q',
    12 : 'K', 13 : 'A', 14 : 'B', 15 : 'R'
}

def heartLevelCardNum(cardList : List, level : int) -> int:
    assert len(cardList) == 54
    return cardList[level - 1]

def removeLevelHeartList(cardList : List, level : int, num_remove : int) -> List:
    assert len(cardList) == 54
    res = cardList.copy()
    res[level - 1] -= num_remove
    res[level - 1] = max(0, res[level - 1])
    return res

def cardNumSum(hiddenCards : List) -> List:
    res = [0] * 15 # 2 ... K - A - SB - HR
    for i in range(13):
        for j in range(4):
            res[i] += hiddenCards[i + j * 13]
    res[13] += hiddenCards[52]
    res[14] += hiddenCards[53]
    return res

def extractCardWithDecor(hiddenCards : List, decor : str) -> List:
    temp = [0] * 13 # A ... Q, K
    for i in range(13):
        if decor == 'H':
            temp[i] = hiddenCards[i]
        elif decor == 'S':
            temp[i] = hiddenCards[i + 13]
        elif decor == 'C':
            temp[i] = hiddenCards[i + 26]
        elif decor == 'D':
            temp[i] = hiddenCards[i + 39]
    res = [temp[-1]] + temp.copy()[0:12]
    return res

def convertCNS(cNS : List) -> List:
    assert len(cNS) == 15
    numA = cNS[12]
    res = [numA] + cNS.copy()[0:12]
    return res

def hasStraightFrom(cNS : List, index : int, remain : int, heart_level_num : int) -> bool:
    if remain == 0:
        return True
    if cNS[index] == 0:
        if heart_level_num == 0:
            return False
        else:
            return hasStraightFrom(cNS, index + 1, remain - 1, heart_level_num - 1)
    else:
        return hasStraightFrom(cNS, index + 1, remain - 1, heart_level_num)
    
def hasStraightFlushFrom(cNS : List, index : int, remain : int, heart_level_num : int) -> bool:
    if remain == 0:
        return True
    if cNS[index] == 0:
        if heart_level_num == 0:
            return False
        else:
            return hasStraightFlushFrom(cNS, index + 1, remain - 1, heart_level_num - 1)
    else:
        return hasStraightFlushFrom(cNS, index + 1, remain - 1, heart_level_num)
    

def actionEncode(action : Optional[List], level : int) -> List:
    assert len(action) == 3
    res = [0] * 24 # 7 + 15 + 1 + 1
    if action == None or action[0] == 'PASS':
        return res
    if action[0] == 'Single':
        res[0] = 1
    elif action[0] == 'Pair':
        res[1] = 1
    elif action[0] == 'Trips':
        res[2] = 1
    elif action[0] == 'ThreePair':
        res[3] = 1
    elif action[0] == 'ThreeWithTwo':
        res[4] = 1
    elif action[0] == 'TwoTrips':
        res[5] = 1
    elif action[0] == 'Straight':
        res[6] = 1
    res[CardLevelToNum[action[1]] + 6] = 1
    if CardLevelToNum[action[1]] == level:
        res[22] = 1
    for card in action[2]:
        if card == 'H' + CardNumToLevel[level]:
            res[23] += 1
    return res

def actionBombEncode(action : Optional[List], level : int) -> List:
    assert len(action) == 3
    res = [0] * 35 # Bomb (7 + 13 + 1 + 1)? StraighFlush (10 + 1 + 1) ? JokerBomb (1)
    if action == None or action[0] == 'PASS':
        return res
    if action[0] == 'StraightFlush':
        res[CardLevelToNum[action[1]] + 17] = 1
        if CardLevelToNum[action[1]] == level:
            res[32] = 1
        for card in action[2]:
            if card == 'H' + CardNumToLevel[level]:
                res[33] += 1
    elif action[0] == 'Bomb':
        if action[1] == 'JOKER':
            res[34] = 1
        else:
            bomb_length = len(action[2])
            res[bomb_length - 4] = 1
            res[CardLevelToNum[action[1]] + 6] = 1
            if CardLevelToNum[action[1]] == level:
                res[20] = 1
            for card in action[2]:
                if card == 'H' + CardNumToLevel[level]:
                    res[21] += 1
    return res

def possibleCombination(hiddenCards : List, cardNum : int, level : int) -> List:
    res = [] # Pair(15) + Trip(13) + ThreePair(12) + ThreeWithTwo(13) + TwoTrips(13) + Straight(10) 
    # + Bomb(7 * 13) + StraightFlush(10) + JokerBomb(1)
    if cardNum == 1:
        return res
    cNS = cardNumSum(hiddenCards)
    pairList = findAllPair(hiddenCards, cNS, level)
    res.extend(pairList)
    return res

def findAllSingle(cNS : List) -> List:
    res = [0] * 15
    for i in range(15):
        if cNS[i] > 0:
            res[i] = 1
    return res

def findAllPair(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 15 # 2 ... K - A - SB - HR
    if hiddenCards == None:
        return res
    # No heart level card
    for i in range(15):
        if cNS[i] >= 2:
            res[i] = 1
    # Have 1 heart level card
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    if heart_level_num >= 1:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 1
        for i in range(13):
            if cNS2[i] >= 1:
                res[i] = 1
    return res

def findAllTrip(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 13
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    for i in range(13):
        if cNS[i] >= 3:
            res[i] = 1
    if heart_level_num == 2:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 2
        for i in range(13):
            if cNS[i] >= 1:
                res[i] = 1
    if heart_level_num == 1:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 1
        for i in range(13):
            if cNS[i] >= 2:
                res[i] = 1    
    return res

def findAllThreePair(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 12
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    for i in range(12):
        if cNS[i] >= 2 and cNS[i+1] >= 2 and cNS[(i+2) % 13] >= 2:
            res[i] = 1
    if heart_level_num == 2:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 2
        for i in range(12):
            if cNS[i] >= 2 and cNS[i+1] >= 1 and cNS[(i+2) % 13] >= 1:
                res[i] = 1
            elif cNS[i] >= 1 and cNS[i+1] >= 2 and cNS[(i+2) % 13] >= 1:
                res[i] = 1
            elif cNS[i] >= 1 and cNS[i+1] >= 1 and cNS[(i+2) % 13] >= 2:
                res[i] = 1
    elif heart_level_num == 1:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 1
        for i in range(12):
            if cNS[i] >= 2 and cNS[i+1] >= 2 and cNS[(i+2) % 13] >= 1:
                res[i] = 1
            elif cNS[i] >= 1 and cNS[i+1] >= 2 and cNS[(i+2) % 13] >= 2:
                res[i] = 1
            elif cNS[i] >= 2 and cNS[i+1] >= 1 and cNS[(i+2) % 13] >= 2:
                res[i] = 1
    return res

def findAllThreeWithTwo(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 13
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    for i in range(13):
        if cNS[i] >= 3:
            for j in range(15):
                if i != j and cNS[j] >= 2:
                    res[i] = 1
                    break
    if heart_level_num == 1:
        cNS1 = cNS.copy()
        cNS1[level - 1] -= 1
        for i in range(13):
            if cNS1[i] >= 2:
                for j in range(15):
                    if i != j and cNS1[j] >= 2:
                        res[i] = 1
                        break
        for i in range(13):
            if cNS1[i] >= 3:
                for j in range(15):
                    if (j < 13 and i != j and cNS1[j] >= 1) or (j >= 13 and cNS1[j] == 2):
                        res[i] = 1
                        break
    elif heart_level_num == 2:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 2
        for i in range(13):
            if cNS2[i] >= 1:
                for j in range(15):
                    if (i != j and cNS2[j] >= 2):
                        res[i] = 1
                        break
        for i in range(13):
            if cNS2[i] >= 2:
                for j in range(15):
                    if (j < 13 and i != j and cNS2[j] >= 1) or (j >= 13 and cNS2[j] == 2):
                        res[i] = 1
                        break
    return res

def findAllTwoTrips(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 13
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    for i in range(13):
        if cNS[i] >= 3 and cNS[(i+2) % 13] >= 3:
            res[i] = 1
    if heart_level_num == 2:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 2
        for i in range(13):
            if cNS[i] >= 3 and cNS[(i+2) % 13] >= 1:
                res[i] = 1
            elif cNS[i] >= 1 and cNS[(i+2) % 13] >= 3:
                res[i] = 1
            elif cNS[i] >= 2 and cNS[(i+2) % 13] >= 2:
                res[i] = 1
    if heart_level_num == 1:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 1
        for i in range(13):
            if cNS[i] >= 3 and cNS[(i+2) % 13] >= 2:
                res[i] = 1
            elif cNS[i] >= 2 and cNS[(i+2) % 13] >= 3:
                res[i] = 1
    return res

#Include StraightFlush
def findAllStraight(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 10
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    if heart_level_num == 0:
        convertCNS = convertCNS(cNS)
        for i in range(10):
            res[i] = 1 if hasStraightFrom(convertCNS, i, 5, 0) else 0
    elif heart_level_num == 2:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 2
        convertCNS2 = convertCNS(cNS2)
        for i in range(10):
            res[i] = 1 if hasStraightFrom(convertCNS2, i, 5, 2) else 0
    elif heart_level_num == 1:
        cNS1 = cNS.copy()
        cNS1[level - 1] -= 1
        convertCNS1 = convertCNS(cNS1)
        for i in range(10):
            res[i] = 1 if hasStraightFrom(convertCNS1, i, 5, 1) else 0
    return res

def findAllBomb(hiddenCards : Optional[List], cNS : List, level : int) -> List:
    res = [0] * 91
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    if heart_level_num == 1:
        cNS1 = cNS.copy()
        cNS1[level - 1] -= 1
    if heart_level_num == 2:
        cNS2 = cNS.copy()
        cNS2[level - 1] -= 2
    for size in range(4, 9):
        for i in range(13):
            if heart_level_num == 0:
                res[i + (size - 4) * 13] = 1 if cNS[i] >= size else 0
            elif heart_level_num == 1:
                res[i + (size - 4) * 13] = 1 if cNS1[i] >= size - 1 else 0
            elif heart_level_num == 2:
                res[i + (size - 4) * 13] = 1 if cNS2[i] >= size - 2 else 0
    if heart_level_num == 1:
        for i in range(13):
            res[i + 65] = 1 if cNS1[i] == 8 else 0
    if heart_level_num == 2:
        for i in range(13):
            res[i + 78] = 1 if cNS2[i] == 8 else 0
    return res

def findAllStraightFlush(hiddenCards : Optional[List], level : int) -> List:
    res = [0] * 10
    if hiddenCards == None:
        return res
    heart_level_num = heartLevelCardNum(hiddenCards, level)
    if heart_level_num == 0:
        for i in range(10):
            res[i] = 1 if hasStraightFlushFrom(extractCardWithDecor(hiddenCards, 'H'), i, 5, 0) \
                or hasStraightFlushFrom(extractCardWithDecor(hiddenCards, 'S'), i, 5, 0) \
                    or hasStraightFlushFrom(extractCardWithDecor(hiddenCards, 'C'), i, 5, 0) \
                        or hasStraightFlushFrom(extractCardWithDecor(hiddenCards, 'D'), i, 5, 0) else 0
    elif heart_level_num == 1:
        cardList1 = removeLevelHeartList(hiddenCards, level, 1)
        for i in range(10):
            res[i] = 1 if hasStraightFlushFrom(extractCardWithDecor(cardList1, 'H'), i, 5, 1) \
                or hasStraightFlushFrom(extractCardWithDecor(cardList1, 'S'), i, 5, 1) \
                    or hasStraightFlushFrom(extractCardWithDecor(cardList1, 'C'), i, 5, 1) \
                        or hasStraightFlushFrom(extractCardWithDecor(cardList1, 'D'), i, 5, 1) else 0
    elif heart_level_num == 2:
        cardList2 = removeLevelHeartList(hiddenCards, level, 2)
        for i in range(10):
            res[i] = 1 if hasStraightFlushFrom(extractCardWithDecor(cardList2, 'H'), i, 5, 2) \
                or hasStraightFlushFrom(extractCardWithDecor(cardList2, 'S'), i, 5, 2) \
                    or hasStraightFlushFrom(extractCardWithDecor(cardList2, 'C'), i, 5, 2) \
                        or hasStraightFlushFrom(extractCardWithDecor(cardList2, 'D'), i, 5, 2) else 0
    return res

def findJokerBomb(cardNumSum : List) -> List:
    res = [0] * 1
    res[0] = 1 if cardNumSum[13] + cardNumSum[14] == 4 else 0
    return res