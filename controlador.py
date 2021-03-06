import threading
import time
from simple_pid import PID
from multiprocessing import Process
from stepper import move_stepper


class Controlador(threading.Thread):
    def __init__(self, dir_pin, step_pin, frecuencia, ref, queue_val, kp=0.1, ki=10 ** 10, kd=0.0, dt=1/120, event=threading.Event()):
        threading.Thread.__init__(self)
        self.dir_pin = dir_pin
        self.step_pin = step_pin
        self.frecuencia = frecuencia
        self.ref = ref
        # atributos de constantes PID
        self.kp = kp
        self.ki = ki
        self.kd = kd
        # atributos de errores
        self.error_k0 = 0
        self.error_k1 = 0
        self.error_k2 = 0
        self.queue_val = queue_val
        self.dt = dt
        self.stopped = event
        # atributos para pruebas de rendimiento
        self.cyclecount = 0
        self.tiempo_inicio = 0
        self.tiempo_final = 0


    def actualizar_error(self):
        self.error_k2 = self.error_k1
        self.error_k1 = self.error_k0
        self.error_k0 = self.ref - self.queue_val.get()
        
        # print(f"El nuevo error es: {self.error_k0}")


    def actualizar_stepper(self):
        # Actualizar valores antes de calcular ángulo
        self.actualizar_error()

        # Se calcula delta-ángulo con pid incremental
        angulo = self.kp * (
            (1 + self.kd / self.dt) * self.error_k0 + 
            (self.dt / self.ki - 2 * self.kd / self.dt - 1) * self.error_k1 + 
            (self.kd / self.dt) * self.error_k2
        )

        # Se verifican direcciones dependiendo de los valores obtenidos
        if angulo < 0:
            angulo *= -1
            direccion = 0
        else:
            direccion = 1
        
        dir_pin = self.dir_pin
        step_pin = self.step_pin
        frecuencia = self.frecuencia
        
        # Se crea el proceso para mover el stepper en angulo=angulo y en direccion=direccion
        # print(f"Se mueve motor y la salida es {angulo}")
        thread_motor = Process(target=move_stepper,args=(dir_pin, step_pin, angulo, frecuencia, direccion))

        # Testeo de desempeño en tiempo del controlador
        self.cyclecount += 1
        if self.cyclecount == 1:
            self.tiempo_inicio = time.time()
        elif self.cyclecount == 61:
            self.tiempo_final = time.time()
            delta_t = self.tiempo_final - self.tiempo_inicio
            self.cyclecount = 0
            print(f"El tiempo de muestreo de control es de: {delta_t}")
            print(f"Se movio:                               {angulo}")

    def run(self):
        while not self.stopped.wait(self.dt):
            self.actualizar_stepper()