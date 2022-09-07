import asyncio
import logging
from aioconsole import aprint
from datetime import datetime

import slixmpp
import networkx as nx
import matplotlib.pyplot as plt
import ast

class Client(slixmpp.ClientXMPP):
    def __init__(self, jid, password, algoritmo, nodo, nodes, names, graph, graph_dict, source):
        super().__init__(jid, password)
        self.received = set()
        self.algoritmo = algoritmo
        # self.topo = topo
        self.names = names
        self.graph = graph
        # Cambio en vez de recibir toda la red recibe su nodo y nodos asociados
        self.nodo = nodo
        self.nodes = nodes
        # self.nodos = nodos
        self.schedule(name="echo", callback=self.echo_message, seconds=5, repeat=True)
        
        # Manejar los eventos
        self.connected_event = asyncio.Event()
        self.presences_received = asyncio.Event()

        # Manejar inicio de sesion y mensajes
        self.add_event_handler('session_start', self.start)
        self.add_event_handler('message', self.message)
        
        # Plugins
        self.register_plugin('xep_0030') # Service Discovery
        self.register_plugin('xep_0045') # Multi-User Chat
        self.register_plugin('xep_0199') # Ping


    # Iniciar sesion
    async def start(self, event):
        self.send_presence() 
        await self.get_roster()
        self.connected_event.set()

    # Recibir mensajes
    async def message(self, msg):
        if msg['type'] in ('normal', 'chat'):
            #await aprint("\n{}".format(msg['body']))
            await self.reply_message(msg['body'])

    # Esta funcion la pueden usar para reenviar sus mensajes
    async def reply_message(self, msg):
        message = msg.split('|')
        if message[0] == '1':
            # Verificar si el mensaje es para mi
            if message[2] == self.jid:
                print("MENSAJE RECIBIDO --> " +  message[6])
            else:
                if int(message[3]) > 0:
                    lista = message[4].split(",")
                    if self.nodo not in lista:
                        message[4] = message[4] + "," + str(self.nodo)
                        message[3] = str(int(message[3]) - 1)
                        StrMessage = "|".join(message)
                        for i in self.nodes:
                            self.send_message(
                                mto=self.names[i],
                                mbody=StrMessage,
                                mtype='chat' 
                            )  
                else:
                    pass
            
        elif message[0] == '2':
            print('Actualizando informacion...')
            
        elif message[0] == '3':
            if message[6] == '':
                now = datetime.now()
                timestamp = datetime.timestamp(now)
                mensaje = msg + str(timestamp)
                self.send_message(
                            mto=message[1],
                            mbody=mensaje,
                            mtype='chat' 
                        )
            else:
                difference = float(message[6]) - float(message[4])
                self.graph[self.nodo][message[5]]['weight'] = difference
        else:
            pass

    def echo_message(self):
        for i in self.nodes:
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            mensaje = "3|" + str(self.jid) + "|" + str(self.names[i]) + "||"+ str(timestamp) +"|" + str(i) + "|"
            self.send_message(
                        mto=self.names[i],
                        mbody=mensaje,
                        mtype='chat' 
                    )