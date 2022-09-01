package redes;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.File;
import java.util.Iterator;
import java.util.Scanner;

public class DVR {

    String myname;
    String mynode = "NotFound";
    JSONObject topo;
    JSONObject names;

    Scanner UI = new Scanner(System.in);
    public DVR(session sech, Config conf)
    {

        myname = conf.myname;
        mynode = conf.mynode;

        topo = conf.topo;;
        names = conf.names;

    }


}
