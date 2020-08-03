import cv2
import numpy as np

def Prewitt (img, b):
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_gaussian = cv2.GaussianBlur(img,(3,3),0)

    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    img_prewittx = cv2.filter2D(img_gaussian, -1, kernelx)
    img_prewitty = cv2.filter2D(img_gaussian, -1, kernely)
    if b:
        return img_prewittx
    else:
        return img_prewitty

def Threshold (img):
    X, Y = img.shape
    for i in range(X):
        for j in range (Y):
            if (img[i][j] >= 128):
                img[i][j] = 255
            else:
                img[i][j] = 0;
    return img

def Houghtransform(edges):
    lines = cv2.HoughLines(edges,1,np.pi/180,200)
    for rho,theta in lines[0]:
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))

        cv2.line(edges,(x1,y1),(x2,y2),255,1)
    return edges