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



    }
}
