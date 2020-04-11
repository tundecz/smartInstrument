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
        if midiNote is constants.MIDDLE_A:
            print("Middle C value {}".format(str(constants.MIDDLE_A_VALUE)))
            return constants.MIDDLE_A_VALUE
        else:
            vibration_value = Helper._rule_of_3(midiNote)
            print("Calculated vibration value: {}".format(str(vibration_value)))
            if vibration_value > 1:
                return 1
            else:
                return vibration_value

    @staticmethod
    def _rule_of_3(note):
        return (constants.MIDDLE_A * constants.MIDDLE_A_VALUE)/note
    
    # we consider the bass range to stop at middle C
    @staticmethod
    def is_in_bass_range(midiNumber):
        return True if midiNumber <= constants.MIDDLE_C else False

    @staticmethod
    def is_in_treble_range(midiNumber):
        return True if midiNumber >= constants.MIDDLE_C and midiNumber <= 70 else False # need to change 70
    
    
