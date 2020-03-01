import readMidiMido as midi
from constants import PORT_NAME


if __name__ == "__main__":
    instrument = midi.ReadMidi(PORT_NAME)
    instrument.run()
    