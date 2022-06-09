import sensor, image, time, omv, pyb, os
from ulab import numpy as np

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # QVGA(320x240)

sensor.skip_frames(time = 2000)     # Wait for settings take effect.
img = sensor.snapshot().lens_corr(strength=1.7).scale(x_scale=2.353,y_scale=2.0)
img.save('img_correccion_y_escalado'+'.bmp')

pyb.delay(500)

sensor.skip_frames(time = 2000)     # Wait for settings take effect.
img = sensor.snapshot().lens_corr(strength=1.7)
img.save('img_correccion'+'.bmp')

pyb.delay(500)

sensor.skip_frames(time = 2000)     # Wait for settings take effect.
sensor.set_framesize(sensor.WVGA2)
img = sensor.snapshot()
img.save('img_sin_correccion'+'.bmp')

pyb.delay(500)

#sensor.set_framesize(sensor.WVGA2)  # WVGA2 (752,480)
#sensor.skip_frames(time = 2000)     # Wait for settings take effect.
#img = sensor.snapshot()
#img.save('img_sin_correccion'+'.bmp')




pyb.hard_reset()



