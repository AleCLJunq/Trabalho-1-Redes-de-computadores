import socket
import threading, pyaudio, pickle,struct
import time
import classes

SIZE = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "FINALIZAR CONEXAO"
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

mensagem = '\n Para interagir com o programa digite: \n\n\
    "L" para receber a lista de musicas.\n\
    "C" para tocar musicas em um cliente remoto.\n\
    "R" para permitir que outro cliente toque nesse.\n\
    "P" para pausar uma música tocando nesse computador.\n\
    "T" para voltar a tocar uma música pausada\n\
    "F" para finalizar o programa'
stream = 0

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def abreConexao():
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(2),
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=SIZE)
    return stream

stream = abreConexao()

def tocaMusica():
    data = b""

    tamanhoPayload = struct.calcsize("Q")
    enviouTudo = True

    while enviouTudo:
        try:
            if stream.is_active():
                while len(data) < tamanhoPayload:
                    pacote = client.recv(4*1024) # 4K
                    if not pacote: 
                        break
                    data+=pacote
                tamanhoMsgEmpacotada = data[:tamanhoPayload]
                data = data[tamanhoPayload:]
                tamanhoMsg = struct.unpack("Q",tamanhoMsgEmpacotada)[0]
                while len(data) < tamanhoMsg:
                    data += client.recv(4*1024)
                frameInfo = data[:tamanhoMsg]
                data  = data[tamanhoMsg:]
                frame = pickle.loads(frameInfo)
                info = frame.info
                stream.write(info)
                if info == b'': 
                    print('Musica finalizada.\n')
                    time.sleep(2)
                    enviouTudo = False
        except:
            break
    

def recebeLista():
    msg = 'RECUPERAR LISTA'
    send(msg)
    print(client.recv(SIZE).decode(FORMAT))
    indc = input()
    send(indc)
    thread = threading.Thread(target=tocaMusica)
    thread.start()

def tocaOutro():
    msg = 'CONECTAR OUTRO CLIENTE'
    send(msg)
    print(client.recv(SIZE).decode(FORMAT))
    indc = input()
    send(indc)
    print(client.recv(SIZE).decode(FORMAT))    
    indc = input()
    send(indc)
    print('Tocando no cliente escolhido. \n')

def recebeCliente():
    print('Esperando cliente escolher a musica')
    thread = threading.Thread(target=tocaMusica)
    thread.start()

def fechaConexao():
    msg = DISCONNECT_MESSAGE
    send(msg)

def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)


print('Bem vindo ao trabalho 1 de Redes de Computadores 23/1!')

while True:
    print(mensagem)
    escolha = input()
    try:
        
        if escolha == 'L':
            if stream != 0:
                stream.close()
            stream = abreConexao()
            recebeLista()

        elif escolha == 'C':
            tocaOutro()

        elif escolha == 'R':
            recebeCliente()

        elif escolha == 'P':
            if stream == 0:
                raise Exception("Nenhuma musica tocando, selecione outra opção")
            else: stream.stop_stream()
            
        elif escolha == 'T':
            if stream == 0:
                raise Exception("Nenhuma musica tocando, selecione outra opção")
            else: stream.start_stream()    

        elif escolha == 'F':
            print('Finalizando conexão.')
            fechaConexao()
            break
        
        else:
            raise Exception("Opção invalida, tente novamente.")
        
    except Exception as e: print(e)


client.close()