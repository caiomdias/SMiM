# -*- coding: utf-8 -*-
import socket, pickle

GIGAFACTOR = float(1<<30)

# Função que imprime a dado formatada
def showInfo(list):
    print('Disco disponivel:', format(str('{:.2f}'.format(list[0] / GIGAFACTOR) + ' GB')))


# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp = 0

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 15320))

    while True:

        print('-------    Escolha uma operação.     --------')
        print('-------    1 Dados de memoria RAM.   --------')
        print('-------    2 Dados da CPU.           --------')
        print('-------    3 Dara dados do Disco.    --------')
        print('-------    4 Dara IP da maquina.     --------')
        msg = input('>>>')

        if msg == 'fim':
            s.send(msg.encode('ascii'))


        if msg == '1'
           # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

        # Converte os bytes para lista
        lista = pickle.loads(bytes)

        print(lista)

        # Finaliza o lado do cliente

except Exception as erro:
    print(str(erro))

# Fecha o socket
s.close()

input("Pressione qualquer tecla para sair...")
