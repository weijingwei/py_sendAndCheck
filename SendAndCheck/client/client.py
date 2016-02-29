from pickle import dumps, loads
from socket import socket, AF_INET, SOCK_STREAM


class TCPClient(object):
    def __init__(self, host, port):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.connect((host, int(port)))

    def __del__(self):
        self.s.close()
    
    '''
    result = TCPClient().send((方法名, 参数), callback)
    '''
    def send(self, params, callback=None):
        self.s.send(dumps(params))
        result = loads(self.s.recv(1024))
        if callback is not None:
#             Thread(target=callback, args=(result,), daemon=True).start()
            callback(result)
        return result