import time


DICT = {}
class Utils(object):
    def deliverItem(self, params):
#         模拟处理业务逻辑消耗的时间
        try:
            global DICT
            time.sleep(3)
            DICT = {params:"received"}
            return (str(params), True)
        except Exception as e:
            return (str(params), False, e)
    
    def checkItemStatus(self, params):
        global DICT
        try:
            if DICT.get(params) is not None and DICT.get(params) == "received":
                return (params, True)
            else:
                return (params, False)
        except Exception as e:
                return (params, False, e)
        