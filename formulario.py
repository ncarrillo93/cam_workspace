# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

import sensor, image, time, btree, json

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
#sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

#configuracion camar
#ganancia=[2,4,6,8,16,32,64,128]
#sensor.set_gainceiling(128)           # set ganancia 2,4,6,8,16,32,64 o 128
#sensor.set_contrast(3)             # set contraste -3 a +3.
#sensor.set_brightness(3)            # set brillo -3 a +3.
#sensor.set_saturation(3)           # set saturacion -3 a +3.

img = sensor.snapshot()         # Take a picture and return the image.
histograma = img.get_histogram()
print(histograma.get_statistics())
print(img.histogram())

#tarea:
#       - setear y guardar valores de los parametros y guardar en un txt o en el nombre de la foto
#contraste  =
ganancia   = sensor.get_gain_db()
exposicion = sensor.get_exposure_us()



#       - mostrar histograma por python (no micropython)

#       - asegurarme de guardar las fotos en .raw (correccion gamma)

#       - asegurarme que los datos influyen en la foto

#       - que hace el codigo cuando cambio algun parametro a nivel de hardaware



