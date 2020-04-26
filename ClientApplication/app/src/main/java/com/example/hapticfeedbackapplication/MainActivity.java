package com.example.hapticfeedbackapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.widget.SeekBar;
import android.widget.Switch;

import java.net.Socket;

public class MainActivity extends AppCompatActivity {

    String SERVER_IP;
    Integer SERVER_PORT;
    Switch onOffSwitch;
    SeekBar bassSeekBar;
    SeekBar seekBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        onOffSwitch = findViewById(R.id.on_off_switch);
        bassSeekBar = findViewById(R.id.bass_seek_bar);
        seekBar = findViewById(R.id.seek_bar);

        onOffSwitch.setChecked(true); // wa want to be on when we start the application

//        new Thread(new ClientThread()).start();
    }

    public void onProgressChanged(SeekBar seekBar, int progressValue, boolean fromUser){

    }
}
