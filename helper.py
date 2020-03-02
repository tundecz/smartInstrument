import math

class Helper:

    # calculates the frequency based on the given midi note
    # formula: f(n) = 2 ^ ((n-49)/12) * 440 Hz
    @staticmethod
    def convertMidiNumberToFrequency(midiNumer):
        base = 2
        power = (midiNumer-49)/12
        return math.pow(base, power) * 440