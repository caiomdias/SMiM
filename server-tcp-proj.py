# -*- coding: utf-8 -*-
# Servidor
import socket, pickle
import psutil as ps
import os


# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtem o nome da máquina
host = socket.gethostname()

porta = 15320

# Associa a porta
socket_servidor.bind((host, porta))

# Escutando...
socket_servidor.listen(1)

print("Servidor de nome", host, "esperando conexão na porta", porta)

# Aceita alguma conexão
(cliente, addresse) = socket_servidor.accept()

print("Conectado a:", str(addresse))


# Porcentagem do uso de memoria
def getMemoryUsagePercent():
    memory_used = ps.virtual_memory().percent
    print("Porcentagem de memoria usada:", memory_used,"%")
    return memory_used

def sendResponse(res):
    # Gera a lista de resposta
    resposta = []

    # Apenda a resposta para o array de respostas
    resposta.append(res)

    # Prepara a lista para o envio
    bytes_resp = pickle.dumps(resposta)

    # Envia os dados
    cliente.send(bytes_resp)

while True:
    # Recebe pedido do cliente:
    msg = cliente.recv(1024)

    print('Connection handled')

    if msg.decode('ascii') == 'fim':
        break

    if msg.decode('ascii') == '1':
        res = getMemoryUsagePercent()
        sendResponse(res)
    

# Fecha socket do servidor e cliente
# cliente.close()
socket_servidor.close()