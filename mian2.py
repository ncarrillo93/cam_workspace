import sensor, image, time, json, omv, pyb, os
from ulab import numpy as np

sensor.reset()
extensiones=['.bmp','.json']
for extension in extensiones:
    files_in_directory = os.listdir('.')
    filtered_files = [file for file in files_in_directory if file.endswith(extension)]
    print('archivos por borrar',filtered_files)
    for file in filtered_files:
        os.remove(file)
    files_in_directory = os.listdir('.')
    filtered_files = [file for file in files_in_directory if file.endswith(extension)]
    print(filtered_files)
green_led = pyb.LED(2)
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.WVGA2)

brillo,saturacion,contraste = [0,0,0]
contador=1

sensor.set_brightness(brillo)
sensor.set_contrast(contraste)
sensor.set_saturation(saturacion)
sensor.skip_frames(time = 10000)

lo_exp,hi_exp,step=[0,20000,500]

sensor.set_auto_gain(False,1)

for i in range(lo_exp,hi_exp,step):
    os.mkdir(str(i)) #carpeta que contiene imagenes con un tiempo de exposición para despues generar un promedio de esas imagenes

    sensor.set_auto_exposure(False, exposure_us=int(i))

    contador = 1

    for i in range(0,20):
        img = sensor.snapshot()
        print('n°: ',contador,'exposicion ',i,'us | Gain: ',1,'dB ',sensor.get_gain_db(),'dB  ')
        x= {"ganancia_db" : sensor.get_gain_db(),
            "exposicion_us" : sensor.get_exposure_us(),
            "media" : img.histogram().get_statistics().mean(),
            "mediana" : img.histogram().get_statistics().median(),
            "Desviación estandar" : img.histogram().get_statistics().stdev(),
            "cuartil superior" : img.histogram().get_statistics().uq()}

        img.save(str(i)+'/image_'+str(contador)+'.bmp')

        with open(str(i)+'/data_'+str(contador)+'.json', 'a') as file:
            json.dump(x,file)
            contador = contador+1


pyb.hard_reset()
