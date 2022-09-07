
import logging
import asyncio
import re
#import time
import json
from slixmpp.exceptions import IqError, IqTimeout
from slixmpp import ClientXMPP
import dvr
import sys
#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if sys.platform == 'win32' and sys.version_info >= (3, 8):
     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#logging.basicConfig(level=logging.DEBUG,format='%(levelname)-8s %(message)s')

seleccion=""
global_user = ""
global_password=""
global_message=""
global_destino=""
node_dest=""
isSender = True 


# rutas={
# 	"A":['B','D'],
# 	"B":['C'],
# 	"D":['B']
# }

# alias= {
# 	"A":"nodoa@alumchat.fun",
# 	"B":"nodob@alumchat.fun",
# 	"C":"nodoc@alumchat.fun",
# 	"D":"couvid@alumchat.fun"
# }

menu1= "BIENVENIDA/ BEINVENIDO A ALUMNCHAT \n PRESIONE : \n 1) PARA LOGUEARSE CON UN USUARIO EXISTENTE\n 2) PARA SALIR \n"
menu2= "BIENVENIDA/ BEINVENIDO " +global_user +" \n PRESIONE : \n 1) PARA CERRAR SESION DE UN USUARIO EXISTENTE\n 2) PARA ELIMINAR A UN USUARIO EXISTENTE\n 3) PARA MOSTRAR TODOS LOS CONTACTOS Y SUS ESTADOS\n 4) PARA AGREGAR UN USUARIO A LOS CONTACTOS\n 5) PARA ENVIAR UN MENSAJE DIRECTO A UN USUARIO\n 6) PARA ENVIAR UN MENSAJE A UN GRUPO\n 7) PARA DEFINIR UN MENSAJE DE PRESCENCIA \n 8) PARA SALIR \n"

print("**LEER JSON de TOPOLOGIAS**")
with open('topo1.txt','r')as r:
	s = r.read()
	s = re.sub(r'\'' , '\"',s)
	e = json.loads(s)
	rutas2= e['config']

print(rutas2)

print("**LEER JSON de nombres**")
with open('names1.txt','r')as r:
	s = r.read()
	s = re.sub(r'\'' , '\"',s)
	e = json.loads(s)
	alias2= e['config']

print (alias2)


#obtiene la letra del nodo que corresponde
def getnode(address):
	keys = [k for k, v in alias2.items() if v == address]
	return keys[0]

#obtiene el listado de vecinos de cualquier nodo
def getneighbors(node):
	return rutas2[node]


print("TESTEARE EL GET NEIGHBORS")
print(getneighbors("A"))


#busca la letra que corresponde al siguiente nodo
def searchpath(origin, destination):
	print("calculating min path FROM: "+ origin + " TO: "+ destination)
	


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
	    
	    self.add_event_handler("failed_auth",self.failed_auth)
	   
	    #registro de los plugins xep
	    self.register_plugin('xep_0030') # Service Discovery
	    self.register_plugin('xep_0050') #adhoc commands
	    self.register_plugin('xep_0004') # Data forms
	    self.register_plugin('xep_0045') # muc 
	    self.register_plugin('xep_0066') # Out-of-band Data
	    self.register_plugin('xep_0077') # in band registration
	    self.register_plugin('xep_0092') # system versions


	async def start(self, event):
		print("CONNECTED...")
		self.send_presence()
		await self.get_roster()
		if (isSender):
			self.send_message(mto=global_destino,mbody=pojo2,mtype='chat')

	

	#en caso que el servidor niegue las credenciales
	def failed_auth(self, event):
		print("FAILED AUTHENTICATION WITHE CREDENTIALS PROVIDED")


	

	#manejo del evento al recibir mensaje deirecto
	def message(self, msg):
		print("SOY EL NODO "+node + " RECIBI ESTE MENSAJE :"+msg['body'] + " de : "+msg['from'].bare)


		
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
			newmsg=  {"origin": js['origin'],"dest": js['dest'],
			"saltos":js['saltos']+1 ,
			"message":js['message']}
			vecinos = getneighbors(node)
			for vecino in vecinos :
				print(alias2[vecino])
				self.send_message(mto=alias2[vecino],mbody=newmsg,mtype='chat')
		





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





#MEnu de registro/ login
while (seleccion !="2"):
	seleccion = input(menu1)
	print("UD SELCCIONO : " + seleccion)
	if seleccion =="1":
		global_user="nodoa@alumchat.fun"
		global_password="computadora"
		global_destino="nodob@alumchat.fun"
		global_user=  input ("INGRESE SU USUARIO \n")
		global_password=  input("INGRESE SU CONTRASEÑA\n")
		
		# Lso nodos pueden tener dos comportamientos: iniciar una conversacion o solo replicar mensajes
		inputDeenvio =input("Este nodo enviara un mensjae? Y/N ")
		if(inputDeenvio =="Y" or inputDeenvio =="y"):
			isSender = True
		else:
			isSender =False 

		if (isSender):
			global_message= input("INGRESE EL MENSAJE A ENVIAR\n")
			global_destino= input("INGRESE EL DESINATARIO\n")
		else:
			print("ESTE NODO SOLO SERVIRA DE REPLICADOR")
		

		pojo2= {"origin": global_user,
           "dest": global_destino,
           "saltos": 1,
           "message":global_message}
		#convierte el mensaje de objeto a string para ser enviado como cuerpo del mensaje
		pojo2= str(pojo2)
		pojo2 =pojo2.replace("'",'"')
		#Para encontrar el nodo que corresponde a el emisor
		
		print("SI NO ESTOY MAL, con ese login, tu nodo deberia ser")
		node= getnode(global_user)
		print(node)
		

		#Para encontrar el nodo que corresponde al destinatario
		
		print("SI NO ESTOY MAL, con ese destinatario, su nodo deberia ser")
		node_dest=getnode(global_destino)
		print(node_dest)
		
		print("TUS VECINOS SON: ")
		print(getneighbors(node))
		
		searchpath(node,node_dest)
		xmpp = chatClient(global_user, global_password)

		seleccion="2"

	elif seleccion =="2":
		exit()
	else:
		print("SELECCION INVALIDA")


print("INICIANDO SESION CON ")
print("CREDENCIALES: "+global_user +" ; "+ global_password)

xmpp.connect()
xmpp.process()


