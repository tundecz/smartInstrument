package com.example.hapticfeedbackapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.Toast;

import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    String SERVER_IP;
    Integer SERVER_PORT;
    Switch onOffSwitch;
    Switch bassOnOffSwitch;
    Switch trebleOnOffSwitch;
    Switch highOnOffSwitch;
    SeekBar seekBar;
    int seekBarProgress = 50;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initializeVariables();
        setDefaultValues();

       // wa want to be on when we start the application

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                Toast.makeText(getApplicationContext(),"seekbar progress: " + progress, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
//                Toast.makeText(getApplicationContext(), "seekbar touch started!", Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
//                Toast.makeText(getApplicationContext(), "sekkabr touched stopped!", Toast.LENGTH_SHORT).show();
            }
        });

//        new Thread(new ClientThread()).start();
    }

    private void initializeVariables(){
        onOffSwitch = findViewById(R.id.on_off_switch);
        bassOnOffSwitch= findViewById(R.id.bass_on_off_switch);
        trebleOnOffSwitch = findViewById(R.id.treble_on_off_switch);
        highOnOffSwitch = findViewById(R.id.high_on_off_switch);
        seekBar = findViewById(R.id.seek_bar);
    }

    private void setDefaultValues(){
        onOffSwitch.setChecked(true);
        bassOnOffSwitch.setChecked(true);
        trebleOnOffSwitch.setChecked(true);
        highOnOffSwitch.setChecked(true);
        seekBar.setProgress(seekBarProgress);
    }
}
