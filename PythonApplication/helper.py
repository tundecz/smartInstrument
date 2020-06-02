import math
import constants
from gpiozero.tones import Tone
from messages import DEFAULT_VALUES, Message

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
    # need to add here the value changer
    # if value < 0.5 or value > 0.5, scale the vibration value
    @staticmethod
    def calculate_value_based_on_note(midiNote):
        if DEFAULT_VALUES[Message.PROGRESS] != 50:
            changed_amount = Helper._calculate_additional_progress()
            if midiNote == constants.MIDDLE_A:
                return constants.MIDDLE_A_VALUE + changed_amount
            else:
                vibration_value = Helper._rule_of_3(midiNote)
                vibration_value += changed_amount
                print("Calculated vibration value: {}".format(str(vibration_value)))
                if vibration_value > 1:
                    return 1
                else:
                    return vibration_value
        else:
            if midiNote == constants.MIDDLE_A:
                print("Middle A value {}".format(str(constants.MIDDLE_A_VALUE)))
                return constants.MIDDLE_A_VALUE
            else:
                vibration_value = Helper._rule_of_3(midiNote)
                print("Calculated vibration value: {}".format(str(vibration_value)))
                if vibration_value > 1:
                    return 1
                else:
                    return vibration_value


    # calculates the vibration value based on user progress input
    # explenation : the middle of the slider is 50
    # if we move it up to 60, it means we moved it up with 10 values
    # if we move it down to 40, we also moved it 10 values
    # we know that if we move it up to 100, we moved it up 50 values
    # the max values for the change will be 0.2
    # so if 50 is 0.2 then changed_amount will be the new value
    # if <, we return it with -, because we have to substract 
    @staticmethod
    def _calculate_additional_progress():
        if DEFAULT_VALUES[Message.PROGRESS] < 50:
            changed_amount = 50 - DEFAULT_VALUES[Message.PROGRESS]
            return -((changed_amount * constants.MAX_MIN_PROGRESS_VALUE)/constants.DEFAULT_VALUE_FOR_SLIDER)
        elif DEFAULT_VALUES[Message.PROGRESS] > 50:
            changed_amount = DEFAULT_VALUES[Message.PROGRESS]
            return ((changed_amount * constants.MAX_MIN_PROGRESS_VALUE)/constants.DEFAULT_VALUE_FOR_SLIDER)

    # take a look on github at Tone class for a better representation for the value
    @staticmethod
    def _rule_of_3(note):
        return (constants.MIDDLE_A * constants.MIDDLE_A_VALUE)/note
    
    # we consider the bass range to stop at middle C
    @staticmethod
    def is_in_bass_range(midiNumber):
        return True if midiNumber < constants.MIDDLE_C else False

    # treble range  == the range that we play with our right hands
    @staticmethod
    def is_in_treble_range(midiNumber):
        return True if midiNumber >= constants.MIDDLE_C and midiNumber <= 70 else False # need to change 70
    
    # operation => on/off
    # note => bass/treble/high
    @staticmethod
    def parse_dequeued_message(message):
        return message.split()

    # for easer parsing in client side
    # appending with 00000001 to have the correct lenght to send
    @staticmethod
    def append_to_frequency(frequency):
        string_frequency = str(frequency)
        if len(string_frequency) < 9:
            to_append = "00000001"
            new_frequency = string_frequency + to_append
            print(new_frequency)
            return float(new_frequency)
        return frequency

