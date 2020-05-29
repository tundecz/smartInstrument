package com.example.hapticfeedbackapplication;

import android.util.Log;
import java.io.BufferedInputStream;
import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.BufferedWriter;
import java.net.Socket;
import java.net.UnknownHostException;

public class ClientThread implements Runnable {

    private Socket socket;
//    private BufferedReader bufferedReader;
    private DataInputStream in;
    private static final String SERVER_IP = "localhost";
    private InputStream input;
//    public static

    @Override
    public void run() {
        try {
//         InetAddress servAddrs = InetAddress.getByName(SERVER_IP);
         socket = new Socket("192.168.1.8", 65432);
         Log.d("socket","Socket binded");
         in = new DataInputStream(new BufferedInputStream(socket.getInputStream()));
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
                    Log.d("socket","test");
                    byte[] message = new byte[1024];
                    in.read(message);
                    String m = new String(message, "UTF-8");
                    Log.d("socket",m);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

}

