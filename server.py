import socket
import threading
from queue import Queue, LifoQueue

def init_server(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    # Bind the socket to the port
    print(f'Empezando en {host} puerto {port}')
    sock.bind((host, port))
    # Listen for incoming connections
    sock.listen(1)
    return sock

def connect(sock, queue_fila, queue_columna, queue_angulo_1, queue_angulo_2):
    try:
        while True:
            # Wait for a connection
            print('Esperando una conexión...')
            socket_cliente, client_address = sock.accept()
            print('Se ha conectado', client_address)
            # Receive the data in small chunks and retransmit it
            try: 
                thread_escuchar = threading.Thread(target=escuchar,args=(socket_cliente, queue_angulo_1, queue_angulo_2,),daemon=True)
                thread_enviar = RepeatTimer(0.05, enviar,args=(socket_cliente, queue_fila, queue_columna,))
                thread_escuchar.start()
                thread_enviar.start()
            except ConnectionError:
                print(f"Se ha desconectado el cliente {client_address}")
                socket_cliente.close() 
    finally:
        print(f"Se ha desconectado el servidor")
        sock.close() 

def escuchar(socket_cliente, queue_x_ref, queue_y_ref):
    while True:
        data = socket_cliente.recv(1024)
        if data:
            data = data.decode()
            posicion = str(data).split(",")
            x_ref = float(posicion[0])
            y_ref = float(posicion[1])
            queue_x_ref.append(x_ref)
            queue_y_ref.append(y_ref)

def enviar(socket_cliente, queue_fila, queue_columna):
    fila = queue_fila.get()
    columna = queue_columna.get()
    #print(queue_columna.qsize())
    if fila is not None:
        # example num2fixstr(19,3) returns '019'
        d = 3
        columna = '%0*d' % (d,int(columna))
        fila = '%0*d' % (d,int(fila))
        string = f"{fila},{columna}"
        print(f"Enviando: {string}")
        socket_cliente.send(string.encode())
   
class RepeatTimer(threading.Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args,**self.kwargs)
