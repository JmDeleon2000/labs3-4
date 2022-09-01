package redes;
import org.jivesoftware.smack.SmackException;

import java.util.Scanner;


public class Main {
    static session sech;
    public static void main( String[] args )
    {
        Scanner scan = new Scanner(System.in);

        String domain = "alumchat.fun";


        boolean inband = false;

        System.out.println("Enter username (not JID): ");
        String user = scan.nextLine();

        System.out.println("Enter your password: ");
        String pw = scan.nextLine();
        try{
            sech = new session(domain, user, pw, inband);
        }
        catch (Exception e)
        {
            System.out.println(e.getMessage());
        }

        if (sech.con != null)
            System.out.println("Connected successfully");

        boolean validInput = false;
        String userInput = "";
        while (!validInput)
        {
            System.out.println("Ingrese una de las siguientes opciones:");
            System.out.println("1) Flooding");
            System.out.println("2) Distance Vector Routing");
            System.out.println("3) Link State Routing");

            Config conf = new Config(user+"@alumchat.fun");
            userInput = scan.nextLine().toLowerCase();
            switch (userInput)
            {
                case"1":
                    //TODO flooding
                    validInput = true;
                    break;
                case"2":
                    DVR dvr = new DVR(sech, conf);
                    validInput = true;
                    break;
                case"3":
                    //TODO lsr
                    validInput = true;
                    break;
                default:
                    System.out.println("Opción inválida");
                    break;
            }
        }

    }
}
