package redes;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;

public class Config {

    public String myname;
    public String mynode = "NotFound";
    public JSONObject topo;
    public JSONObject names;
    public Config(String jid)
    {
        getTopo();

        myname = jid;

        Iterator<String> keys = names.keys();

        while (keys.hasNext())
        {
            String k = keys.next();
            if (((String) names.get(k)).equals(myname))
            {
                mynode = k;
                System.out.println("This is node: " + k);
            }
        }
        if (mynode.equals("NotFound"))
        {
            System.out.println("JID represents no node");
            return;
        }
    }

    private void getTopo()
    {
        try
        {
            File topoFile = new File("topo-demo.txt");
            Scanner topoReader = new Scanner(topoFile);
            String s = topoReader.nextLine();
            topo =  (JSONObject) (new JSONObject(s)).get("config");
        }
        catch (java.io.FileNotFoundException e)
        {
            System.out.println("topo-demo.txt file not found");
        }
        catch (org.json.JSONException e)
        {
            System.out.println("Invalid topo file");
        }
        System.out.println("Loaded topo");
        try
        {
            File namesFile = new File("names-demo.txt");
            Scanner namesReader = new Scanner(namesFile);
            String s = namesReader.nextLine();
            names =  (JSONObject) (new JSONObject(s)).get("config");
        }
        catch (java.io.FileNotFoundException e)
        {
            System.out.println("names-demo.txt file not found");
        }
        catch (org.json.JSONException e)
        {
            System.out.println("Invalid names file");
        }
        System.out.println("Loaded names");
    }
}
