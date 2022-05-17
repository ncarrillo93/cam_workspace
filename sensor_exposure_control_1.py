# Control de exposición del sensor
#
# Este ejemplo muestra cómo controlar el sensor de la cámara.
# exposición manual versus dejar que se ejecute el control de exposición automático.

# ¿Cuál es la diferencia entre control de exposición y ganancia?
#
# Bueno, al aumentar el tiempo de exposición de la imagen, obtienes más
# luz de la cámara. Esto le brinda la mejor relación señal / ruido. Ustedes
# en general siempre quiere aumentar el tiempo de expsoure ... excepto, cuando
# aumenta el tiempo de exposición disminuye la velocidad máxima de fotogramas posible
# y si algo se mueve en la imagen, comenzará a difuminarse más con un
# mayor tiempo de exposición. El control de ganancia le permite aumentar la salida por
# píxel usando multiplicadores analógicos y digitales ... sin embargo, también amplifica
# ruido. Por lo tanto, es mejor dejar que la exposición aumente tanto como sea posible.
# y luego use el control de ganancia para recuperar el terreno restante.

import sensor, image, time

# Cambie este valor para ajustar la exposición. Pruebe 10.0 / 0.1 / etc.
EXPOSURE_TIME_SCALE = 1.0

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.WVGA2)
sensor.set_windowing(480,480)

# Imprima el tiempo de exposición inicial para comparar.
print("Initial exposure == %d" % sensor.get_exposure_us())

sensor.skip_frames(time = 2000)     # Wait for settings take effect.
clock = time.clock()                # Create a clock object to track the FPS.

# Tienes que desactivar el control automático de ganancia y el balance de blancos automático
# de lo contrario, cambiarán las ganancias de la imagen para deshacer cualquier configuración de exposición
# que pusiste en su lugar ...
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
# Need to let the above settings get in...
sensor.skip_frames(time = 500)

current_exposure_time_in_microseconds = sensor.get_exposure_us()
print("Current Exposure == %d" % current_exposure_time_in_microseconds)

# El control de exposición automático (AEC) está habilitado de forma predeterminada. Llamar a la siguiente función
# desactiva el control de exposición automática del sensor. La "exposición_us" adicional
El argumento # entonces anula el valor de exposición automática después de que AEC está deshabilitado.
sensor.set_auto_exposure(False, \
    exposure_us = int(current_exposure_time_in_microseconds * EXPOSURE_TIME_SCALE))

print("New exposure == %d" % sensor.get_exposure_us())
# sensor.get_exposure_us () devuelve el tiempo de exposición exacto del sensor de la cámara
# en microsegundos. Sin embargo, este puede ser un número diferente al que se
# ordenado porque el código del sensor convierte el tiempo de exposición en microsegundos
# a una hora de fila / píxel / reloj que no coincide perfectamente con microsegundos ...

# Si desea volver a activar la exposición automática, haga: sensor.set_auto_exposure (True)
# Tenga en cuenta que el sensor de la cámara cambiará el tiempo de exposición a su gusto.

# Haciendo: sensor.set_auto_exposure (False)
# Simplemente desactiva la actualización del valor de exposición pero no cambia la exposición
# El valor que determinó el sensor de la cámara era bueno.

while(True):
    clock.tick()                    # Update the FPS clock.
    img = sensor.snapshot()         # Take a picture and return the image.
    print(clock.fps())              # Note: OpenMV Cam runs about half as fast when connected
                                    # to the IDE. The FPS should increase once disconnected.
