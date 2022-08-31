package redes;


import org.jivesoftware.smack.SmackException;

import org.jivesoftware.smack.chat2.ChatManager;
import org.jivesoftware.smack.packet.Presence;
import org.jivesoftware.smack.packet.PresenceBuilder;
import org.jivesoftware.smack.roster.Roster;
import  org.jivesoftware.smack.roster.RosterEntry;
import org.jivesoftware.smack.roster.RosterListener;
import org.jivesoftware.smackx.muc.MultiUserChatManager;
import org.jxmpp.jid.BareJid;
import org.jxmpp.jid.EntityBareJid;
import org.jxmpp.jid.Jid;
import org.jxmpp.jid.impl.JidCreate;
import org.jxmpp.stringprep.XmppStringprepException;


import java.util.Collection;
import java.util.Scanner;

public class ui {
    Roster roster;
    ChatManager chatManager;
    MultiUserChatManager GCManager;
    ui() throws SmackException.NotConnectedException, SmackException.NotLoggedInException, InterruptedException
    {
        roster = Roster.getInstanceFor(Main.sech.con);
        //https://github.com/igniterealtime/Smack/blob/master/documentation/roster.md
        roster.addRosterListener(new RosterListener() {
            public void entriesAdded(Collection<Jid> addresses) {}
            public void entriesDeleted(Collection<Jid> addresses) {}
            public void entriesUpdated(Collection<Jid> addresses) {}
            public void presenceChanged(Presence presence) { }
        });
        showRoster();

        chatManager = ChatManager.getInstanceFor(Main.sech.con);
        GCManager = MultiUserChatManager.getInstanceFor(Main.sech.con);
        Scanner scan = new Scanner(System.in);
        boolean running = true;
        String userInput;
        String args = "";
        String command;
        while (running)
        {
            System.out.print(Main.sech.domainName + ": ");
            userInput = scan.nextLine();
            command = userInput.split(" ")[0];
            if (command != userInput)
                args = userInput.split(" ")[1];

            switch (command)
            {
                case "-h":
                    print("-h:\tDisplay this message");
                    print("-r:\tShow your roster");
                    print("-radd: [JID]\tAdd a user to your roster");
                    print("-rdetail:\tShow details about a user in your roster");
                    print("-c: [JID]\tChat with a user");
                    print("-cg [Group chat name]\tJoin a group chat (creates a new one if the specified room doesn't exist)");
                    print("-dc:\tDisconnect (log out)");
                    print("-rmacc:\tDeletes current account from the server");
                    print("-st:\tChange status");
                    break;
                case"-r":
                    showRoster();
                    break;
                case "-c":
                    try
                    {
                        EntityBareJid jid = JidCreate.entityBareFrom(args);
                        direct_chat dm = direct_chat.getChat(jid, chatManager);
                        dm.run();
                    }catch (XmppStringprepException e) {print(args + " isn't a valid JID");}
                    break;
                case"-radd":
                    try {
                        EntityBareJid jid = JidCreate.entityBareFrom(args);
                        roster.sendSubscriptionRequest(jid);
                        print("Subscription request sent successfully!");
                    }catch (XmppStringprepException e) {print(args + " isn't a valid JID");}
                    break;
                case"-rdetail":
                    try {
                        EntityBareJid jid = JidCreate.entityBareFrom(args);
                        showDetails(jid);
                    }catch (XmppStringprepException e) {print(args + " isn't a valid JID");}
                    break;
                case "-gc":
                    try {
                        muc gc = muc.getMUC(args, GCManager);
                        gc.enter();
                    }catch (XmppStringprepException e) {print(args + " isn't a valid JID");}
                    break;
                case"-dc":
                    running = false;
                    if(Main.sech.con != null)
                        Main.sech.con.disconnect();
                    break;
                case "-st":
                    print("Write your new status: ");
                    changeStatus(scan.nextLine());
                    break;
                case "-rmacc":
                    Main.sech.tryRemoveAccount();
                    running = false;
                    break;
                default:
                    print("Usage error. Use -h for reference.");
                    break;
            }
        }

    }


    void showRoster() throws SmackException.NotConnectedException, SmackException.NotLoggedInException
    {


        if (!roster.isLoaded())
        {
            print("Loading roster...");
            try {
                roster.reloadAndWait();
            }
            catch (InterruptedException e){}
        }
        Collection<RosterEntry> entries = roster.getEntries();
        if(entries.size() == 0)
            print("Looks like your roster is empty!");
        else {
            for (RosterEntry entry : entries) {
                print(entry);
            }
        }
    }

    void  showDetails(BareJid jid)
    {
        RosterEntry entry = roster.getEntry(jid);

        print(entry);
        print("Subscription approved: " + entry.isApproved());
        print("Can see their presence: " + entry.canSeeHisPresence());
        print("Can see your presence: " + entry.canSeeMyPresence());
        //print("Groups: " + entry.getGroups());
        Presence presence = roster.getPresence(jid);
        print("Is available: " + presence.isAvailable());
        print("Status: " + presence.getStatus());

    }

    void changeStatus(String status) throws SmackException.NotConnectedException, InterruptedException
    {
        Presence presence = PresenceBuilder.buildPresence()
                .setMode(Presence.Mode.available)
                .setStatus(status)
                .build();
        Main.sech.con.sendStanza(presence);
        print("Status changed!");
    }

    //Enserio me cae mal lo verboso que es Java
    void print(Object a)
    {
        System.out.println(a);
    }
}


