## Código escrito basandose en el tutorial https://picamera.readthedocs.io/en/release-1.13/recipes1.html
## Manipulado por Matías Woolvett, Agustín Mendoza y Benjamín Fortuño para el ramo Diseño Eléctrico
## en la Universidad Católica de Chile

import time
import threading
import picamera
import io
import numpy as np
import multiprocessing
from PIL import Image, ImageMorph

class ImageProcessor(threading.Thread):
    def __init__(self, owner):
        super(ImageProcessor, self).__init__()
        self.stream = io.BytesIO()
        self.event = threading.Event()
        self.terminated = False
        self.owner = owner
        self.start()

    def run(self):
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    self.stream.seek(0)
                    with Image.open(self.stream) as self.img:
                        self.img.load()
                        self.array = np.asarray(self.img)
                    self.filas, self.columnas = np.nonzero((self.array[:,:,1] > 180))
                    try:
                        self.fila = int(np.average(self.filas))
                        self.columna = int(np.average(self.columnas))
                        self.owner.queue_fila.put(self.fila)
                        self.owner.queue_columna.put(self.columna) 
                        self.owner.queue_y_c.put(self.fila)
                        self.owner.queue_x_c.put(self.columna) 
                        #self.owner.queue_y_c[-1] = self.fila
                        #self.owner.queue_x_c[-1] = self.columna
                    except:
                        self.fila = 0
                        self.columna = 0
                    #print(self.fila, self.columna)
                    

                    # Set done to True if you want the script to terminate
                    # at some point
                    #self.owner.done=True
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()
                    # Return ourselves to the available pool
                    with self.owner.lock:
                        self.owner.pool.append(self)

class ProcessOutput(object):
    def __init__(self, queue_fila, queue_columna, queue_x_c, queue_y_c):
        self.done = False
        # Construct a pool of 4 image processors along with a lock
        # to control access between threads
        self.lock = threading.Lock()
        self.pool = [ImageProcessor(self) for i in range(100)]
        self.processor = None
        self.contador = 0
        self.queue_fila = queue_fila
        self.queue_columna = queue_columna
        self.queue_x_c = queue_x_c
        self.queue_y_c = queue_y_c

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame; set the current processor going and grab
            # a spare one
            if self.processor:
                self.processor.event.set()
            with self.lock:
                if self.pool:
                    self.processor = self.pool.pop()
                else:
                    # No processor's available, we'll have to skip
                    # this frame; you may want to print a warning
                    # here to see whether you hit this case
                    print("No hay procesador!")
                    self.processor = None
        if self.processor:
            self.contador += 1
            if self.contador == 1:
                self.time2 = time.time()
            if self.contador % 60 == 0:
                #pass 
                #print(time.time()-self.time2) 
                self.time2 = time.time()
            self.processor.stream.write(buf)
    

    def flush(self):
        # When told to flush (this indicates end of recording), shut
        # down in an orderly fashion. First, add the current processor
        # back to the pool
        if self.processor:
            with self.lock:
                self.pool.append(self.processor)
                self.processor = None
        # Now, empty the pool, joining each thread as we go
        while True:
            with self.lock:
                try:
                    proc = self.pool.pop()
                except IndexError:
                    pass # pool is empty
            proc.terminated = True
            proc.join()

def encontrar_laser(queue_fila, queue_columna, queue_x_c, queue_y_c):
    with picamera.PiCamera(resolution='VGA', framerate = 60) as camera:
        camera.start_preview()
        time.sleep(2)
        output = ProcessOutput(queue_fila, queue_columna , queue_x_c, queue_y_c)
        camera.start_recording(output, format='mjpeg') #, quality=23 [1, 40] (1 el mejor), normal entre 20-25
        while not output.done:
            camera.wait_recording(1)
        camera.stop_recording()


