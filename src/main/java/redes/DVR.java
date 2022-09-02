package redes;


import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.chat2.Chat;
import org.jivesoftware.smack.chat2.ChatManager;
import org.jivesoftware.smack.chat2.IncomingChatMessageListener;
import org.jivesoftware.smack.packet.Message;
import org.json.JSONObject;
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
    String fuente = "";
    String destino = "";
    int saltos = 0;
    int distancia = 0;
    String recorrido = "";
    String mensaje = "";



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

    public listener(){}
    @Override
    public void newIncomingMessage(EntityBareJid from, Message message, Chat chat) {
        System.out.println(message.getBody());
    }
}