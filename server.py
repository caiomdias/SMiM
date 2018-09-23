# -*- coding: utf-8 -*-

# Problemas:
# Tem que configurar na opção 5, "get IP" a rede certa para pegar o IP

# Servidor
import socket
import pickle
import cpuinfo
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
    return temp


# Tamanho de um diretorio
def getDirSize(path):

    ## calcula o tamano de um diretorio
    if os.path.isdir(path):
        somador = 0

        lista = os.listdir(path)

        for i in lista:
            p = os.path.join(path, i)
            if os.path.isfile(p):
                somador = somador + os.stat(p).st_size
        return somador / 1000
    else:
        return "O diretório", '\'' + path + '\'', "não existe."


# Retorna o pid de um processo com base no nome do mesmo
def getPIDByName(name):

    lp = ps.pids()

    lista_pid = []

    for i in lp:
        p = ps.Process(i)

        if p.name() == name:
            lista_pid.append(str(i))

    if len(lista_pid) > 0:
        return lista_pid

    else:
        return "não está executando no momento."


# Retorna os dados de um PID
def getProcessInformation(pid):
    return ps.Process(int(pid))
    


def sendResponse(res):
    # Verifica se a resposta ja é uma lista.
    if type(res) is list:
        # Prepara a lista para o envio
        bytes_resp = pickle.dumps(res)

        # Envia os dados
        cliente.send(bytes_resp)

    else:
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
    msg = cliente.recv(2048)

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

    # retornar as informações do arquivo
    if msg.decode('ascii') == '6':
        path = cliente.recv(1024)
        decode_path = path.decode('ascii')
        list_files = os.listdir(decode_path)
        sendResponse(list_files)

    # retornar as informações de um diretorio
    if msg.decode('ascii') == '7':
        path = cliente.recv(1024)
        decode_path = path.decode('ascii')

        response = []

        # Retorna o tamanho do diretorio
        dir_size = getDirSize(decode_path)
        response.append(dir_size)
        
        # Data de criação do repositorio
        create_date = os.path.getmtime(path)    
        response.append(create_date)
        
        sendResponse(response)
    
    # retornar o PID de um processo
    if msg.decode('ascii') == '8':
        process_name = cliente.recv(1024)
        decode_name = process_name.decode('ascii')

        response = []
        # Retorna o pid do processo
        pid = getPIDByName(decode_name)
        response.append(pid[0])        

        # Retorna as informações do pid
        process_info = getProcessInformation(int(pid[0]))
        response.append(process_info)

        sendResponse(response)
    
    # Retorna as informações da rede em que a maquina se encontra
    if msg.decode('ascii') == '9':
        interfaces = ps.net_if_addrs()
        sendResponse(interfaces)



# Fecha socket do servidor
socket_servidor.close()
