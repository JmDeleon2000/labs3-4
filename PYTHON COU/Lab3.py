
import logging
import asyncio
#import time
import json
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp import ClientXMPP

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#logging.basicConfig(level=logging.DEBUG,format='%(levelname)-8s %(message)s')

seleccion=""
global_user = ""
global_password=""
global_message=""
global_destino=""
node_dest=""

rutas={
	"A":['B','D'],
	"B":['C'],
	"D":['B']
}

alias= {
	"A":"nodoa@alumchat.fun",
	"B":"nodob@alumchat.fun",
	"C":"nodoc@alumchat.fun",
	"D":"couvid@alumchat.fun"
}

menu1= "BIENVENIDA/ BEINVENIDO A ALUMNCHAT \n PRESIONE : \n 1) PARA LOGUEARSE CON UN USUARIO EXISTENTE\n 2) PARA SALIR \n"
menu2= "BIENVENIDA/ BEINVENIDO " +global_user +" \n PRESIONE : \n 1) PARA CERRAR SESION DE UN USUARIO EXISTENTE\n 2) PARA ELIMINAR A UN USUARIO EXISTENTE\n 3) PARA MOSTRAR TODOS LOS CONTACTOS Y SUS ESTADOS\n 4) PARA AGREGAR UN USUARIO A LOS CONTACTOS\n 5) PARA ENVIAR UN MENSAJE DIRECTO A UN USUARIO\n 6) PARA ENVIAR UN MENSAJE A UN GRUPO\n 7) PARA DEFINIR UN MENSAJE DE PRESCENCIA \n 8) PARA SALIR \n"

# print("**LEER JSON**")

# text_file = open("names.json", "r")
# data = text_file.read()
# text_file.close()
# print(data)
# print(type(data))

# data = data.replace("'",'"')
# print()


# names= json.load(data)

# print(names)



class chatClient(ClientXMPP):

	def __init__(self, jid, password):
		##Extension de la clase clientxmpp
	    ClientXMPP.__init__(self, jid, password)
	    print("Credenciales")
	    print(self.boundjid.user)
	    print(self.boundjid.domain)
	    #registro de los event handlers y binding con las funciones de la clase 
	    self.add_event_handler("session_start", self.start)
	    self.add_event_handler("connection_failed", self.connection_failed)
	    self.add_event_handler("message", self.message)
	    self.add_event_handler("groupchat_message", self.muc_message)
	    self.add_event_handler("failed_auth",self.failed_auth)
	    self.add_event_handler("pubsub_config",self.pubsub_config)
	    self.add_event_handler("groupchat_message",self.muc_message)
	    #self.add_event_handler("roster_update",self.get_roster)
	    #registro de los plugins xep
	    self.register_plugin('xep_0030') # Service Discovery
	    self.register_plugin('xep_0050') #adhoc commands
	    self.register_plugin('xep_0004') # Data forms
	    self.register_plugin('xep_0045') # muc 
	    self.register_plugin('xep_0066') # Out-of-band Data
	    self.register_plugin('xep_0077') # in band registration
	    self.register_plugin('xep_0092') # system versions


	async def start(self, event):
		print("WAITING FOR ROSTER")
		self.send_presence()
		await self.get_roster()
		self.send_message(mto=global_destino,mbody=pojo2,mtype='chat')
		#self.menu()

	

	#en caso que el servidor niegue las credenciales
	def failed_auth(self, event):
		print("FAILED AUTHENTICATION WITHE CREDENTIALS PROVIDED")


	#Manejo de unirse a grupo
	def joinChatRoom(self, room, nick):
		print("JOINING CHAT ROOM")
		self.room = room
		self.nick = nick
		self.plugin['xep_0045'].join_muc(self.room,
                                     self.nick)




	# def roster_update(self,msg):
	# 	print("ROSTER UPDATED")
	# 	#print(event)

	#manejo del evento al recibir mensaje deirecto
	def message(self,msg):
		print("SOY EL NODO "+node + " RECIBI ESTE MENSAJE :"+msg['body'] + " de : "+msg['from'].bare)
		print("Lo trate de hacer json")
		# print(msg['body']['origin'])
		# print(msg['body']['dest'])
		# print(msg['body']['saltos'])
		# print(msg['body']['message'])

		js = json.loads(msg['body'])
		print(js)
		print(js['origin'])
		print(js['dest'])
		print(js['saltos'])
		print(js['message'])

		
		if(global_user== js['dest']):
			print("YO SOY EL DESTINATARIO")
		else:
			print("Evaluar a quien retransmitir***")

			newmsg=  {"origin": js['origin'],
	           "dest": js['dest'],
	           "saltos":js['saltos']+1 ,
	           "message":js['message']}
			print(newmsg)

			self.send_message(mto="nodob@alumchat.fun",mbody=newmsg,mtype='chat')
			print("RETRANSMITIRE ")



	#manejo del evento al recibir mensaje grupal (multi user chat)
	def muc_message(self,msg):
		print("RECIBI ESTE MENSAJE de un grupo" +msg['body'].bare)
		##print(msg['body'])


	def pubsub_config(self,event):
		print("RECIBI UN PUBSUB CONFIG")

	#manejo de envio de mensajes
	def sendMessage(self,msg,dest):
		print("Soy : "+self.jid+" y Enviare el mensje "+msg+" a "+dest	)
		self.send_message(mto=dest,
                          mbody=msg,
                          mtype='chat')

	#manejo de error de connexion
	def connection_failed(self,event):
		print("CONNECTION FAILED TRY AGAIN (TRYING TO CONNECT WITH CREDENTIALS:  "+self.jid+":"+self.password+")")

	
	
xmpp= ""

def searchpath(origin, destination):
	print("calculating min path FROM: "+ origin + " TO: "+ destination)


#MEnu de registro/ login
while (seleccion !="2"):
	seleccion = input(menu1)
	print("UD SELCCIONO : " + seleccion)
	if seleccion =="1":
		global_user="nodoa@alumchat.fun"
		global_password="computadora"
		#global_destino="nodob@alumchat.fun"
		#global_user=  input ("INGRESE SU USUARIO \n")
		#global_password=  input("INGRESE SU CONTRASEÑA\n")
		#global_message= input("INGRESE EL MENSAJE A ENVIAR\n")
		global_destino= input("INGRESE EL DESINATARIO\n")
		xmpp = chatClient(global_user, global_password)

		pojo2= {"origin": global_user,
           "dest": global_destino,
           "saltos": 1,
           "message":global_message}
		
		pojo2= str(pojo2)
		pojo2 =pojo2.replace("'",'"')
		#Para encontrar el nodo que corresponde a el emisor
		keys = [k for k, v in alias.items() if v == global_user]
		print("SI NO ESTOY MAL, con ese login, tu nodo deberia ser")
		print(keys[0])
		node= keys[0]

		#Para encontrar el nodo que corresponde al destinatario
		keys2 = [k for k, v in alias.items() if v == global_destino]
		print("SI NO ESTOY MAL, con ese destinatario, su nodo deberia ser")
		print(keys2[0])
		node_dest= keys2[0]

		print("TUS VECINOS SON: ")
		print(rutas[node])

		searchpath(node,node_dest)


		seleccion="2"

	elif seleccion =="2":
		exit()
	else:
		print("SELECCION INVALIDA")


print("INICIANDO SESION CON ")
print("CREDENCIALES: "+global_user +" ; "+ global_password)

xmpp.connect()
xmpp.process()

