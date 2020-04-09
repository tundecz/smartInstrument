import math
import constants
from gpiozero.tones import Tone

class Helper:

    # calculates the frequency based on the given midi note
    # formula: f(n) = 2 ^ ((n-49)/12) * 440 Hz
    @staticmethod
    def convert_midi_number_to_frequency(midiNumer):
        try:
            tone = Tone(midi=midiNumer)
            return tone.frequency
        except:
            print("Operation problem (convert midi number to freuency)")

    # converts midi note numbers to ansi note
    @staticmethod
    def number_to_note(midiNumber):
        return constants.NOTES[midiNumber % 12]

    @staticmethod
    def convert_velocity_to_value(velocity):
        #due to some keyboard issue, mostly I get 0 velocity when a key is pressed
        if velocity is 0:
            return 0.5
        else:
            pass

    # middle A (69) will be 0.5
    @staticmethod
    def calculate_value_based_on_note(midiNote):
        if midiNote is constants.MIDDLE_C:
            return constants.MIDDLE_C_VALUE
        else:
            return Helper._rule_of_3(midiNote)

    @staticmethod
    def _rule_of_3(note):
        return (constants.MIDDLE_C * constants.MIDDLE_C_VALUE)/note
    
    
    
