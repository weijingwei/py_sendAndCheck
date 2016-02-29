from collections import OrderedDict
from threading import Thread
import time

from client import TCPClient
from messages import Messages


class EventHandler(object):
    def __init__(self):
        self.dict = OrderedDict()
        self.dict['a'] = False
        self.dict['b'] = False
        self.dict['c'] = False
        self.dict['d'] = False
        self.dict['e'] = False
        self.dict['f'] = False
        self.messages = Messages()
        
#     向服务器发送item
    def send(self):
        for key in self.dict:
            value = self.dict[key]
            if not value:
                self.item = key
                break
        if self.dict[key]:
            return
        host = self.messages.getValue("socket1", "host")
        port = int(self.messages.getValue("socket1", "port"))
        params = (("deliverItem", self.item), self.sendCallBack)
#         检查当前item在服务器的状态，7次
        Thread(target=TCPClient(host, port).send, args=params).start()
        self.check(self.item)
        
    def sendCallBack(self, params):
        if params[1]:
            print("Send", params[0], "成功")
        elif len(params) == 3:
            print("Send", params[0], "出现异常", params[2])
    
#     轮询检查服务器端item的还行状况，7次
    def check(self, item):
        totalTimes = 7
        times = 0
        while times < totalTimes:
            time.sleep(1)
            if self.dict[item]:
                return
            host = self.messages.getValue("socket2", "host")
            port = int(self.messages.getValue("socket2", "port"))
            params = (("checkItemStatus", item), self.checkCallBack)
            Thread(target=TCPClient(host, port).send, args=params).start()
            times += 1
        else:
            print("已经对", item, "发起", totalTimes, "次校验，没有结果. 任务终止.")
        
    def checkCallBack(self, params):
        if params[1]:
            self.dict[params[0]] = params[1]
            print("Check", params[0], "成功。当前队列状态为：", self.dict.items())
            self.send()
        elif len(params) == 3:
            print("Check", params[0], "出现异常：", params[2])
        else:
            print("Check", params[0], "未得到结果")
            
if __name__ == '__main__':
    handler = EventHandler()
    handler.send()