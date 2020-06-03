package com.example.hapticfeedbackapplication;

import androidx.appcompat.app.AppCompatActivity;

import android.graphics.Color;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.ImageView;
import android.widget.SeekBar;
import android.widget.Switch;
import android.widget.Toast;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Random;

public class MainActivity extends AppCompatActivity {

    Switch onOffSwitch;
    Switch bassOnOffSwitch;
    Switch trebleOnOffSwitch;
    Switch highOnOffSwitch;
    SeekBar seekBar;
    Button resetButton;
    ImageView frequencyColorView;
    int seekBarProgress = 50;

//    ClientThread clientThread;
    ClientSocket clientThread;
    Thread thread;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        initializeVariables();
        setDefaultValues();
//        clientThread = new ClientThread();
        clientThread = new ClientSocket();
        thread = new Thread(clientThread);
        thread.start();

        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
                Toast.makeText(getApplicationContext(),"seekbar progress: " + progress, Toast.LENGTH_SHORT).show();
//                frequencyColorView.setBackgroundColor(Color.BLACK);
                if(clientThread != null){
                    clientThread.sendMessage("progress " + progress);
                }
            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // or we can send the progress here
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

        resetButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                resetValues();
                if(clientThread != null){
                    clientThread.sendMessage("reset all");
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
        resetButton = findViewById(R.id.reset_all);
        frequencyColorView = findViewById(R.id.colorView);
    }

    private void setDefaultValues(){
        onOffSwitch.setChecked(true);
        bassOnOffSwitch.setChecked(true);
        trebleOnOffSwitch.setChecked(true);
        highOnOffSwitch.setChecked(true);
        seekBar.setProgress(seekBarProgress);
    }

    private void resetValues() {
        bassOnOffSwitch.setChecked(true);
        trebleOnOffSwitch.setChecked(true);
        highOnOffSwitch.setChecked(true);
        seekBar.setProgress(seekBarProgress);
    }

    private void sendMessageToServer(boolean isChecked, String type, ClientSocket clientThread){
        if(isChecked){
            clientThread.sendMessage(type + " on");
        }else{
            clientThread.sendMessage(type + " off");
        }
    }

    private void setColor(Float frequency){
        Random rand = new Random();
        frequencyColorView.setBackgroundColor(Color.argb(255,rand.nextInt(256),rand.nextInt(256),rand.nextInt(256)));
    }



    public class ClientSocket implements Runnable{

        private Socket socket;
        private InputStream inputStream;
        private DataInputStream in;
        private final int bufferSize = 13;

        @Override
        public void run() {
            try {
                socket = new Socket("192.168.1.12", 65432);
                Log.d("socket","Socket binded");
                inputStream = socket.getInputStream();
                in = new DataInputStream(inputStream);
                Log.d("socket","Socket binded");
                new Thread(new MessageThread()).run();
            } catch (IOException e) {
                e.printStackTrace();
            }

        }

        public void sendMessage(final String message){
            new Thread(new Runnable() {
                @Override
                public void run() {
                    if(null != socket){
                        try {
                            PrintWriter out = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
                            out.println(message);
                        } catch (IOException e) {
                            e.printStackTrace();
                        }
                    }
                }
            }).start();
        }

        public class MessageThread implements Runnable{

            @Override
            public void run() {
                while(true){
                    try {
                        byte[] message = new byte[bufferSize];
                        in.readFully(message);
                        String decoded = new String(message,"UTF-8");
                        Log.d("socket",decoded);
                        try{
                            final Float frequencyValue = Float.valueOf(decoded);
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    setColor(frequencyValue);
                                }
                            });
                        } catch (NumberFormatException e){
                            e.printStackTrace();
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    }

}
