import time
import cv2
import numpy as np
import math
import random

def distanceAB(x1,y1,x2,y2):
    return math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2))

def NEps(image, i, j,distance):
    array_NEps = []
    if ((i - distance) < 0):
        Xmin = 0
    else:
        Xmin = i - distance
    if ((i + distance) > image.shape[0]):
        Xmax = image.shape[0]
    else:
        Xmax = i + distance
    if ((j - distance) < 0):
        Ymin = 0
    else:
        Ymin = j - distance
    if ((j + distance) > image.shape[1]):
        Ymax = image.shape[1]
    else:
        Ymax = j + distance
    for x in range(Xmin, Xmax+1):
        for y in range(Ymin, Ymax+1):
            if((x>=image.shape[0])or (y>=image.shape[1])):
                continue
            else:
                if (image[x, y]<255):
                    if (distanceAB(i,j,x,y)<=distance):
                        array_NEps.append([x, y])
    return array_NEps

def DBSCAN(file, minPts, distance):
    img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    print(img.shape[0], img.shape[1])
    image_number = []
    image_output = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
    C = np.zeros((img.shape[0], img.shape[1], 1), np.uint8)
    C[:, :] = 0
    count = 0
    image_output[:, :,:] = [255,255,255]
    for i in range(0, img.shape[0]):
        for j in range(0, img.shape[1]):
            if(img[i,j]<255):
                image_number.append([i,j])
    while(image_number!=[]):
        for item in image_number:
            NeighborPts = NEps(img, item[0], item[1], distance)
            if (len(NeighborPts) >= minPts):
                count += 1
                C[item[0], item[1]] = count
                while(NeighborPts!=[]):
                    for ne_item in NeighborPts:
                        C[ne_item[0], ne_item[1]] = count
                        ne_NeighborPts = NEps(img, ne_item[0], ne_item[1], distance)
                        if ne_item in image_number:
                            for join in ne_NeighborPts:
                                if(C[join[0],join[1]]!=0):
                                    continue
                                # 未檢查
                                if (len(ne_NeighborPts)>=minPts):
                                   C[join[0],join[1]]=count
                                Nne_NeighborPts = NEps(img, join[0], join[1], distance)
                                for nejoin in Nne_NeighborPts:
                                    if(len(NEps(img, nejoin[0], nejoin[1], distance))>=minPts and(nejoin not in NeighborPts)):
                                        NeighborPts.append(nejoin)
                            del image_number[image_number.index(ne_item)]
                        del NeighborPts[NeighborPts.index(ne_item)]
            if item in image_number:
                del image_number[image_number.index(item)]
    print("finall_"+str(count))
    for color in range(1,count+1):
        C_color= [random.randint(50, 220),random.randint(50, 220),random.randint(50, 220)]
        for i in range(0, img.shape[0]):
            for j in range(0, img.shape[1]):
                if(C[i,j]==color):
                    if(C[i,j]==0):
                        image_output[i,j,:]=[255,255,255]
                    else:
                        image_output[i, j,:] = C_color
    cv2.imwrite("test2_" + str(distance)+"_"+str(count)+ ".bmp", image_output)


file = "test2.bmp"
minPts = 5
distance = 1
start = time.time()
DBSCAN(file, minPts, distance)
end = time.time()
print('{} s'.format(end - start))