import time


DICT = {}

class Utils(object):
    def deliverItem(self, params):
#         模拟处理业务逻辑消耗的时间
        global DICT
        time.sleep(3)
        DICT = {params:"received"}
        return "send success. -- " + str(params)
    
    def checkItemStatus(self, params):
        global DICT
        if DICT.get(params) is not None and DICT.get(params) == "received":
            return (params, True)
        else:
            return (params, False)
        