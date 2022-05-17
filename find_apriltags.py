# AprilTags Max Res Example
#
# This example shows the power of the OpenMV Cam to detect April Tags
# on the OpenMV Cam M7. The M4 versions cannot detect April Tags.

import sensor, image, time, math, omv

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.WVGA2) # nos quedamos sin memoria si la resolución es mucho mayor...
# AprilTags funciona en un máximo de <64K píxeles.

if omv.board_type() == "H7": sensor.set_windowing((240, 240))
elif omv.board_type() == "M7": sensor.set_windowing((200, 200))
else: raise Exception("Necesita una cámara OpenMV más potente para ejecutar este script")

sensor.skip_frames(30)
sensor.set_auto_gain(False)  # debe desactivar esto para evitar el lavado de la imagen...
#sensor.set_auto_whitebal(False) # debe desactivar esto para evitar el lavado de la imagen...
clock = time.clock()

# ¡Nota! A diferencia de find_qrcodes, el método find_apriltags no necesita corrección de lente en la imagen para funcionar.

# El código apriltag admite hasta 6 familias de etiquetas que se pueden procesar al mismo tiempo.
# Los objetos de etiquetas devueltos tendrán su familia de etiquetas e identificación dentro de la familia de etiquetas.

#tag_families = 0
#tag_families |= image.TAG16H5      # comentar para deshabilitar esta familia
#tag_families |= image.TAG25H7      # comentar para deshabilitar esta familia
#tag_families |= image.TAG25H9      # comentar para deshabilitar esta familia
#tag_families |= image.TAG36H10     # comentar para deshabilitar esta familia
tag_families = image.TAG36H11       # comentar para deshabilitar esta familia (default family)
#tag_families |= image.ARTOOLKIT    # comentar para deshabilitar esta familia

# ¿Cuál es la diferencia entre las familias de etiquetas? Bueno, por ejemplo, la familia TAG16H5 es efectivamente
# una etiqueta cuadrada de 4x4. Entonces, esto significa que se puede ver a una distancia mayor que una etiqueta TAG36H11 que
# es una etiqueta cuadrada de 6x6. Sin embargo, el valor H más bajo (H5 versus H11) significa que el falso positivo
# la tarifa para la etiqueta 4x4 es mucho, mucho, mucho más alta que la etiqueta 6x6. Entonces, a menos que tengas un
# razón para usar las otras familias de etiquetas, solo use TAG36H11, que es la familia predeterminada.

def family_name(tag):
    if(tag.family() == image.TAG16H5):
        return "TAG16H5"
    if(tag.family() == image.TAG25H7):
        return "TAG25H7"
    if(tag.family() == image.TAG25H9):
        return "TAG25H9"
    if(tag.family() == image.TAG36H10):
        return "TAG36H10"
    if(tag.family() == image.TAG36H11):
        return "TAG36H11"
    if(tag.family() == image.ARTOOLKIT):
        return "ARTOOLKIT"

while(True):
    clock.tick()
    img = sensor.snapshot()
    for tag in img.find_apriltags(families=tag_families):
#   for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
        img.draw_rectangle(tag.rect(), color = 127)
        img.draw_cross(tag.cx(), tag.cy(), color = 127)
        print_args = (family_name(tag), tag.id(), (180 * tag.rotation()) / math.pi)
        print("Tag Family %s, Tag ID %d, rotation %f (degrees)" % print_args)
    print(clock.fps())
