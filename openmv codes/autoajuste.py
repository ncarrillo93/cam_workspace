import sensor, image, time, math, omv

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.WVGA2)   # Set frame size to QVGA (752x480)

sensor.skip_frames(time = 2000)     # Wait for settings take effect.
tag_families = image.TAG36H11

def find_coordenates():
    x,y,w,h=[0,0, int(sensor.width()/4) , int(sensor.height()/2)]
    cxw,cyw,w2,h2=[0,0,0,0]
    centros,tag_list=[[],[]]
    img = sensor.snapshot()
    img = img.to_bitmap()
    for i in range(0,752,int(w/4)):
        for j in range(0,480,int(h/4)):
            try:
                tag_list.extend(img.find_apriltags(roi=(x+i,y+j,w,h), families=tag_families))
            except (MemoryError):# No detecte todas las excepciones,
                print(None)      #de lo contrario no podrá detener el script.
                pass
            if(len(tag_list)>2):
                tag_list=[]
            if(len(tag_list)==2):
                if(tag_list[0].id() != tag_list[1].id()):
                    for tag in tag_list:

                        img.draw_rectangle(tag.rect(), color = (255, 0, 0))
                        img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))

                        centros.append((tag.cx(),tag.cy()))
                        w2=int(tag.w()/2)
                        h2=int(tag.h()/2)
                        if len(centros)==2:
                            cxw = int((centros[0][0]+centros[1][0])/2)
                            cyw = int((centros[0][1]+centros[1][1])/2)
                            aux=(cxw,cyw,w2,h2)
                            centros,tag_list=[[],[]]
                            return aux


def bisection(roi,ideal,minimo,maximo,tol):
    mitad=(minimo+maximo)/2
    mean=evaluate(roi,mitad)
    while True:
        mean=evaluate(roi,mitad)
        if mean<=ideal:
            minimo=mitad
            mitad=int((minimo+maximo)/2)
        mean=evaluate(roi,mitad)
        else:
            maximo=mitad
            mitad=int((minimo+maximo)/2)
        if mean>=(ideal-tol):
            if mean<=(ideal+tol):
                return mitad

def evaluate(roi,time_exp):
    sensor.set_auto_exposure(False,exposure_us=int(time_exp))
    sensor.skip_frames(time = 500)
    img = sensor.snapshot()
    aux = img.get_statistics(roi=roi)
    return aux.mean()

# main
coord=None
while coord is None:
    coord=find_coordenates()
print(coord)
img=sensor.snapshot()
img.draw_rectangle(coord, color = (0, 0, 0),thickness=2)
sensor.skip_frames(time=500)
data=bisection(coord,200,0,20000,10)

print('tiempo de exposición',data)
