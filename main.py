import readMidiMido as midi
from constants import PORT_NAME, HOST, PORT
import logging
import socket
import serverSocket
import threading

def runMidiReading():
    print("In the maun function")
    instrument = midi.ReadMidi(PORT_NAME)
    instrument.run()

def runServer():
    server = serverSocket.MessageServer((HOST, PORT))
    server.serve_forever()
 
if __name__ == "__main__":
    t1 = threading.Thread(target = runMidiReading) #we don't want to execute the function, so don't put ()
    rt2 = threading.Thread(target = runServer)

    
    