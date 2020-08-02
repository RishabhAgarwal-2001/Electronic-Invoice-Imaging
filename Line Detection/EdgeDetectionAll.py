import cv2
from Helpers import *
from CropBoxes import CropBoxes
import numpy as np
from os.path import isdir
from os import mkdir

def CompleteImage (im):
    X, Y = im.shape
    for i in range(X):
        for  j in range(Y):
            if (im[i, j] == 0):
                continue
            count = 0
            no = 0
            if (i-10 >= 0 and im[i-10, j] == 255):
                count += 1
                no = 1
            if (j+10 < Y and im[i, j+10] == 255):
                count += 1
                no = 2
            if (i+10 < X and im[i+10, j] == 255):
                count += 1
                no = 3
            if (j-10 >= 0 and im[i, j-10] == 255):
                count += 1
                no = 4
            if (count == 1):
                if (no == 3):
                    for k in range(i-1, -1, -1):
                        if (im[k, j] == 0):
                            im[k, j] = 255
                        else:
                            break
                elif (no == 4):
                    for k in range(j+1, Y):
                        if (im[i, k] == 0):
                            im[i, k] = 255
                        else:
                            break
                elif (no == 1):
                    for k in range(i+1, X):
                        if (im[k, j] == 0):
                            im[k, j] = 255
                        else:
                            break
                else:
                    for k in range(j-1, -1, -1):
                        if (im[i, k] == 0):
                            im[i, k] = 255
                        else:
                            break
    return im

#Call this method by passing image and a bool value that you want to show mask image formed or not
def EdgeDetectionAll(name, toShow):
    i1 = cv2.cvtColor(cv2.imread(name), cv2.COLOR_BGR2GRAY)
    i2 = i1
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    i1 = clahe.apply(i1)

    iHorizontaledges = Prewitt(i1, True)
    # iHorizontaledges = cv2.Canny (i1, 200, 255)
    iHorizontaledges = Threshold(iHorizontaledges)
   
    #Closing to link some broken horizontal edges
    mask = np.ones((1, 7), dtype = np.uint8)
    iHorizontaledges = cv2.dilate(iHorizontaledges, mask)
    iHorizontaledges = cv2.erode(iHorizontaledges, mask)

    #Opening to remove everything except horizontal lines
    mask = np.ones((1, 201), dtype = np.uint8)
    iHorizontaledges = cv2.erode(iHorizontaledges, mask)
    iHorizontaledges = cv2.dilate(iHorizontaledges, mask)
  
    # iHorizontaledges = Houghtransform(iHorizontaledges)

    # iHorizontaledges = Threshold(iHorizontaledges)    

    iVerticaledges = Prewitt(i1, False)
    iVerticaledges = Threshold(iVerticaledges)
    
    #Closing to link some broken vertical edges
    mask = np.ones((15, 1), dtype = np.uint8)
    iVerticaledges = cv2.dilate(iVerticaledges, mask)
    iVerticaledges = cv2.erode(iVerticaledges, mask)

    #Opening to remove everything except vertical lines
    mask = np.ones((125, 1), dtype = np.uint8)
    iVerticaledges = cv2.erode(iVerticaledges, mask)
    iVerticaledges = cv2.dilate(iVerticaledges, mask)

    # iVerticaledges = Threshold(iVerticaledges)

    # X, Y = iHorizontaledges.shape
    # lastOne = [-1, -1]
    # for i in range (X):
    #     for j in range (Y):
    #         if ((iVerticaledges[i, j] == 255 or iHorizontaledges[i, j] == 255 or j == Y-1) and lastOne[0] == i and j - lastOne[1] > 1):
    #             for k in range (lastOne[1],j+1):
    #                 iHorizontaledges[i, k] = 255
    #             lastOne = [-1, -1]
    #         if (iHorizontaledges[i, j] == 255):
    #             lastOne = [i, j]
    #             continue

    # lastOne = [-1, -1]
    # for i in range (X-1, -1, -1):
    #     for j in range (Y-1, -1, -1):
    #         if ((iVerticaledges[i, j] == 255 or iHorizontaledges[i, j] == 255 or j == 1) and lastOne[0] == i and lastOne[1]-j > 1):
    #             for k in range (j, lastOne[1]+1):
    #                 iHorizontaledges[i, k] = 255
    #             lastOne = [-1, -1]
    #         if (iHorizontaledges[i, j] == 255):
    #             lastOne = [i, j]
    #             continue

    # mask = np.ones ((3, 1), dtype=np.uint8)
    # mask[1][0] = 0
    # iHorizontaledges = iHorizontaledges + cv2.erode(iHorizontaledges, mask)
    # iHorizontaledges = Threshold(iHorizontaledges)
    # mask = np.ones ((3, 1), dtype=np.uint8)
    # iHorizontaledges = cv2.erode(iHorizontaledges, mask)

    # X, Y = iVerticaledges.shape

    # lastOne = [-1, -1]
    # for j in range (Y):
    #     for i in range (X):
    #         if ((iVerticaledges[i, j] == 255 or iHorizontaledges[i, j] == 255 or j == Y-1) and lastOne[1] == j and i-lastOne[0] > 1):
    #             if (i == X-1):
    #                 iVerticaledges[i, j] = 255
    #             for k in range(lastOne[0]+1, i):
    #                 iVerticaledges[k, j] = 255
    #             lastOne = [-1, -1]
    #         if (iVerticaledges[i, j] == 255):
    #             lastOne = [i, j]
    #             continue;

    # lastOne = [-1, -1]
    # for j in range(Y-1, -1, -1):
    #     for i in range(X-1, -1, -1):
    #         if ((iHorizontaledges[i, j] == 255 or i==1) and lastOne[1] == j and lastOne[0]-i > 1):
    #             if (i == 1):
    #                 iVerticaledges[i, j] = 255
    #             for k in range(i+1,lastOne[0]):
    #                 iVerticaledges[k, j] = 255
    #             lastOne = [-1, -1]
    #         if (iVerticaledges[i, j] == 255):
    #             lastOne = [i, j]
    #             continue

    # lastOne = [-1, -1]
    # for i in range (X):
    #     for j in range (Y):
    #         if (iVerticaledges[i, j] == 255 and lastOne[0] == i and j - lastOne[1] > 1 and j - lastOne[1] < 5):
    #             for k in range(lastOne[1]+1, j):
    #                 iVerticaledges[i, k] = 255
    #             lastOne = [-1, -1]
    #         if (iVerticaledges[i, j] == 255):
    #             lastOne = [i, j]
    #             continue;
    # mask = np.ones((1, 3), dtype=np.uint8)
    # mask[0][1] = 0
    # iVerticaledges = cv2.erode(iVerticaledges, mask)
    
    # cv2.imshow('Horizontal', iHorizontaledges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow('Vertical', iVerticaledges)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    im = iHorizontaledges + iVerticaledges
    im = Threshold(im)

    # mask = np.ones((19, 19), dtype = np.uint8)
    # im = cv2.dilate(im, mask)
    # im = cv2.erode(im, mask)

    # im = Threshold(im)
    im = CompleteImage(im)

    if (toShow):
        cv2.imshow('All', im)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if (not isdir('Images')):
        mkdir('Images')
    cv2.imwrite('Images/EdgesAll.jpeg', im)
    cv2.imwrite('Images/EdgesH.jpeg', iHorizontaledges)
    cv2.imwrite('Images/EdgesV.jpeg', iVerticaledges)
    CropBoxes(i2, im);
    return


if __name__ == '__main__':
     EdgeDetectionAll('Images/image24.tif', True)
