import cv2
import tkinter as tk
from PIL import ImageTk, Image
import numpy as np
import pygame
import time


frekvence = 160          # nosná frerkvence pro servo
duration = 1/frekvence  # délka samplu v s
sample_rate = 40000     # samplovací frekvence          
mL0 = 200               # pomocné, pamatují si předešlou hodnotu, hodnota 200 provede inicializaci
mR0 = 100
dmL = -105#-105			# uživatelská korekce posunu audio kanálů = korekce USB_C převodníku
dmR = -83	# -75		# korekce +-100%
pVelikost = int(sample_rate*duration)
signalLR = np.int16(np.zeros((pVelikost * 2)))
maxUp = np.int16(np.zeros(20))
maxDown = np.int16(np.zeros(20))
minDown = np.int16(np.zeros(20))
minUp = np.int16(np.zeros(20))
pocitadlo = 1638
for i in range(20):
    maxUp[i] = pocitadlo
    maxDown[i] = 32767 - pocitadlo
    minUp[i] = - pocitadlo
    minDown[i] = -(32767 - pocitadlo)
    pocitadlo = pocitadlo + 1638

#určeno pouze pro demostraci funkčnosti
casOld = time.time()
citac = 0 

# inicializace
# nastavení parametrů mixéru: vzorkovací frekvence/ počet kanálů/ povolení změn/ 
# defaltně 16b hodnota -16 = +-32000
pygame.mixer.pre_init(frequency=sample_rate, channels=2, allowedchanges=1)
pygame.init()

# Vytvoření zvukového objektu pomocí knihovny pygame
sound = pygame.mixer.Sound(signalLR.tobytes()) # předávání hodnot po Bytu
sound.play(-1)  # -1 znamená nekonečné opakování
root = tk.Tk()
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
lmain = tk.Label(root)
lmain.grid()

cap = cv2.VideoCapture(0)
fps = cap.get(cv2.CAP_PROP_FPS)


def motory(mL, mR):
    global signalLR, mL0, mR0, dmL,dmR, sound,pVelikost
    mL, mR = int((mL+dmL)/5), int((mR+dmR)/5) #změněno na rozsah -10..10
    #if mL<-20: mL=-20
    #if mL>20: mL=20
   # if mR<-20: mR=-20
    #if mR>20: mR=20
    if (mL != mL0) or (mR != mR0):
        # plnění v násobcích 0.025ms = 25us (mikrosekund)
        # 40 - vlevo   60 - stojí   80 - vpravo (1ms/1.5ms/2ms) - !!!CELÉ číslo
        dutyL = int(80 + mL)	#60 = 1.5 ms + 20 = 5ms pauza (náběh do maxima)
        dutyR = int(80 + mR)
        #print(dutyL,dutyR)
        
        #vygenerování L-kanálu
        signalLR[0:40:2]=maxUp
        signalLR[40:(2*dutyL):2]=32767
        signalLR[(2*dutyL):(40+2*dutyL):2]=maxDown
        signalLR[(40+2*dutyL):pVelikost:2]=0
        
        
        signalLR[pVelikost:(pVelikost+40):2]=minUp
        signalLR[(pVelikost+40):(pVelikost+2*dutyR):2]=-32767
        signalLR[(pVelikost+2*dutyR):(40+pVelikost+2*dutyR):2]=minDown
        signalLR[(40+pVelikost+2*dutyR)::2]=0
        
        #vygenerování R-kanálu
        signalLR[1::2]= signalLR[0::2]

        sound.stop()
        #print(signalLR[0::2])
        sound = pygame.mixer.Sound(signalLR.tobytes()) # předávání hodnot po Bytu
        sound.play(-1)  # -1 znamená nekonečné opakování

        mL0, mR0 = mL, mR
        



motory(0,0) 
time.sleep(3)

P = -0.001

