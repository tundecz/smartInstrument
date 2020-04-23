from queue import Queue
from constants import QUEUE_MAX_SIZE
from threading import Event

message_q = Queue(maxsize = QUEUE_MAX_SIZE) # this queue is for when the client sent data to the server
ev = Event()
def enqueue_message(message):
    message_q.put(message)
    ev.set()


def dequeue_message():
    message = message_q.get()
    message_q.task_done()
    ev.clear() # do we need to call this method here or in readMidiMido class?
    return message

# this module is creatied for the coomuniction between two threads
# for the love of god, change the module name