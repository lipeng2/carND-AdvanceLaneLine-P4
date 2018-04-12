import numpy as np
import cv2

def canny(img, thresh=(10,50), ksize=5):
    return cv2.Canny(img, thresh[0], thresh[1], ksize)

def abs_sobel_thresh(img, orient='x', thresh=(0,255), ksize=3):
    # check for invalid input
    if len(img) == 0:
        print('no image found')
        return
    if orient not in ['x', 'y']:
        print('invalid orient')
        return

    # convert img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # apply sobel operator
    x = 1 if orient == 'x' else 0
    y = 1 if orient == 'y' else 0
    sobel = np.absolute(cv2.Sobel(gray, cv2.CV_64F, x, y, ksize))

    scale_sobel = np.uint8(255*sobel/np.max(sobel))
    binary_output = np.zeros_like(scale_sobel)
    binary_output[(scale_sobel>=thresh[0])&(scale_sobel<=thresh[1])] = 1

    return binary_output

def mag_thresh(img, thresh=(0,255), ksize=3):
    # convert img to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
    sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
    mag = np.sqrt(sobelx**2 + sobely**2)
    scale_sobel = np.uint8(mag*255/np.max(mag))
    binary_output = np.zeros_like(scale_sobel)
    binary_output[(scale_sobel>=thresh[0])&(scale_sobel<=thresh[1])] = 1

    return binary_output

def dir_thresh(img, thresh=(0, np.pi/2), ksize=3):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    sobelx = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize))
    sobely = np.absolute(cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize))
    dir = np.arctan2(sobely, sobelx)
    binary_output = np.zeros_like(dir)
    binary_output[(dir>thresh[0])&(dir<thresh[1])] = 1

    return binary_output

def hls_thresh(img,thresh=(100,255)):
    hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
    s = hls[:,:,2]
    binary_output = np.zeros_like(s)
    binary_output[(s>=thresh[0])&(s<=thresh[1])]=1

    return binary_output

def hsv_thresh(img, thresh=(100,255)):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    v = hsv[:,:,2]
    binary_output=np.zeros_like(v)
    binary_output[(v>=thresh[0])&(v<=thresh[1])]=1

    return binary_output

def rgb_thresh(img):
    r, g, b = img[:,:,0], img[:,:,1], img[:,:,2]
    binary_output, yellow, white = np.zeros_like(r), np.zeros_like(r), np.zeros_like(r)
    yellow[(r>=150)&(g>=130)&(b<85)] = 1
    white[(r>=220)&(g>=220)&(b>220)] = 1
    binary_output[(yellow==1)|(white==1)] = 1

    return binary_output
