import threading
import time
from stepper import init_stepper, move_stepper

step_1_pin = 11
dir_1_pin = 12
step_2_pin = 15
dir_2_pin = 16
frecuencia = 1000
direccion_1 = 0
direccion_2 = 0

init_stepper(step_1_pin, step_2_pin, dir_1_pin, dir_2_pin)

hertz = 1
hertz *= 2
tiempo_entre = 1/hertz

contador = 0
t0 = time.time()
while True:
    angulo_1 = 80
    angulo_2 = 80

    if angulo_1 < 0:
        angulo_1 = angulo_1*-1
        direccion_1 = 1
    else:
        direccion_1 = 0
    if angulo_2 < 0:
        angulo_2 = angulo_2*-1
        direccion_2 = 1
    else:
        direccion_2 = 0

    thread_motor_1 = threading.Thread(target=move_stepper,args=(dir_1_pin, step_1_pin, angulo_1, frecuencia, direccion_1))
    #thread_motor_2 = threading.Thread(target=move_stepper,args=(dir_2_pin, step_2_pin, angulo_2, frecuencia, direccion_2))
    thread_motor_1.start()
    #thread_motor_2.start()

    time.sleep(tiempo_entre)
    
    angulo_1 = -80
    angulo_2 = -80

    if angulo_1 < 0:
        angulo_1 = angulo_1*-1
        direccion_1 = 1
    else:
        direccion_1 = 0
    if angulo_2 < 0:
        angulo_2 = angulo_2*-1
        direccion_2 = 1
    else:
        direccion_2 = 0

    thread_motor_1 = threading.Thread(target=move_stepper,args=(dir_1_pin, step_1_pin, angulo_1, frecuencia, direccion_1))
    #thread_motor_2 = threading.Thread(target=move_stepper,args=(dir_2_pin, step_2_pin, angulo_2, frecuencia, direccion_2))
    thread_motor_1.start()
    #thread_motor_2.start()

    time.sleep(tiempo_entre)
    contador += 1
    if contador == 6:
        print(time.time() - t0)