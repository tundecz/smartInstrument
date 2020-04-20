import socket
import asyncore
import time

class Client(asyncore.dispatcher):

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect(('localhost', 8888))


    def handle_write(self):
        message = "hello"
        self.send(message.encode())
        time.sleep(3)
    
    def handle_read(self):
        data = self.recv(1024)
        print(data.decode())

    def handle_close(self):
        self.close()


client = Client()
asyncore.loop()