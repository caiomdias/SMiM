# -*- coding: utf-8 -*-



## Problemas:
## Tem que configurar na opção 5, "get IP" a rede certa para pegar o IP

# Servidor
import socket, pickle, cpuinfo
import psutil as ps
import os


# Cria o socket
socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Obtem o nome da máquina
host = socket.gethostname()

porta = 14562

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
    return memory_used


# Porcentagem do uso de CPU;
def getCpuUsagePercent(i):
    return ps.cpu_percent(interval=1, percpu=True)[i]


# Informações de CPU
def getCpuInfo(info):
    temp = []
    temp.append(info['brand'])
    temp.append(info['arch'])
    temp.append(info['bits'])
    temp.append(ps.cpu_freq().max)
    temp.append(ps.cpu_freq().current)
    temp.append(ps.cpu_freq().min)
    temp.append(ps.cpu_count(logical=False))
    temp.append(ps.cpu_count() - ps.cpu_count(logical=False))
    print(temp)
    return temp

def sendResponse(res):
    # Verifica se a resposta ja é uma lista.
    if type(res) is list:
         # Prepara a lista para o envio
        bytes_resp = pickle.dumps(res)

        # Envia os dados
        cliente.send(bytes_resp)

    # Gera a lista de resposta
    resposta = []
    print(res)
    # Apenda a resposta para o array de respostas
    resposta.append(res)

    # Prepara a lista para o envio
    bytes_resp = pickle.dumps(resposta)

    # Envia os dados
    cliente.send(bytes_resp)

while True:
    res = []
    # Recebe pedido do cliente:
    msg = cliente.recv(1024)

    print('Connection handled')

    if msg.decode('ascii') == 'fim':
        break

    # Percentual de memoria RAM
    if msg.decode('ascii') == '1':
        res = []
        res = getMemoryUsagePercent()
        sendResponse(res)
        

    # Percentual de uso da CPU
    if msg.decode('ascii') == '2':
        res = []
        for i in range(0, ps.cpu_count()):
            temp = getCpuUsagePercent(i)
            res.append(temp)
        
        sendResponse(res)


    # Percentual de uso de Disco
    if msg.decode('ascii') == '3':
        res = []  
        res = ps.disk_usage('.')      
        sendResponse(res.percent)


    # Informações da CPU
    if msg.decode('ascii') == '4':
        res = []
        info = cpuinfo.get_cpu_info()
        res = getCpuInfo(info)
        sendResponse(res)
    

    # Ip da maquina
    if msg.decode('ascii') == '5':
        dic_interfaces = ps.net_if_addrs()
        machine_ip = dic_interfaces['Ethernet'][1].address
        sendResponse(machine_ip)


        
 

# Fecha socket do servidor e cliente
socket_servidor.close()