package redes;
import org.jivesoftware.smack.ConnectionConfiguration;
import org.jivesoftware.smack.SmackException;
import org.jivesoftware.smack.XMPPException;
import org.jivesoftware.smack.packet.Presence;
import org.jivesoftware.smack.packet.PresenceBuilder;
import org.jivesoftware.smack.roster.Roster;
import org.jivesoftware.smack.tcp.XMPPTCPConnectionConfiguration;
import org.jivesoftware.smack.AbstractXMPPConnection;
import org.jivesoftware.smackx.iqregister.AccountManager;
import org.jivesoftware.smack.tcp.XMPPTCPConnection;
import org.jxmpp.jid.parts.Localpart;


class session
{
    public AbstractXMPPConnection con;
    public String domainName;

    public session(String domain, String user, String pw, boolean inBandReg) throws Exception
    {
        domainName = domain;
        if (inBandReg)
        {
            XMPPTCPConnectionConfiguration conConf =
                    XMPPTCPConnectionConfiguration.builder()
                            .setXmppDomain(domain)
                            .setHost(domain)
                            .setSendPresence(true)
                            .setSecurityMode(ConnectionConfiguration.SecurityMode.disabled)
                            .build();
            con = new XMPPTCPConnection(conConf);


            con.connect();

            AccountManager acctManager = AccountManager.getInstance(con);

            acctManager.sensitiveOperationOverInsecureConnection(true);
            acctManager.createAccount(Localpart.from(user), pw);

            con.login(user, pw);

        }
        else
        {
            XMPPTCPConnectionConfiguration conConf =
                    XMPPTCPConnectionConfiguration.builder()
                            .setXmppDomain(domain)
                            .setHost(domain)
                            .setSendPresence(true)
                            .setSecurityMode(ConnectionConfiguration.SecurityMode.disabled)
                            .setUsernameAndPassword(user, pw)
                            .build();
            con = new XMPPTCPConnection(conConf);

            con.connect();
            con.login();
        }
        Presence presence = PresenceBuilder.buildPresence()
                .setMode(Presence.Mode.available)
                .build();
        con.sendStanza(presence);
        Roster.setDefaultSubscriptionMode(Roster.SubscriptionMode.accept_all);
    }

    public void tryRemoveAccount() throws SmackException.NotConnectedException, InterruptedException
    {
        AccountManager acctManager = AccountManager.getInstance(con);
        try {
            acctManager.deleteAccount();
        } catch (SmackException.NoResponseException e){System.out.println("Couldn't delete account");}
        catch (XMPPException.XMPPErrorException e){System.out.println("Couldn't delete account");}
    }
}
