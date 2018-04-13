# carND-AdvanceLaneLine-P4
The project is designed to robustly detect highway lanes under various pavement and lighting conditions. The solution is devised using a number of image processing algorithms that work on the frames of a video stream of the oncoming road sections taken by a camera mounted on the front windshield of the vehicle. 

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

### Distortion Correction
Then using `cv2.calibrateCamera` and the stored objpoints and imgpoints to compute the camera calibration and distortion coefficients. Lastly, we can apply this distortion correction to the test images using `cv2.undistort`
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/test_images/test1.jpg' width='400' hspace='20' title='distorted'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/undistortion/undistorted-test1.jpg' width='400' title='undistorted'>
</div>

### Apply Color/gradient Threshold to Create Binary Images

After many empirical trials, using a combination of RGB, HSV, and HLS threholds works the best to eliminate noises and detect lane lines accuracly. Below is an example. 
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/undistortion/undistorted-test1.jpg' width='400' title='undistorted' hspace='20'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/color_thresh/color_thresh-test1.jpg' width='400' title='binary'>
</div>

### Perspective Transform

After obtaining the binary image of road, we can perform a perspective transform to get a birdeye view of the road lanes. The code is implemented in [perspective_transform.py](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/perspective_transform.py). Use function `get_corners`,implemented in [utils.py](https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/utils.py), define source points consists of four corners in the original image, and destination points consists of four corners in the new transformed image as below. 
<img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/birdeye/poly_region.jpg' width=800>

Then use `cv2.getPerspectiveTransform` function to compute the transform matrix, and supply it to `cv2.warpPerspective` function to get the birdeye view of the road image.
<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/color_grad/color_grad-test5.jpg' width='400' title='binary' hspace='20'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/birdeye/color_grad_birdeye-test5.jpg' width='400' title='birdeye'>
</div>

### Detect Lanes
After applying calibration, thresholding, and a perspective transform to a road image, the result is a binary image where the lane lines stand out clearly as shown below. First we take a histogram along all the columns in the lower half of the image like this:
```
hist = np.sum(binary_img[height//2:,:], axis=0)
plt.plot(hist)
```

<div align='middle'>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/bianry.jpg' width=400 />
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/histogram.jpg' width=400 />
</div>

and the positions of the two most prominent peaks in the histogram correspond to the x-coordinates of the base for two lanes. These two positions can serve as starting points for where to search for the lines. From that point, a sliding window can be placed around the line center to find and follow the lines up to the top of the frame

<div>
  <img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/sliding_window.jpg' width=800>
</div>

Finally, we will plot all the pixels found within the sliding window region to fit a second degree polynomial using `np.polynomial` function. Example result shown below.

<img src='https://github.com/lipeng2/carND-AdvanceLaneLine-P4/blob/master/output_images/sliding_window2.jpg' width=600>

### Radius of Curvature and Vehicle Position with Respect to Road Center

The radius of curvature of curve at a particular point is defined as the radius of the approximating circle. This radius changes as we move along the lane. The formula for the radius of curvature at a given point is explained [here](https://www.intmath.com/applications-differentiation/8-radius-curvature.php), and the function `curvature` is implemented in [sliding_window.py] for calculating the radius of curvature.

The vehicle position with respect to road center is calculated as followed. First, calculate the road center position by getting the mid point of the ends points from each lane such as`(left_fitx[-1]+right_fitx[-1])/2`, then calculate the center of the road image, which is the position of the vehicle, by doing `img_width/2`, lastly, subtract the two values to get the value of deviation from center. 


### Video
You can watch the output video for this project [here](https://www.youtube.com/watch?v=1x1KWZSZQ0I&feature=youtu.be)

### Discussion
* The biggest problem encountered when implementing the pipeline is getting the correct lanes detected while eliminating all other noises to improve the performance of the algorithm. Gradient thresholding performs quite well at detecting edges, however, it does not eliminate edges created by shadows, therefore, I don't recommend to use any of gradient thresholding. On the other hand, color channel thresholding works suprisingly well at this task. A combination of RGB, HSV, and HLS thresholding is deployed to address the problem. I use RGB threholding for detecting yellow and white lanes, HSV for saturation thresholding, and HLS thresholding to address different lighting conditions.
* The pipeline can certainly be improved by using dynamic color thresholding and dynamic region perspective transformation to enhance its robustness. Additionally, more advanced statistical models can be deployed in finding lane pixels and fitting lanes instead of polynomial method.
* This pipeline is designed primarily to detect highway lanes, and I think it will fail to detect hill road lanes which have significantly shorter straight lanes and more drastic turning lanes.