poland = [[0 for _ in range(3)] for i in range(3)]
sum_ll = 0
sum_rr = 0
poc = 0
velikost = 80
vyska = 175
prumer = 0
white = 255
maxi = 0
vahy = [_ for _ in range(-400, 400)]
soucet = 0
soucet_vah = 0
smer = 0
cap.set(cv2. CAP_PROP_ANDROID_FLASH_MODE, cv2.CAP_ANDROID_FLASH_MODE_ON)
def analyze_frame():
    global poland, sum_ll, sum_rr
    ret, frame = cap.read()
    
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
    frame = cv2.resize(frame, (720, 480))
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    sum_rr = np.sum(frame_gray[0:480, 600:720])
    cv2.rectangle(frame_gray, (600, 0), (720, 480), white, 3)
    
    sum_ll = np.sum(frame_gray[:, 0:120])
    cv2.rectangle(frame_gray, (0, 0), (120, 480), white, 3)
    
    poland[0][0] = np.sum(frame_gray[0:120, 120:240])
    cv2.rectangle(frame_gray, (240, 120), (120, 0), white, 3)
    
    poland[0][1] = np.sum(frame_gray[0:120, 240:480])
    cv2.rectangle(frame_gray, (240, 0), (480, 120), white, 3)
    
    poland[0][2] = np.sum(frame_gray[0:120, 480:600])
    cv2.rectangle(frame_gray, (480, 0), (600, 120), white, 3)
    
    poland[1][0] = np.sum(frame_gray[120:360, 120:240])
    cv2.rectangle(frame_gray, (120, 120), (240, 360), white, 3)
    
    poland[1][1] = np.sum(frame_gray[120:360, 240:480])
    cv2.rectangle(frame_gray, (240, 120), (480, 360), white, 3)
    
    poland[1][2] = np.sum(frame_gray[120:360, 480:600])
    cv2.rectangle(frame_gray, (480, 120), (600, 360), white, 3)
    
    poland[2][0] = np.sum(frame_gray[360:480, 120:240])
    cv2.rectangle(frame_gray, (120, 360), (240, 480), white, 3)
    
    poland[2][1] = np.sum(frame_gray[360:480, 240:480])
    cv2.rectangle(frame_gray, (240, 360), (480, 480), white, 3)
    
    poland[2][2] = np.sum(frame_gray[360:480, 480:600])
    cv2.rectangle(frame_gray, (480, 360), (600, 480), white, 3)
    
    
    poland = np.divide(poland, 100000)
    poland = np.int32(poland)
    sum_ll = np.divide(sum_ll, 100000)
    sum_ll = np.int32(sum_ll)
    sum_rr = np.divide(sum_rr, 100000)
    sum_rr = np.int32(sum_rr)
    
    cv2.putText(frame_gray, str(sum_ll), (270, 200), cv2.FONT_ITALIC, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame_gray, str(poland[0]), (300, 170), cv2.FONT_ITALIC, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame_gray, str(poland[1]), (300, 200), cv2.FONT_ITALIC, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame_gray, str(poland[2]), (300, 230), cv2.FONT_ITALIC, 0.5, white, 2, cv2.LINE_AA)
    cv2.putText(frame_gray, str(sum_rr), (400, 200), cv2.FONT_ITALIC, 0.5, white, 2, cv2.LINE_AA)
    #print(poland)
    """for p in range(100, 140):
        arr_l_u = 0.0
        for x in range(p, (p+velikost)):
            for y in range(vyska, vyska + velikost):
                arr_l_u += frame_gray[y][x]
                frame_gray[vyska - 1][x] = 255
                frame_gray[vyska + velikost + 1][x] = 255
                
    for p in range(140, 180):
        arr_m_u = 0.0
        for x in range(p, (p+velikost)):
            for y in range(vyska, vyska + velikost):
                arr_m_u += frame_gray[y][x]
                frame_gray[vyska - 1][x] = 255
                frame_gray[vyska + velikost + 1][x] = 255
    for p in range(180, 220):
        arr_r_u = 0.0
        for x in range(p, (p+velikost)):
            for y in range(vyska, vyska + velikost):
                arr_r_u += frame_gray[y][x]
                frame_gray[vyska - 1][x] = 255
                frame_gray[vyska + velikost + 1][x] = 255
    """
    return frame_gray
def je_zed():
    return 0
   
def main():
    global imgtk, soucet,poc, velikost,vyska,prumer,white,maxi,vahy,soucet,soucet_vah,smer
    frame_gray = analyze_frame()
    
    """ 
    for i in range(1, len(arr_l_u)):
        
        cv2.line(frame_gray, (i - 1, 600 - int(arr_l_u[i - 1] / 20)), (i, 600 - int(arr_l_u[i] / 20)), white, 2)
    for i in range(1, len(arr_m_u)):
        
        cv2.line(frame_gray, (i - 1, 600 - int(arr_l_u[i - 1] / 20)), (i, 600 - int(arr_l_u[i] / 20)), white, 2)
    for i in range(1, len(arr_r_u)):
        
        cv2.line(frame_gray, (i - 1, 600 - int(arr_l_u[i - 1] / 20)), (i, 600 - int(arr_l_u[i] / 20)), white, 2)
    #cv2.line(frame_gray, (400 + int(smer), 0), (400 + int(smer) , 100), white, 2)
    """ 
    img = Image.fromarray(frame_gray)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.configure(image=imgtk)
    lmain.update()
    lmain.after(0, main)

main()
root.mainloop()