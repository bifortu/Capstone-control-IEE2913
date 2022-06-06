import threading
import time
from stepper import init_stepper, move_stepper
from server import init_server, connect, enviar
from queue import Queue, LifoQueue
from controlador import Controlador
import image_processing  
import socket
from multiprocessing import Process

## Parameters
# ifconfig en terminal de raspberry entrega la direccion ip (host) 
# host = "172.20.10.2"  # Celular woolvett
host = "172.20.10.6"  # Celular benja
# host = "192.168.0.234" # Casa woolvett
# host = "192.168.1.137"  # Casa benja

port = 9000
step_1_pin = 11
dir_1_pin = 12
step_2_pin = 15
dir_2_pin = 16
resolucion_y = 640
resolucion_x = 480
frecuencia = 5000
direccion_1 = 0
direccion_2 = 0
treshold = 10
queue_fila = LifoQueue()
queue_columna = LifoQueue()
queue_x_ref = [320]
queue_y_ref = [120]
queue_x_c = LifoQueue()
queue_y_c = LifoQueue()
Kx = 0.3
Ky = 0.3

## Initialize the stepper
init_stepper(step_1_pin, step_2_pin, dir_1_pin, dir_2_pin)

## Initialize the server and make the connection
socket_servidor = init_server(host, port)
thread_interfaz = threading.Thread(target=connect,args=(socket_servidor, queue_fila, queue_columna, queue_x_ref, queue_y_ref,), daemon=True) # Damon >
thread_interfaz.start()

## Initialize the camera
thread_camara = threading.Thread(target=image_processing.encontrar_laser ,args=(queue_fila, queue_columna, queue_x_c, queue_y_c))
thread_camara.start()

## Controladores
origen_y = 240
origen_x = 320
control_y = Controlador(dir_1_pin, step_1_pin, frecuencia, ref=origen_y, queue_val=queue_y_c)
control_x = Controlador(dir_2_pin, step_2_pin, frecuencia, ref=origen_x, queue_val=queue_x_c)

control_y.start()
control_x.start()

while True:
   pass
   