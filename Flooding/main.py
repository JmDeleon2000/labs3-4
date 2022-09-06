import getpass
from aioconsole.stream import aprint
from optparse import OptionParser

from client import Client
from aioconsole import ainput

import json
import networkx as nx
import matplotlib.pyplot as plt

# Funcion para cargar los archivos de configuracion
def loadConfig():
    with open("topo-demo.txt", 'r') as f:
        topology = json.load(f)

    with open("names-demo.txt", 'r') as f:
        names = json.load(f)

    print(str(topology))
    print(str(names))

    return topology, names

# Funcion para conocer mi nodo y sus nodos asociados
def getNodes(topo, names, user):
    for key, value in names["config"].items():
        if user == value:
            return key, topo["config"][key]

def getGraph(topo, names, user):
    '''Build graph in python a dict'''
    
    graph = {}
    source = None

    for key, value in topo['config'].items():
        graph[key] = {}
        for node in value:
            graph[key][node] = float('inf') 
            if names['config'][node] == user:
                source = node
    
    return graph, source


def pruebaGrafo(topo, names):
    G = nx.DiGraph()
    G.add_nodes_from(G.nodes(data=True))
    G.add_edges_from(G.edges(data=True))
    for key, value in names["config"].items():
        G.add_node(key, jid=value)
        
    for key, value in topo["config"].items():
        for i in value:
            G.add_edge(key, i, weight=1)
    
    return G
    
# Funcion para manejar el cliente
async def main(xmpp: Client):
    corriendo = True
    while corriendo:
        print("""
         ------------------------------------------------
        |                                                |
        |                   ALUMCHAT                     |         
        |                                                | 
         ------------------------------------------------
        1. Enviar un mensaje
        2. Salir
        """)
        opcion = await ainput("Ingresa la opción que deseas realizar: ")
        if opcion == '1':
            destinatario = await ainput("Ingrese el nombre del usuario al que quieres enviar un mensaje:  ")
            activo = True
            while activo:
                mensaje = await ainput("Escribe el mensaje: ")
                if (mensaje != 'volver') and len(mensaje) > 0:
                    mensaje = "1|" + str(xmpp.jid) + "|" + str(destinatario) + "|" + str(xmpp.graph.number_of_nodes()) + "||" + str(xmpp.nodo) + "|" + str(mensaje)
                    for i in xmpp.nodes:
                        xmpp.send_message(
                            mto=xmpp.names[i],
                            mbody=mensaje,
                            mtype='chat' 
                        )
        elif opcion == '2':
            corriendo = False
            xmpp.disconnect()
        else:
            pass


if __name__ == "__main__":

    optp = OptionParser()

    optp.add_option("-j", "--jid", dest="jid")
    optp.add_option("-p", "--password", dest="password")
    optp.add_option("-a", "--algoritmo", dest="algoritmo")
    
    opts, args = optp.parse_args()

    topo, names = loadConfig()
    if opts.jid is None:
        opts.jid = input("Ingrese su nombre de usuario: ")
    if opts.password is None:
        opts.password = getpass.getpass("Ingrese su contraseña: ")
    if opts.algoritmo is None:
        opts.algoritmo = "1"

    graph_dict, source = getGraph(topo, names, user=opts.jid)

    nodo, nodes = getNodes(topo, names, opts.jid)

    graph = pruebaGrafo(topo, names)

    xmpp = Client(opts.jid, opts.password, opts.algoritmo, nodo, nodes, names["config"], graph, graph_dict, source)
    xmpp.connect() 
    xmpp.loop.run_until_complete(xmpp.connected_event.wait())
    xmpp.loop.create_task(main(xmpp))
    xmpp.process(forever=False)
    