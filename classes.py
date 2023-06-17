import os

class ListaDeMusicas:
    def __init__(self, pastaMusicas = ''):
        self.listaMusicas = []

    def montaLista(self, nomePasta):
        for nomeArq in os.listdir(nomePasta):
            if nomeArq.endswith('.wav'):
                self.listaMusicas.append(nomeArq)
    def enviaLista(self):
        contador = 0
        mensagem = 'Selecione qual música deseja tocar indicando seu índice.\n'
        for msc in self.listaMusicas:
            contador += 1
            mensagem += f'{contador}.{msc.rstrip(".wav")}\n'
        return mensagem
   
    def retornaLista(self):
        return self.listaMusicas

class frame:
    def __init__(self, estado = 'TOCANDO', info = b''):
        self.estado = estado
        self.info = info

class clientesConectados:
    def __init__(self, conexoes = []):
        self.conexoes = conexoes

    def adicionaConn(self, conn):
        self.conexoes.append(conn)

    def removeConn(self, conn):
        self.conexoes.remove(conn)

    def enviaConectados(self):
        contador = 0
        mensagem = 'Selecione o cliente que tocará a música \n'
        for cone in self.conexoes:
            contador += 1
            mensagem += f'{contador}.{cone[1]}\n'
        return mensagem
    
    def retornaConexoes(self):
        return self.conexoes