import time
import picamera
import numpy as np
from PIL import Image


with picamera.PiCamera(resolution='VGA') as camera:
    camera.start_preview()
    time.sleep(2)
    camera.capture('Fotos/foo.jpg')
with Image.open('Fotos/foo.jpg') as img:
    img.load()
    array = np.asarray(img)
    
    img_final = array.copy()
    #gray_img = img.convert("L")
    #threshold = 10
    #img_threshold = img.point(lambda x: 255 if x > threshold else 0)
    #img_threshold = img_threshold.convert("1")
    for i in range(3):
        img_2 = array[:,:,i]
        Image.fromarray(img_2).convert("L").save(f"Fotos/foo{i}.png")
    try:
        im_binaria = (array[:,:,1] > 200)
        print(im_binaria.shape)
        Image.fromarray(im_binaria).convert("L").save("Fotos/EncontradaBinaria.png")
        filas, columnas = np.nonzero((array[:,:,1] > 200))
        fila_promedio = int(np.average(filas))
        columna_promedio = int(np.average(columnas))
        for fila in range(img_2.shape[0]):
            img_final[fila, columna_promedio, :] = 0
        for columna in range(img_2.shape[1]):
            img_final[fila_promedio, columna, :] = 0
        print(f"Punto encontrado en la posicion {fila_promedio},{columna_promedio}")
    except:
        print("Punto no encontrado")
                
    Image.fromarray(img_final).convert("RGB").save("Fotos/Encontrada.png")
    