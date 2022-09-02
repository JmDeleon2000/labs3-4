package redes;


import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.chat2.Chat;
import org.jivesoftware.smack.chat2.ChatManager;
import org.jivesoftware.smack.chat2.IncomingChatMessageListener;
import org.jivesoftware.smack.packet.Message;
import org.json.JSONObject;
import org.json.JSONArray;

import java.util.ArrayList;
import org.jxmpp.jid.EntityBareJid;
import org.jxmpp.jid.impl.JidCreate;
import org.jxmpp.stringprep.XmppStringprepException;

import java.util.Iterator;
import java.util.Scanner;

public class DVR {

    String myname;
    String mynode = "NotFound";
    JSONObject topo;
    JSONObject names;
    ArrayList<ArrayList<Integer>> vecinos;
    ArrayList<String> nameList = new ArrayList<String>();


    JSONArray myVec ;

    Scanner UI = new Scanner(System.in);
    public DVR(session sech, Config conf)
    {

        myname = conf.myname;
        mynode = conf.mynode;
        try {
            EntityBareJid myjid = JidCreate.entityBareFrom(myname);
        } catch (XmppStringprepException e) {
            throw new RuntimeException(e);
        }
        topo = conf.topo;
        names = conf.names;

        Iterator<String> keys = names.keys();
        while (keys.hasNext())
            nameList.add(keys.next());


        vecinos = new ArrayList<ArrayList<Integer>>();


        JSONArray myVec = topo.getJSONArray(mynode);
        for(int i = 0; i <= topo.length(); i++) {
            vecinos.add(new ArrayList<Integer>());
            for (int j = 0; j <= topo.length(); j++)
            {
                if (j == i)
                    vecinos.get(i).add(1000);
                else
                    vecinos.get(i).add(0);
            }
        }

        System.out.println(vecinos);



        Chat chat;
        ChatManager manager = ChatManager.getInstanceFor(sech.con);
        listener list = new listener();
        manager.addIncomingListener(list);

        while (true)
        {
            System.out.println("To send a message write a target node.");
            System.out.println("Choose one of the following: ");
            System.out.println(nameList);

            String userinput = UI.nextLine();
            if (userinput.equals("-q"))
                break;
            if (!nameList.contains(userinput))
            {
                System.out.println("Invalid node name");
                continue;
            }
            System.out.println("Write a message: ");
            String msgBody = UI.nextLine();
            Msg m = new Msg(myname, names.getString(userinput), msgBody);
            try {
                chat = manager.chatWith(JidCreate.entityBareFrom(names.getString(userinput)));
            } catch (XmppStringprepException e) {
                throw new RuntimeException(e);
            }
            try {
                chat.send(m.toString());
            } catch (SmackException.NotConnectedException e) {
                throw new RuntimeException(e);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }


}

class Msg
{
    public String fuente = "";
    public String destino = "";
    public int saltos = 0;
    public int distancia = 0;
    public String recorrido = "";
    public String mensaje = "";



    public Msg(String fuente, String destino, String mensaje)
    {
        this.fuente = fuente;
        this.destino = destino;
        this.mensaje = mensaje;
        recorrido += fuente + ",";
    }
    public Msg(String json)
    {
        JSONObject a = new JSONObject(json);
        fuente = a.getString("fuente");
        destino = a.getString("destino");
        saltos = a.getInt("saltos");
        distancia = a.getInt("distancia");
        recorrido = a.getString("recorrido");
        mensaje = a.getString("mensaje");
    }
}

class listener implements IncomingChatMessageListener
{

    ChatManager chats;
    String myname;

    public listener(ChatManager c, String n)
    {
        chats = c;
        myname = n;
    }
    @Override
    public void newIncomingMessage(EntityBareJid from, Message message, Chat chat) {
        Msg m = new Msg(message.getBody());
        if (myname.equals(m.destino))
                System.out.println("Mensaje recibido: "  + message.getBody());
        else
        {
            System.out.println("Pasando: " + message.getBody());
            try {
                Chat forward = chats.chatWith(JidCreate.entityBareFrom(m.destino));
                m.saltos += 1;
                m.distancia += 1;
                m.recorrido += myname + ",";

                forward.send(m.toString());

            } catch (XmppStringprepException e) {
                throw new RuntimeException(e);
            } catch (SmackException.NotConnectedException e) {
                throw new RuntimeException(e);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }

        }
    }
}