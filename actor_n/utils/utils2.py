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
    res = [0] * 33 # Bomb (5 + 13 + 1 + 1)? StraighFlush (10 + 1 + 1) ? JokerBomb (1)
    if action == None or action[0] == 'PASS':
        return res
    if action[0] == 'StraightFlush':
        res[CardLevelToNum[action[1]] + 17] = 1
        if CardLevelToNum[action[1]] == level:
            res[30] = 1
        for card in action[2]:
            if card == 'H' + CardNumToLevel[level]:
                res[31] += 1
    elif action[0] == 'Bomb':
        if action[1] == 'JOKER':
            res[32] = 1
        else:
            bomb_length = min(len(action[2]), 8)
            res[bomb_length - 4] = 1
            res[CardLevelToNum[action[1]] + 4] = 1
            if CardLevelToNum[action[1]] == level:
                res[18] = 1
            for card in action[2]:
                if card == 'H' + CardNumToLevel[level]:
                    res[19] += 1
    return res
