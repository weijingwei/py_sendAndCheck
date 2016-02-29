
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
        host = self.messages.getValue("socket1", "host")
        port = int(self.messages.getValue("socket1", "port"))
        params = (("deliverItem", self.item), self.sendCallBack)
#         检查当前item在服务器的状态
        Thread(target=TCPClient(host, port).send, args=params).start()
        Thread(target=self.check, args=(self.item,)).start()
        
    def sendCallBack(self, params):
        print("sendCallBack:", str(params))
    
#     轮询检查服务器端item的还行状况
    def check(self, item):
        times = 0
        while times < 7:
            time.sleep(1)
            if self.dict[item]:
                return
            host = self.messages.getValue("socket2", "host")
            port = int(self.messages.getValue("socket2", "port"))
            params = (("checkItemStatus", item), self.checkCallBack)
            Thread(target=TCPClient(host, port).send, args=params).start()
#             TCPClient(host, port).send(("checkItemStatus", item), self.checkCallBack)
            times += 1
        
    def checkCallBack(self, params):
        print("checkCallBack:-----------", str(params[0]) ,str(params[1]))
        if params[1]:
            self.dict[params[0]] = params[1]
            print(self.dict.items())
            self.send()
            
if __name__ == '__main__':
    handler = EventHandler()
    handler.send()