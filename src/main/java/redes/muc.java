package redes;

import org.jivesoftware.smack.MessageListener;
import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.XMPPException;
import org.jivesoftware.smack.packet.Message;
import org.jivesoftware.smack.packet.MessageBuilder;
import org.jivesoftware.smackx.muc.MultiUserChat;
import org.jivesoftware.smackx.muc.MultiUserChatException;
import org.jivesoftware.smackx.muc.MultiUserChatManager;


import org.jxmpp.jid.EntityBareJid;
import org.jxmpp.jid.impl.JidCreate;
import org.jxmpp.jid.parts.Domainpart;
import org.jxmpp.jid.parts.Resourcepart;
import org.jxmpp.stringprep.XmppStringprepException;

import java.util.ArrayList;
import java.util.Scanner;

public class muc
{
    static  muc active;
    String RoomName = "";
    MultiUserChat chat;
    Resourcepart myResourcePart;
    MUCListener listener;
    static ArrayList<Resourcepart> openJIDs = new ArrayList<Resourcepart>();
    static ArrayList<muc> openChats = new ArrayList<muc>();
    private muc(EntityBareJid room, Resourcepart room_name, MultiUserChatManager manager) throws SmackException.NotConnectedException
    {
        chat = manager.getMultiUserChat(room);
        try
        {
            chat.create(room_name).makeInstant();
        }
        catch (SmackException.NoResponseException e) {}
        catch (InterruptedException e) {}
        catch (XMPPException.XMPPErrorException e){}
        catch (MultiUserChatException.NotAMucServiceException e){}
        catch (MultiUserChatException.MissingMucCreationAcknowledgeException e){}
        catch (MultiUserChatException.MucAlreadyJoinedException e)
        {
           // chat = manager.getMultiUserChat(room);
        }
        openJIDs.add(room_name);
        openChats.add(this);
        RoomName = room_name.toString();
        listener = new MUCListener(this);
        chat.addMessageListener(listener);
    }

    public static muc getMUC(String room_name, MultiUserChatManager manager) throws SmackException.NotConnectedException, XmppStringprepException
    {
        EntityBareJid room = JidCreate.entityBareFrom(room_name + "@" + Main.sech.domainName);
        Resourcepart resourcepart = Resourcepart.from(room_name);

        if (openJIDs.contains(resourcepart))
        {
            for (muc chat : openChats)
                if (chat.myResourcePart == resourcepart)
                    return chat;
        }
        return new muc(room, resourcepart, manager);
    }

    public void enter()
    {
        active = this;
        Scanner scan = new Scanner(System.in);
        print("Type -q to quit current chat, -h for help. Any other input will be sent as messages.");
        print("--------------------------------" + RoomName + "--------------------------------");
        String userInput;
        boolean running = true;
        System.out.print(listener.msgQueue);
        listener.msgQueue = "";
        while (running)
        {

            userInput = scan.nextLine();

            switch (userInput)
            {
                case "-h":
                    print("Type -q to quit current chat, -h for help. Any other input will be sent as messages.");
                    break;
                case "-q":
                    running = false;
                    break;
                default:
                    try {
                        chat.sendMessage(
                                MessageBuilder
                                        .buildMessage()
                                        .setBody(userInput));
                    }catch (SmackException.NotConnectedException e) {print("Unexpectedly disconnected");}
                    catch (InterruptedException ignored){}
                    break;
            }

        }
        active = null;
    }
    //Enserio me cae mal lo verboso que es Java
    void print(Object a)
    {
        System.out.println(a);
    }
}


class MUCListener implements MessageListener {

    muc myChat;
    public String msgQueue = "";

    public  MUCListener(muc chat)
    {
        myChat = chat;
    }

    @Override
    public void processMessage(Message message) {
        if (muc.active == myChat)
        {
            System.out.println(message.getBody());
        }
        else
        {
            msgQueue += message.getBody();
        }
    }
}