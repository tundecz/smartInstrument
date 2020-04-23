from queue import Queue
from constants import QUEUE_MAX_SIZE
from threading import Event

message_q = Queue(maxsize = QUEUE_MAX_SIZE) # this queue is for when the client sent data to the server
ev = Event()
def insert_message(message):
    message_q.put(message)


def get_message_from_queue():
    message = message_q.get()
    message_q.task_done()
    return message

# need to thing how can we 
def new_mesage_has_arrived():
    return False if message_q.empty() else True

# this module is creatied for the coomuniction between two threads
# for the love of god, change the module name