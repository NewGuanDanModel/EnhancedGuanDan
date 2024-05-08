# -*- coding: utf-8 -*-
# @Time       : 2020/10/1 16:30
# @Author     : Duofeng Wu
# @File       : client.py
# @Description:


import json
from ws4py.client.threadedclient import WebSocketClient
from state1 import State1
from action1 import Action1
from state2 import State2
from action2 import Action2
from state4 import State4
from action4 import Action4

import numpy as np


class ExampleClient(WebSocketClient):

    def __init__(self, url):
        super().__init__(url)
        self.state1 = State1("client0")
        self.action1 = Action1("client0")
        self.state2 = State2("client0")
        self.action2 = Action2("client0")
        self.state4 = State4("client0")
        self.action4 = Action4("client0")
        
        

    def opened(self):
        pass

    def closed(self, code, reason=None):
        print("Closed down", code, reason)

    def received_message(self, message):
        message = json.loads(str(message))                                    # 先序列化收到的消息，转为Python中的字典
        self.state1.parse(message)
        self.state2.parse(message)
        self.state4.parse(message)                                            # 调用状态对象来解析状态
        
        
        
        if "actionList" in message:                                           # 需要做出动作选择时调用动作对象进行解析
            random_number = np.random.randint(4, size=1).tolist()[0]
            act_index = 0
            if random_number == 0:
                act_index = self.action1.rule_parse(message,self.state1._myPos,self.state1.remain_cards,self.state1.history,
                                                self.state1.remain_cards_classbynum,self.state1.pass_num,
                                                self.state1.my_pass_num,self.state1.tribute_result)
            elif random_number == 1:
                try:
                    if message["stage"]=="play":
                        act_index = self.action2.GetIndexFromPlay(message, self.state2.retValue)
                    elif message["stage"]=="back":
                        act_index = self.action2.GetIndexFromBack(message, self.state2.retValue)
                    else:
                        act_index = self.action2.parse(message)
                except:
                    act_index = self.action2.parse(message)
            elif random_number == 2:
                act_index = self.action1.rule_parse(message,self.state1._myPos,self.state1.remain_cards,self.state1.history,
                                                self.state1.remain_cards_classbynum,self.state1.pass_num,
                                                self.state1.my_pass_num,self.state1.tribute_result)
            elif random_number == 3:
                act_index = self.action4.rule_parse(message,self.state4._myPos,self.state4.remain_cards,self.state4.history,
                                                self.state4.remain_cards_classbynum,self.state4.pass_num,
                                                self.state4.my_pass_num,self.state4.tribute_result)

            # print(act_index)
            self.send(json.dumps({"actIndex": act_index}))

if __name__ == '__main__':
    try:
        ws = ExampleClient('ws://127.0.0.1:23456/game/client1')

        #ws = ExampleClient('ws://112.124.24.226:80/game/gd/15251763326255578')
        # ws = ExampleClient('ws://101.37.15.53:80/game/gd/15251763326255578')
        ws.connect()
        ws.run_forever()
    except KeyboardInterrupt:
        ws.close()
