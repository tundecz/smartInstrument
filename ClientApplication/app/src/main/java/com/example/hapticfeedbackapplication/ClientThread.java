package com.example.hapticfeedbackapplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.BufferedWriter;
import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.Socket;
import java.net.UnknownHostException;

public class ClientThread implements Runnable {

    private Socket socket;
    private BufferedReader bufferedReader;
    private static final String SERVER_IP = "raspberrypi.local";

    @Override
    public void run() {
        try {
         InetAddress servAddrs = InetAddress.getByName(SERVER_IP);
         socket = new Socket(servAddrs, 65432);
         if(socket.isBound()){

         }
        } catch (UnknownHostException e) {
            e.printStackTrace();
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
}
