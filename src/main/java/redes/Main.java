package redes;
import org.jivesoftware.smack.SmackException;

import java.util.Scanner;


public class Main {
    static session sech;
    public static void main( String[] args )
    {
        Scanner scan = new Scanner(System.in);



        System.out.println("Enter domain: ");
        String domain = scan.nextLine();




        boolean inband = true;
        boolean invalid_input = true;
        while (invalid_input)
        {
            System.out.println("Do you want have an account? (Y/N): ");

            switch (scan.nextLine().toUpperCase())
            {
                case "Y":
                    inband = false;
                    invalid_input = false;
                    break;
                case "N":
                    invalid_input = false;
                    break;
                default:
                    break;
            }
        }



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
        try {
            ui myUI = new ui();
        }
        catch (SmackException.NotConnectedException e){System.out.println("Not yet connected");}
        catch (SmackException.NotLoggedInException e){System.out.println("Not yet logged in");}
        catch (InterruptedException e) {System.out.println(e.getMessage());}

    }
}
