from pickle import loads, dumps
from socketserver import BaseRequestHandler, ThreadingTCPServer
from threading import Thread


class EchoRequestHandler(BaseRequestHandler):
    def handle(self):
        from utils import Utils
        print("Got new connection!")
        while True:
            msg = self.request.recv(1024)
            if not msg:
                break
            msg = loads(msg)
            print("Received:", msg)
            result = getattr(Utils(), msg[0])(msg[1])
            print(result)
            self.request.send(dumps(result))
            print("Done with connection")
    
if __name__ == '__main__':
    from messages import Messages
    messages = Messages()
    server1 = ThreadingTCPServer((messages.getValue("socket1", "host"), int(messages.getValue("socket1", "port"))), EchoRequestHandler)
    server2 = ThreadingTCPServer((messages.getValue("socket2", "host"), int(messages.getValue("socket2", "port"))), EchoRequestHandler)
    print("server running...")
    Thread(target=server1.serve_forever).start()
    Thread(target=server2.serve_forever).start()
