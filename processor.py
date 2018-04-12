import numpy as np
from utils import *
import camera_calibration as cc
import color_gradient_threshold as cgt
import perspective_transform as ps
import sliding_window as sd
from collections import deque
import pickle

def draw_window(img, window, dim=(100,100), offset=0):
    '''
    draw an image on top of another image
    '''
    if window.shape[-1] !=3:
        window = np.dstack((window, window, window))*255
    window = cv2.resize(window, dim)
    img[offset*dim[1]:dim[1]*(offset+1), -dim[0]:] = window
    return img

# define a class to receive the characteristics of each detected line
class VideoProcess():

    def __init__(self):
        self.detected = False
        self.left_fits = deque(maxlen=10)
        self.right_fits = deque(maxlen=10)
        self.best_left_fit = None
        self.best_right_fit = None

    def pipeline(self, frame):
        # obtain calibration objpoints and imgpoints
        dist_pickle = pickle.load( open( "calibration.p", "rb" ) )
        objpoints = dist_pickle["objpoints"]
        imgpoints = dist_pickle["imgpoints"]

        # create variables to store useful information for image transformation
        img_size = (frame.shape[1], frame.shape[0])
        mtx, dist = cc.cal_undistort(frame, objpoints, imgpoints)
        src = get_corners(img_size, top_bot=(.635,1), top_lr=(.395,.6), bot_lr=(0.105,.955))
        dst = get_corners(img_size, top_bot=(0,1), top_lr=(-.05,1.04), bot_lr=(0.245,.815))

        # undistort image
        undist = cc.undistort(frame, mtx, dist)
        # apply color threshold to obtain a binary image
        s = cgt.hls_thresh(undist, (120,255))
        v = cgt.hsv_thresh(undist, (45,255))
        binary=np.zeros_like(s)
        rgb=cgt.rgb_thresh(undist)
        filter1 = ((s==1) & (v==1))
        binary[filter1| (rgb==1)]=1
        # transform perspective
        binary_warped = ps.warp(binary, src, dst)

        # get result
        nwindow, margin, minpix = 9, 100, 50
        curve, rect_img, left_fit, right_fit, self.detected, left_cur, right_cur = sd.find_curves(binary_warped, nwindow, margin, minpix, self.detected, self.best_left_fit, self.best_right_fit)

        self.left_fits.append(left_fit)
        self.right_fits.append(right_fit)

        self.best_left_fit = np.average(self.left_fits, axis=0)
        self.best_right_fit = np.average(self.right_fits, axis=0)

        new_warp = ps.warp(curve, dst, src)
        result = cv2.addWeighted(undist, 1.0, new_warp, 1.0, 0.0)
        output_result = np.zeros_like(result)

        # add filter images to the final output video
        draw_window(output_result, rect_img, (300,240))
        draw_window(output_result, rgb, (300,240),1)
        draw_window(output_result, binary,(300,240),2)

        # add curvature calculations
        cv2.putText(result, 'Radius of Left Curvature ='+ str(round(left_cur,3))+'(m)', (50,50), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        cv2.putText(result, 'Radius of Right Curvature ='+ str(round(right_cur,3))+'(m)', (50,100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        result = cv2.resize(result, (980, 720))
        output_result[:,:-300] = result

        return output_result
