# Untitled - By: nicol - mi. oct. 6 2021

import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
for i in range(10):
    img = sensor.snapshot()
    img.save('/imagen_'+str(i)+'.bmp')

