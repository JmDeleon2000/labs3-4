import json
import re



def dvr(cuerpo):

    return True, 'destinatario', 'mensaje'


#f, a, b = dvr(msg['body'])
#if f:
#    #reenviar
#    pass
#else: 
#    #no reenviar
#    pass


with open('PYTHON COU/topo-demo.txt', 'r') as r:
    s = r.read()
    s = re.sub(r'\'', '\"', s)
    e = json.loads(s)
    print(e)
    print(e['type'])
    print(e['config'])
    print(e['config']['A'])