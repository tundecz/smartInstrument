package com.example.hapticfeedbackapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.CompoundButton;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.Toast;

public class MainActivity extends AppCompatActivity {

    Switch onOffSwitch;
    Switch bassOnOffSwitch;
    Switch trebleOnOffSwitch;
    Switch highOnOffSwitch;
    SeekBar seekBar;
    int seekBarProgress = 50;

    ClientThread clientThread;
    Thread thread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initializeVariables();
        setDefaultValues();
        clientThread = new ClientThread();
        thread = new Thread(clientThread);
        thread.start();

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                Toast.makeText(getApplicationContext(),"seekbar progress: " + progress, Toast.LENGTH_SHORT).show();
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {

            }
        });

        onOffSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
               if(clientThread != null){
                  sendMessageToServer(isChecked,"switch",clientThread);
               }
            }
        });

        bassOnOffSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
               if(clientThread != null){
                  sendMessageToServer(isChecked,"bass",clientThread);
               }
            }
        });

        trebleOnOffSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(clientThread != null){
                   sendMessageToServer(isChecked,"treble",clientThread);
                }
            }
        });

        highOnOffSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if(clientThread != null){
                  sendMessageToServer(isChecked,"high",clientThread);
                }
            }
        });
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

    private void sendMessageToServer(boolean isChecked, String type, ClientThread clientThread){
        if(isChecked){
            clientThread.sendMessage(type + " on");
        }else{
            clientThread.sendMessage(type + " off");
        }
    }
}
