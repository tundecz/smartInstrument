import readMidiMido as midi
from constants import PORT_NAME
import logging


def main():
    main_logger = logging.getLogger('root')
    instrument = midi.ReadMidi(PORT_NAME)
    instrument.run()

if __name__ == "__main__":
    main()
    