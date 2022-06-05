import time
import RPi.GPIO as GPIO

def init_stepper(step_1_pin, step_2_pin, dir_1_pin, dir_2_pin):
    # Suppress warnings
    GPIO.setwarnings(False)             # Porque tenemos loop infinito
    # Use "GPIO" pin numbering
    GPIO.setmode(GPIO.BOARD)            # Segun la numeracion del conector externo (BOARD) y no segun la numeraciun del chip (BCM)
    # Set LED pin as output
    GPIO.setup(step_1_pin, GPIO.OUT)  
    GPIO.setup(dir_1_pin, GPIO.OUT) 
    GPIO.setup(step_2_pin, GPIO.OUT)  
    GPIO.setup(dir_2_pin, GPIO.OUT)  

def move_stepper(dir_pin, step_pin, angle, frequency, direction):
    t0 = time.process_time()
    if direction == 0:
        GPIO.output(dir_pin, GPIO.HIGH)  # Girar en un sentido
    else:
        GPIO.output(dir_pin, GPIO.LOW)   # Girar en un sentido
    steps = int(angle/360*400)
    semiperiod = 1/(2*frequency) 
    #print("Semiperido:", semiperiod)
    #print("Steps:", steps)       
    for i in range(steps):
        GPIO.output(step_pin, GPIO.HIGH) # Turn STEP pin on
        time.sleep(semiperiod)           
        GPIO.output(step_pin, GPIO.LOW)  # Turn STEP pin on
        time.sleep(semiperiod)           
    t1 = time.process_time()
    #print("Mover el motor se demoro:", t1 - t0)
