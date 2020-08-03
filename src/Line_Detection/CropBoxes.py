from os.path import isdir
from os import mkdir, walk
import shutil
import cv2
import numpy as np

def CropBoxes(im, mask):
    region = 1
    finish = [-1, -1]
    count = 0
    # Specify the folder where the files live.
    myFolder = '../results/crops_line'
    if (not isdir(myFolder)):
        mkdir(myFolder)
    else:
        try:
            shutil.rmtree(myFolder)
        except OSError as e:
            print ("Error: %s - %s." % (e.filename, e.strerror))
        mkdir(myFolder)
    sizeX, sizeY = im.shape
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if (mask[i][j] < 128):
                mask[i][j] = 0
            else:
                mask[i][j] = 1
    # cv2.imshow('Mask', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    for i in range (sizeX):
        for j in range(sizeY):
            if (mask[i, j] >= 1):
               continue
            start = [i, j]
            region = region+1
            mx = -1
            for x in range(i, sizeX):
                if (mask[x, j] == 1 or x == sizeX-1):
                    for y in range(j, mx+1):
                        mask[x, y] = region
                    finish = [x, mx]
                    break
                for y in range(j, sizeY):
                    if (mask[x, y] == 1 or y == sizeY-1):
                        mask[x, y] = region
                        mx = y
                        break
                    elif (mask[x, y] == 0):
                        mask[x, y] = region
            if (finish[0] < start[0] or finish[1] < start[1]):
                continue
            temp = np.zeros((finish[0]-start[0]+1, finish[1]-start[1]+1), dtype = np.uint8)
            for x in range(start[0], finish[0]+1):
                for y in range (start[1], finish[1]+1):
                    temp[x-start[0], y-start[1]] = im[x, y]
            count = count+1
            name = myFolder + '/out_' + str(count)
            name = name + '.png'
            cv2.imwrite(name, np.uint8(temp))

# if __name__ == '__main__':
#     CropBoxes(np.uint8(cv2.cvtColor(cv2.imread('image.tif'), cv2.COLOR_BGR2GRAY)), cv2.imread('EdgesAll.jpeg', cv2.IMREAD_UNCHANGED))