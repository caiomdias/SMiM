# -*- coding: utf-8 -*-

## problemas:
## De aguma maneira a resposta nao esta sendo atualizada para vazio depois que o servidor responde


import socket, pickle, time, psutil as ps

GIGAFACTOR = float(1<<30)

def formatCpuInfoPercent(res):
    c = 1
    
    for i in range(0, len(res)):
        print("Porcentagem de CPU no nucleo", c, "usada:", res[i], "%")
        c +=1


# Informações de CPU
def formatCpuInfo(info):
    print("-------    Informações da CPU da sua maquina: ")
    print("-------    Nome / modelo:", info[0])
    print("-------    Tipo de arquitetura:", info[1])
    print("-------    Plavra do processador:", info[2])
    print("-------    Frequencia total da CPU:", info[3])
    print("-------    Frequencia atual da CPU:", info[4])
    print("-------    Frequencia minima da CPU:", info[5])
    print("-------    Numero de nucleos fisicos", info[6])
    print("-------    Numero de nucleos logicos", info[7])

# Cria o socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
temp = 0

try:
    # Tenta se conectar ao servidor
    s.connect((socket.gethostname(), 14562))

    while True:
        
        print('-------    Escolha uma operação.')
        print('-------    1 Percentual de memoria RAM.')
        print('-------    2 Percentual deu so da CPU.')
        print('-------    3 Percentual deu so de Disco.')
        print('-------    4 Informações da CPU.')
        print('-------    5 IP da maquina.')
        print('-------    6 Informações sobre um arquivo.')
        print('-------    fim para sair.')
        print('')
        msg = input('>>> ')
        print('')


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
            
            print("Porcentagem de memoria usada:", res_mem_percent[0],"%")
            print('')


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
            
            print("Porcentagem de disco usada:", res_disk_percent[0],"%")
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
            print('')


        # Retorna o ip da maquina
        if msg == '5':
            
            # Envia mensagem vazia apenas para indicar a requisição
            s.send(msg.encode('ascii'))

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_ip = pickle.loads(bytes)
            
            print('Ip da maquina:', res_ip[0])
            print('')


        # Retorna as informações de um arquivo com base no path.
        if msg == '6':
            print('Por favor, digite o caminho do arquivo.')
            print('')
            path = input('>>> ')

            msg_to_send = msg + ',' + path
            # Envia mensagem vazia apenas para indicar a requisição
            s.sendall(msg_to_send.encode('ascii'), )

            # Recebe a resposta do servidor.
            bytes = s.recv(1024)

            # Converte os bytes para lista
            res_ip = pickle.loads(bytes)



except Exception as erro:
    print(str(erro))

# Fecha o socket
s.close()

input("Pressione qualquer tecla para sair...")
