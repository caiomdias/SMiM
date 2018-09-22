# -*- coding: utf-8 -*-

# problemas:
# De aguma maneira a resposta nao esta sendo atualizada para
# vazio depois que o servidor responde


import socket
import pickle
import os
import time
import psutil as ps

GIGAFACTOR = float(1 << 30)


def formatCpuInfoPercent(res):
    c = 1

    for i in range(0, len(res)):
        print('\n'+'\t'+"Porcentagem de CPU no nucleo", c, "usada:", res[i], "%")
        c += 1


# Informações de CPU
def formatCpuInfo(info):
    print('\n'+'\t'+"Informações da CPU da sua maquina:")
    print('\t'+"Nome / modelo:", info[0])
    print('\t'+"Tipo de arquitetura:", info[1])
    print('\t'+"Plavra do processador:", info[2])
    print('\t'+"Frequencia total da CPU:", info[3])
    print('\t'+"Frequencia atual da CPU:", info[4])
    print('\t'+"Frequencia minima da CPU:", info[5])
    print('\t'+"Numero de nucleos físicos:", info[6])
    print('\t'+"Numero de nucleos lógicos:", info[7], ''+'\n')

def getFileInformation(path, list_files):

    dic_files = {}

    for i in list_files:
        if os.path.isfile(i):
            dic_files[i] = []
            dic_files[i].append(os.stat(i).st_size)
            dic_files[i].append(os.stat(i).st_atime)
            dic_files[i].append(os.stat(i).st_mtime)

    titulo = '{:11}'.format("Tamanho")  # 10 caracteres + 1 de espaço

    # Concatenar com 25 caracteres + 2 de espaços
    titulo = titulo + '{:27}'.format("Data de Modificação")

    # Concatenar com 25 caracteres + 2 de espaços
    titulo = titulo + '{:27}'.format("Data de Criação")

    titulo = titulo + "Nome"

    print('\n'+'\t'+titulo)

    for i in dic_files:
        kb = dic_files[i][0] / 1000
        tamanho = '{:10}'.format(str('{:.2f}'.format(kb) + ' KB'))
        print('\t'+tamanho, time.ctime(dic_files[i][2]), " ", time.ctime(dic_files[i][1])," ", i)
    print('')


# Formata os dados de um diritorio
def formatDirInformation(path, dir_size, create_date):

    dir_name = os.path.split(path)

    # Formata os dados
    dir_size = '{:16}'.format(str('{:.2f}'.format(dir_size) + ' KB'))
    create_date = '{:29}'.format(time.ctime(create_date))

    #formata titulo
    titulo = '{:17}'.format("Tamanho")  # 13 caracteres + 1 de espaço

    titulo = titulo + '{:30}'.format("Data de Criação")

    titulo = titulo + '{:30}'.format("Nome do diretorio")

    # Mostra informações formatadas
    print('\n'+'\t'+titulo)
    print('\t'+dir_size, create_date, dir_name[1] + '\n')

# Formata os dados de um PID
def formatProcessInformation(pid, current_process):
    print('\n'+'\t'+"PID", pid)
    print('\t'+"Nome:", current_process.name())
    print('\t'+"Executável:", current_process.exe())
    print('\t'+"Tempo de criação:", time.ctime(current_process.create_time()))
    print('\t'+"Tempo de usuário:", current_process.cpu_times().user, "s")
    print('\t'+"Tempo de sistema:", current_process.cpu_times().system, "s")
    print('\t'+"Percentual de uso de CPU:", current_process.cpu_percent(interval=1.0), "%")
    perc_mem = '{:.2f}'.format(current_process.memory_percent())
    print('\t'+"Percentual de uso de memória:", perc_mem, "%")

    # RSS: Resident set size e VMS: Virtual Memory Size
    mem = '{:.2f}'.format(current_process.memory_info().rss / 1024 / 1024)
    print('\t'+"Uso de memória:", mem, "MB")
    print('\t'+"Número de threads:", current_process.num_threads(), '' + '\n')


