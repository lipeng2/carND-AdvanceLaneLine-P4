# carND-AdvanceLaneLine-P4

## Overview

The steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

### Camera Calibration
The [road images](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/tree/master/test_images)obtained from the camera are distorted, and undistortion can undermine the accuracy of lane detection and the calculation of radius of curvatures. Therefore, we need to first calibrate the camera and undistort road images. The code for calibrating camera is implemented in [camera_calibration.py](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/camera_calibration.py). 

There are 20 calibration images of a 9x6 chessboard are taken from different angles. We use `cv2.findChessboardCorners` to obtain corners points and object points for each calibration image, and store them in [calibration.p](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/calibration.p). 
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/camera_cal/calibration2.jpg' width='400' hspace='20'/> 
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/find_corners/corners-calibration2.jpg' width='400'/>
</div>

### Distortion correction
Then using `cv2.calibrateCamera` and the stored objpoints and imgpoints to compute the camera calibration and distortion coefficients. Lastly, we can apply this distortion correction to the test images using `cv2.undistort`
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/test_images/test1.jpg' width='400' hspace='20' title='distorted'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/undistortion/undistorted-test1.jpg' width='400' title='undistorted'>
</div>

### Apply color/gradient threshold to create binary images

After many empirical trials, we dicoveried that RGB, HSV, and HLS threholding works the best to eliminate noises and detect lane lines accuracly. 
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/undistortion/undistorted-test1.jpg' width='400' title='undistorted' hspace='20'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/color_thresh/color_thresh-test1.jpg' width='400' title='binary'>
</div>

### video
You can watch the output video for this project [here](https://www.youtube.com/watch?v=bFBkiqR_XWU&feature=youtu.be)
