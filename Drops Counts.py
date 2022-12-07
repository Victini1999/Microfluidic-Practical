##Comptage des gouttes non fluorescentes
# library imports
from math import pi,sqrt
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imshow
from skimage.color import rgb2gray
from skimage.feature import blob_dog, blob_log, blob_doh
from skimage.morphology import (erosion, dilation, closing, opening, area_closing, area_opening)
from skimage.measure import label, regionprops

listitem=['a','b']

for it1 in range(1,6):
    for it2 in listitem:
        pathway="C:/Users/jules/Desktop/Cours M2 CBM/Microfluidique et Biologie Digitale/TP/Data/Photo/Etalonnage/C"+ str(it1) + "_" + it2 +'/'
        file='C'+ str(it1) + "_" + it2 +'_c1.JPG'
        im=pathway+file
        im2=pathway+'C'+ str(it1) + "_" + it2 +'_c2.JPG'

        # binarizing source image
        img = cv2.imread(im,0)
        img2= cv2.imread(im2,0)
        img = cv2.medianBlur(img,5)

        th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                    cv2.THRESH_BINARY,15,2)
        th2 = cv2.threshold(img,127,255,cv2.THRESH_BINARY)

        img_morph = area_closing(area_opening(th3, 100), 400)
        rbc_bw = label(img_morph)
        rbc_props = regionprops(rbc_bw)
        fig, ax = plt.subplots(figsize=(18, 8))
        ax.imshow(img)
        rbc_count = 0
        area=[]
        Position=[]
        allume=0
        for i, prop in enumerate(rbc_props):
            circularity=4*pi*prop.area/(prop.perimeter**2)
            if circularity>0.65 and prop.area>500:
                y1, x1, y2, x2 = (prop.bbox[0], prop.bbox[1], prop.bbox[2], prop.bbox[3])
                width = x2 - x1
                height = y2 - y1
                r = plt.Rectangle((x1, y1), width = width, height=height, color='r', fill=False)
                ax.add_patch(r)
                rbc_count += 1
                area.append(prop.area)
                Pos=prop.centroid
                x=int(Pos[0])
                y=int(Pos[1])
                Position.append([x,y,width])
                if img2[x][y]>17:
                    allume+=1
                    # r = plt.Rectangle((x1, y1), width = width, height=height, color='r', fill=False)
                    # ax.add_patch(r)


        plt.savefig(pathway+'detection.PNG')
        plt.clf()
        plt.hist(area,150)
        plt.xlabel('Rayon')
        plt.ylabel('Nombre de gouttes')
        plt.title('Répartition des volumes des gouttes')
        print('Number total of drops :', rbc_count)
        print('Number total of illuminated drops :', allume)
        plt.savefig(pathway+'Repartition.PNG')
        plt.clf()