# Formata as informações de redes
def formatNetworkInformation(interfaces):
    nomes = []

    # Obtém os nomes das interfaces primeiro
    for i in interfaces:
        nomes.append(str(i))

    # Depois, imprimir os valores:
    for i in nomes:
        print('\n'+i+":")

        for j in interfaces[i]:
            #print("\t"+str(j))
            print("\t"+'Endereço IP: '+str(j.address))
            print("\t"+'Familia: '+str(j.family))
            print("\t"+'Netmask: '+str(j.netmask)+'\n')

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp = 0

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 14562))

    while True:

        print('\n'+'\t'+'-------    Escolha uma operação.'+'\n')
        print('\t'+'-------    1 Percentual de memoria RAM.')
        print('\t'+'-------    2 Percentual deu so da CPU.')
        print('\t'+'-------    3 Percentual deu so de Disco.')
        print('\t'+'-------    4 Informações da CPU.')
        print('\t'+'-------    5 IP da maquina.')
        print('\t'+'-------    6 Informações de arquivos de um diretorio.')
        print('\t'+'-------    7 Informações sobre um diretorio.')
        print('\t'+'-------    8 Informações sobre um processo.')
        print('\t'+'-------    9 Informações sobre a rede presente.')
        print('\t'+'-------    fim para sair.'+'\n')
        msg = input('>>> ')

        # Finaliza o lado do cliente
        if msg == 'fim':
            s.send(msg.encode('ascii'))
            break

        # Retorna porcentagem de memoria
        if msg == '1':

            # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_mem_percent = pickle.loads(bytes)

            print('\n'+'\t'+"Porcentagem de memoria usada:", res_mem_percent[0], "%"+'\n')

        # Retorna porcentagem de uso da CPU
        if msg == '2':

            # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_cpu_percent = pickle.loads(bytes)

            formatCpuInfoPercent(res_cpu_percent)
            print('')

        # Retorna porcentagem de uso de disco
        if msg == '3':

            # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_disk_percent = pickle.loads(bytes)

            print('\n'+'\t'+"Porcentagem de disco usada:", res_disk_percent[0], "%"+'\n')
            print('')

        # Retorna informações da CPU
        if msg == '4':

            # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_cpu_info = pickle.loads(bytes)

            formatCpuInfo(res_cpu_info)

        # Retorna o ip da maquina
        if msg == '5':

            # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_ip = pickle.loads(bytes)

            print('\n'+'\t'+'Ip da maquina:', res_ip[0], ''+'\n')

        # Retorna as informações de um arquivo com base no path.
        if msg == '6':
            s.send(msg.encode('ascii'))

            # recebe e envia o path para o servidor
            print('\n'+'\t'+'Por favor, digite o caminho do arquivo.\n')
            path = input('>>> ')
            s.send(path.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_files = pickle.loads(bytes)

            getFileInformation(path, res_files)

        
        # Retorna as informações de um diretorio com base no path.
        if msg == '7':
            s.send(msg.encode('ascii'))

            # recebe e envia o path para o servidor
            print('\n'+'\t'+'Por favor, digite o caminho de um diretorio.\n')
            path = input('>>> ')
            s.send(path.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_files = pickle.loads(bytes)

            formatDirInformation(path, res_files[0], res_files[1])

        # Retorna as informações de um processo com base no seu nome.
        if msg == '8':
            s.send(msg.encode('ascii'))

            # recebe e envia o path para o servidor
            print('\n'+'\t'+'Por favor, digite o nome do processo.\n')
            path = input('>>> ')
            s.send(path.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_process = pickle.loads(bytes)
            
            formatProcessInformation(res_process[0], res_process[1])

        # Retorna as informações da rede em que a maquina se encontra.
        if msg == '9':
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(2048)

            # Converte os bytes para lista
            res_network = pickle.loads(bytes)
            
            formatNetworkInformation(res_network[0])


except Exception as erro:
    print(str(erro))

# Fecha o socket
s.close()

input("Pressione qualquer tecla para sair...")
