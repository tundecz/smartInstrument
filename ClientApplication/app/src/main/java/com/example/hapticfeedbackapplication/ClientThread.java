package com.example.hapticfeedbackapplication;

import android.util.Log;
import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.BufferedWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class ClientThread implements Runnable {

    private Socket socket;
    private BufferedReader bufferedReader;
    private InputStream inputStream;
    private static final String SERVER_IP = "localhost";
    private DataInputStream in;
    private final int bufferSize = 13;

    @Override
    public void run() {
        try {
         socket = new Socket("192.168.1.12", 65432);
         Log.d("socket","Socket binded");
         inputStream = socket.getInputStream();
         bufferedReader = new BufferedReader(new InputStreamReader(inputStream, "UTF-8"));
         in = new DataInputStream(inputStream);
         Log.d("socket","Socket binded");
         new Thread(new MessageThread()).start();
        } catch (UnknownHostException e) {
            System.out.println("Server not found");
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

    class MessageThread implements Runnable{

        @Override
        public void run() {
            while(true){
                try {
                    byte[] message = new byte[bufferSize];

                    in.readFully(message);
                    String decoded = new String(message,"UTF-8");
//
//                    inputStream.read(message);
//                    String m = new String(message, "UTF-8");


//                    Log.d("socket","Socket binded");
//                    byte[] m = bufferedReader.readLine().getBytes();
                    Log.d("socket", decoded);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

}

