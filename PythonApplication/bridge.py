try:
    import queue as Queue
except ImportError:
    import Queue 
from constants import QUEUE_MAX_SIZE
from threading import Event

message_q = Queue.Queue(maxsize = QUEUE_MAX_SIZE)
message_to_client_q = []
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