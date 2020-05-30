import socket
from constants import HOST, PORT
import asyncore # wrappre over socket
import constants
import bridge

class MessageHandler(asyncore.dispatcher):

    def __init__(self, conn_sock, client_addr, server):
        print("In the Message Handler constructor")
        self.server = server
        self.client_addr = client_addr

        asyncore.dispatcher.__init__(self, conn_sock)

    # it means the server is allowed to read messages from the client
    def readable(self):
        return True
    
    # change this if we don't send anything from the server
    def writable(self):
        # if len(bridge.message_to_client_q) != 0:
        #     return True
        # return False
        return True

    # send frequencies to client for color represenation
    def handle_write(self):
        if(len(bridge.message_to_client_q) != 0):
            to_send = bridge.message_to_client_q.pop()
            string_to_send = str(to_send).encode()
            sent = self.send(string_to_send)

    # reads the incomming message from the client
    def handle_read(self):
        data = self.recv(constants.BUFFER_SIZE)
        decoded_data = data.decode()
        bridge.enqueue_message(decoded_data)
        # print(data.decode())

    def handle_close(self):
        self.close()


class MessageServer(asyncore.dispatcher):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 2

    def __init__(self, address, handlerClass = MessageHandler):
        self.address = address
        self.handlerClass = handlerClass
        print("Hello fro the server")
        
        asyncore.dispatcher.__init__(self)
        self.create_socket(self.address_family, self.socket_type)
        self.set_reuse_addr()
        self.server_bind()
        self.server_activate()


    def server_bind(self):
        self.bind(self.address)

    #listen to connection
    def server_activate(self):
        self.listen(self.request_queue_size)

    # serve the server
    def serve_forever(self):
        asyncore.loop()

    # the handlerClass will handle the reading
    def handle_accept(self):
        (conn_sock, client_addr) = self.accept()
        self.handlerClass(conn_sock, client_addr, self)

# use it like this

# server = serverSocket.MessageServer((PORT, HOTS))
# server.serve_forever()