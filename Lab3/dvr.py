import json
import re


neighbours = {}
JIDs = {}
nodes = {}
tables = {}
table = {}

with open('topo1.txt', 'r') as r:
    s = r.read()
    s = re.sub(r'\'', '\"', s)
    e = json.loads(s)
    neighbours = e['config']


with open('names1.txt', 'r') as r:
    s = r.read()
    s = re.sub(r'\'', '\"', s)
    e = json.loads(s)
    nodes = {v:i for i,v in e['config'].items()}
    JIDs = e['config']


def sendInitTable(user):
    global table
    myNode = nodes[user]
    newTable = {}
    newTable[myNode] = [0, myNode]
    
    for i, v in neighbours.items():
        if (myNode in v):
            newTable[i] = [10000, myNode]
    table = newTable
    return [JIDs[i] for i in neighbours.keys() if myNode in neighbours[i]], json.dumps(newTable)

def dvr(body, user):
    global table
    e = json.loads(body)
    if 'table' in e.keys():
        myNode = nodes[user]
        if e['node'] in neighbours[myNode]:
            tables[e['node']] = e['table']

        
        newTable = {}
        newTable[myNode] = [0, myNode]
        
        for i, v in neighbours.items():
            if (myNode in v):
                newTable[i] = [1, myNode]
        for i in neighbours.keys():
            if i not in newTable.keys():
                n = howToGetTo(i)
                if (i == n):
                    if i in table.keys():
                        newTable[i] = table[i]
                    else:
                        newTable[i] = [10000, myNode]
                else:
                    newTable[i] = [newTable[n][0]+1, n]
                    
        
        changed = (newTable != table)
        table = newTable

        if e['response']:
            return False, '', ''
        msg = json.dumps({'table':table, 
        'node':nodes[user], 'response':not(changed)})
        return True, [JIDs[i] for i in neighbours.keys() if myNode in neighbours[i]], msg
    else:
        nodeRenv = howToGetTo(nodes[e['dest']])

        e['saltos']+=1
        e['distancia']+=1
        e['recorrido']+=f', {user}'

    return True, [JIDs[nodeRenv]], [json.dumps(e)]

def howToGetTo(n):
    out = n
    quickest = float('inf')
    for i, v in tables.items():
        if (n in v.keys()):
            eta = v[n][0]
            if eta < quickest:
                quickest = eta
                out = v[n][1]
    return out

#SE LLAMA CUANDO SE SABE QUE ESTE NODO NO ES EL DESTINATARIO
#f, msg, dests = dvr(msg['body'], global_user)
#if f:
#    for dest in dests: (puede que se envíe el mensaje a más de un destinatario, por eso se devuelve una lista)
#        reenviar msg a dest

# m = {'table':{'F':[0, 'F'], 'A':[4, 'F'], 'B':[7, 'F']},
#     'node':'F',
#     'response':False}

# f, d, m = dvr(json.dumps(m), 'foo@alumchat.xyz')
# print(f)
# print(d)
# print(m + '\n')


# m = {'table':{'C':[0, 'C'], 'A':[2, 'C'], 'D':[10, 'C'], 'G':[9, 'C']},
#     'node':'C',
#     'response':False}

# f, d, m = dvr(json.dumps(m), 'foo@alumchat.xyz')

# print(f)
# print(d)
# print(m + '\n')


# m = {'table':{'B':[0, 'B'], 'F':[2, 'B'], 'G':[9, 'G']},
#     'node':'B',
#     'response':False}

# f, d, m = dvr(json.dumps(m), 'foo@alumchat.xyz')
# print(f)
# print(d)
# print(m + '\n')

# m = {'dest':'bar@alumchat.xyz',
#     'origin':'foo@alumchat.xyz',
#     'saltos':1,
#     'distancia':1,
#     'recorrido':'',
#     'message':'lorem ipsum'}

# f, d, m = dvr(json.dumps(m), 'foo@alumchat.xyz')
# print(f)
# print(d)
# print(m)

