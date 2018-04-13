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

After many empirical trials, using a combination of RGB, HSV, and HLS threholds works the best to eliminate noises and detect lane lines accuracly. Below is an example. 
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/undistortion/undistorted-test1.jpg' width='400' title='undistorted' hspace='20'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/color_thresh/color_thresh-test1.jpg' width='400' title='binary'>
</div>

### Perspective transform

After obtaining the binary image of road, we can perform a perspective transform to get a birdeye view of the road lanes. The code is implemented in [perspective_transform.py](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/perspective_transform.py). Use function `get_corners`,implemented in [utils.py](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/utils.py), define source points consists of four corners in the original image, and destination points consists of four corners in the new transformed image as below. 
<img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/birdeye/poly_region.jpg' width=800>

Then use `cv2.getPerspectiveTransform` function to compute the transform matrix, and supply it to `cv2.warpPerspective` function to get the birdeye view of the road image.
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/color_grad/color_grad-test5.jpg' width='400' title='binary' hspace='20'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/birdeye/color_grad_birdeye-test5.jpg' width='400' title='birdeye'>
</div>

### Find lanes>
<p align='middle'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/bianry.jpg' width=200 />
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/histogram.jpg' width=200 />
</p>

<img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/sliding_window.jpg' width=800>
<img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/sliding_window2.jpg' width=600>


### video
You can watch the output video for this project [here](https://www.youtube.com/watch?v=bFBkiqR_XWU&feature=youtu.be)
