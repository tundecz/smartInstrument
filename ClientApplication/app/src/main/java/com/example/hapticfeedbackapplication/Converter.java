package com.example.hapticfeedbackapplication;

import java.lang.Math;
import java.util.Vector;

public class Converter {

    private static final Integer speedOfLight = 299792458;
    private static final Double minFreqLight = 4 * Math.pow(10,14); // THz
    private static final Double gamma = 0.8;

    private Converter(){
        // private constructor
    }


    public static Vector<Double> getRGB(Double frequency){
        Vector<Double> rgbColors = new Vector<>(3);
        Double visibleFreq = findVisibleOctave(frequency);
        Double waveLength = frequencyToWaveLenght(visibleFreq);
        Double red, green, blue;
        if(waveLength >= 380 && waveLength < 440){
            Double attenuation = 0.3 + 0.7 * (waveLength -380) / (440 - 380);
            red = ((-(waveLength - 440)/(440 - 380)) * attenuation);
            red = Math.pow(red, gamma);
            green = 0.0;
            blue = (1.0 * attenuation);
            blue = Math.pow(blue,gamma);
        }else if(waveLength >= 440 && waveLength < 490){
            red = 0.0;
            green = ((waveLength - 440) / (440-490));
            green = Math.pow(green, gamma);
            blue = 1.0;
        } else if(waveLength >= 490 && waveLength < 510){
            red = 0.0;
            green = 1.0;
            blue = (-(waveLength -510) / (510 - 490));
            blue = Math.pow(blue,gamma);
        }else if(waveLength >= 510 && waveLength <580){
            red = ((waveLength - 510) / (580 - 510));
            red = Math.pow(red,gamma);
            green = 1.0;
            blue = 0.0;
        }else if(waveLength >= 580 && waveLength <645){
            red = 1.0;
            green = (-(waveLength - 645) / (645 - 580));
            green = Math.pow(green, gamma);
            blue = 0.0;
        }else if(waveLength >= 645 && waveLength <= 750){
            Double attenuation = 0.3 + 0.7 * (750 - waveLength) / (750 - 645);
            red = Math.pow((1.0 * attenuation),gamma);
            green = 0.0;
            blue = 0.0;
        }else{
            red = 0.0;
            green = 0.0;
            blue = 0.0;
        }
        red *= 255;
        green *= 255;
        blue *= 255;
        rgbColors.add(0,red);
        rgbColors.add(1,green);
        rgbColors.add(2,blue);
        return rgbColors;
    }


    private static Double findVisibleOctave(Double frequency){
        while(frequency < minFreqLight){
            frequency = frequency * 2; // if we move up with one octave, the frequency increases logarithmically
        }
        return frequency;
    }


    private static Double frequencyToWaveLenght(Double frequency){
        Double wavelenght = speedOfLight/frequency;
        wavelenght = wavelenght/Math.pow(10,-9); //nanometers
        return wavelenght;
    }

}
