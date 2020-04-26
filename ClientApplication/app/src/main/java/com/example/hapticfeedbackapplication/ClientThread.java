package com.example.hapticfeedbackapplication;

import java.io.BufferedReader;
import java.io.IOException;
import java.net.Socket;
import java.net.UnknownHostException;

public class ClientThread implements Runnable {

    private Socket socket;
    private BufferedReader bufferedReader;

    @Override
    public void run() {
        try {
         socket = new Socket("a", 65432);
         if(socket.isBound()){

         }
        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
