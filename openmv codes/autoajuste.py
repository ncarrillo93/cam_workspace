import sensor, image, time, math, omv

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.GRAYSCALE) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.WVGA2)   # Set frame size to QVGA (320x240)
#sensor.set_auto_exposure(False,exposure_us=int(5000))
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
            except (MemoryError): # No detecte todas las excepciones, de lo contrario no podrá detener el script.
                print(None)
                pass
            if(len(tag_list)>2):
                tag_list=[]
            if(len(tag_list)==2):
                if(tag_list[0].id() != tag_list[1].id()):
                    for tag in tag_list:
                        centros.append((tag.cx(),tag.cy()))
                        w2=int(tag.w()/2)
                        h2=int(tag.h()/2)
                        if len(centros)==2:
                            cxw = int((centros[0][0]+centros[1][0])/2)
                            cyw = int((centros[0][1]+centros[1][1])/2)
                            aux=(cxw,cyw,w2,h2)
                            centros,tag_list=[[],[]]
                            return aux

#Modificar. usare otro metodo o evaluar distintos y elegir el mas optimo?
def auto_ajuste(coord,lo,hi,lo_exp,hi_exp):
    mid_lock = int((hi+lo)/2)
    while (1):
        mid_exp = int((hi_exp+lo_exp)/2)
        print (mid_exp)
        while (1):
            sensor.set_auto_exposure(False, exposure_us=lo_exp)
            aux=img.get_histogram(roi=coord )
            du_low = aux.get_statistics().mean()

            if (du_low is not None):
                break
            else:
                lo_exp = lo_exp + 10
        print (du_low)
        while (1):
            sensor.set_auto_exposure(False, exposure_us=hi_exp)
            aux=img.get_histogram(roi=coord )
            du_high = aux.get_statistics().mean()

            print (du_high)
            if (du_high is not None):
                break
            else:
                hi_exp = hi_exp - 10
                print ("Hi: {}".format(hi_exp))
        while (1):
            sensor.set_auto_exposure(False, exposure_us=mid_exp)
            aux=img.get_histogram(roi=coord )
            du_mid = aux.get_statistics().mean()
            print (du_mid)
            if (du_mid is not None):
                break
            else:
                hi_exp = mid_exp
                mid_exp = mid_exp - 10
        print (du_mid)
        if (du_mid > lo and du_mid < hi):
            print ("OKOK")
            return mid_exp
        elif (du_mid < mid_lock):
                lo_exp = mid_exp
        elif (du_mid > mid_lock):
                hi_exp = mid_exp


def auto_ajuste_2(coord,lo,hi,lo_exp,hi_exp):
    flag=1
    ideal=(lo+hi)/2
    mitad_exp=(lo_exp+hi_exp)/2
    while(flag):


        sensor.set_auto_exposure(False, exposure_us=int(lo_exp))
        mitad = img.get_histogram(roi=coord ).get_statistics().mean()
        if(mitad<ideal):
            lo=mitad
            lo_exp=mitad_exp

        sensor.set_auto_exposure(False, exposure_us=int(hi_exp))
        mitad = img.get_histogram(roi=coord ).get_statistics().mean()
        if(mitad>ideal):
            hi=mitad
            hi_exp=mitad_exp

coord=find_coordenates()
while(True):
    img=sensor.snapshot()
    img.draw_rectangle(coord,color=(0,0,0))

    auto_ajuste_2(coord,180,220,0,10000)
