import socket
import threading, wave,pickle,struct
import classes


SIZE = 2048
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "FINALIZAR CONEXAO"

listaMusicas = classes.ListaDeMusicas()
listaMusicas.montaLista(r'musicas')

clientesConn = classes.clientesConectados()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def enviaMusica(conn, indiceMusica, listaMusicas):
	try:
		arquivo = f'musicas\{listaMusicas[int(indiceMusica) - 1]}'
		wf = wave.open(arquivo, 'rb')
		data = None
		enviouTudo = True
		tocando = True
		while enviouTudo:
			if tocando:
				while enviouTudo:
					try:
						info = classes.frame()
						info.info = wf.readframes(SIZE)
						data = info
						a = pickle.dumps(data)
						message = struct.pack("Q", len(a)) + a
						conn.sendall(message)
						if len(data.info) < SIZE:
							enviouTudo = False
							break
					except:
						enviouTudo = False
	except:
		print('Formato invalido')

def handle_client(conn, addr):
	print(f"[NOVA CONEXÃO] {addr} conectado.")

	conectado = True
	while conectado:
		msg = conn.recv(SIZE).decode(FORMAT)
		print(f"[{addr}] {msg}")
		if msg:
			if msg == 'RECUPERAR LISTA':
				lista = listaMusicas.enviaLista()
				lista = lista.encode(FORMAT)
				conn.send(lista)
				indice = conn.recv(SIZE).decode(FORMAT)
				thread = threading.Thread(target=enviaMusica,args=(conn, indice, listaMusicas.retornaLista()))
				thread.start()
				
			elif msg == 'CONECTAR OUTRO CLIENTE':
				listaClientes = clientesConn.enviaConectados()
				listaClientes = listaClientes.encode(FORMAT)
				conn.send(listaClientes)
				indice = conn.recv(SIZE).decode(FORMAT)
				lista = listaMusicas.enviaLista()
				lista = lista.encode(FORMAT)
				conn.send(lista)
				indiceMsc = conn.recv(SIZE).decode(FORMAT)
				clienteEscolhido = 	clientesConn.conexoes[int(indice) - 1][0]		
				thread = threading.Thread(target=enviaMusica,args=(clienteEscolhido, indiceMsc, listaMusicas.retornaLista()))
				thread.start()

			elif msg == DISCONNECT_MESSAGE:
				conectado = False

	clientesConn.removeConn((conn,addr))
	print(f"[CONEXÃO FINALIZADA] {addr} se desconectou")
	conn.close()

def start():
	print(f"[ESCUTANDO] Servidor está esperando conexões em {SERVER}")
	server.listen()
	while True:
		conn, addr = server.accept()
		clientesConn.adicionaConn((conn,addr))
		thread = threading.Thread(target=handle_client,args=(conn,addr))
		thread.start()



print("[INICIALIZANDO] servidor está inicializando ...")
start()