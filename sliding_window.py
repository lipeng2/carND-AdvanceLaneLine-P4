import cv2
import numpy as np
import matplotlib.pyplot as plt

def get_base_pos(binary_warped):
    '''
    Input:
    binary_warped -- a binary birdeye image

    Return:
    leftx_base -- x-coordinate of left lane at the bottom of the image
    rightx_base -- x-coordinate of right lane at the bottom of the image
    '''
    # get image size
    height = binary_warped.shape[0]
    width = binary_warped.shape[1]
    # take histogram of the bottom half of the image
    hist = np.sum(binary_warped[height//2:,:], axis=0)
    # find peaks of left and right lanes
    midpoint = width//2
    leftx_base = np.argmax(hist[:midpoint])
    rightx_base = np.argmax(hist[midpoint:]) + midpoint

    return leftx_base, rightx_base

def window_mask(x_current, margin):
    '''
    Create left and right of window_mask's x-coords
    '''
    win_x_low = x_current - margin
    win_x_high = x_current + margin

    return win_x_low, win_x_high

def good_inds(y, x, y_low, y_high, x_low, x_high):
    '''
    returns indices of pixels locates within the boundaries
    '''
    return ((y>=y_low)&(y<y_high)&(x>=x_low)&(x<x_high)).nonzero()[0]

def curvature(y, x, ym_per_pix, xm_per_pix):
    '''
    Input:
    y -- y-coordinates
    x -- x-coordinates
    ym_per_pix -- coversion from pixel to meter in y direction
    xm_per_pix -- coversion from pixel to meter in x direction

    Return:
    radius of given curvature in meters
    '''
    fit_cr = np.polyfit(y*ym_per_pix, x*xm_per_pix, 2)
    return ((1+(2*fit_cr[0]*y[-1]*ym_per_pix + fit_cr[1])**2)**1.5) / np.absolute(2*fit_cr[0])

# helper function
def get_region(left_fitx, right_fitx, margin, ploty):
    '''
    get region pixels of given lanes and center of roads
    '''
    left_line_window1 = np.array([np.transpose(np.vstack([left_fitx-margin, ploty]))])
    left_line_window2 = np.array([np.flipud(np.transpose(np.vstack([left_fitx+margin, ploty])))])
    left_line_pts = np.hstack((left_line_window1, left_line_window2))
    right_line_window1 = np.array([np.transpose(np.vstack([right_fitx-margin, ploty]))])
    right_line_window2 = np.array([np.flipud(np.transpose(np.vstack([right_fitx+margin, ploty])))])
    right_line_pts = np.hstack((right_line_window1, right_line_window2))
    inner_line_pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    inner_line_pts_right =  np.array([np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    inner_line_pts = np.hstack((inner_line_pts_left, inner_line_pts_right))

    return left_line_pts, right_line_pts, inner_line_pts

# helper function
def fill_region(img, left_line_pts, right_line_pts, inner_line_pts, dir='straight'):
    '''
    fill colors in given regions
    '''
    window_img = np.zeros_like(img)
    cv2.fillPoly(window_img, np.int_([left_line_pts]), (0,255, 0))
    cv2.fillPoly(window_img, np.int_([right_line_pts]), (0,255, 0))
    if dir == 'straight':
        cv2.fillPoly(window_img, np.int_([inner_line_pts]), (255,255,0))
    if dir == 'right':
        cv2.fillPoly(window_img, np.int_([inner_line_pts]), (120,0,0))
    if dir == 'left':
        cv2.fillPoly(window_img, np.int_([inner_line_pts]), (0,0,120))
    return window_img

# helper function
def get_direction(left_cur, right_cur, diff):
    '''
    get direction of the vehicle is heading
    '''
    if left_cur > 1200 and right_cur > 1200:
        direction = 'straight'
    elif diff > 210:
        direction = 'right'
    elif diff < -180:
        direction = 'left'
    else:
        direction = 'straight'
    return direction

# helper function
def skip_slide_window(binary_warped, left_fit, right_fit, margin=100):
    '''
    get all lane pixels given lanes detected from the previous frame
    '''
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])

    left_lane_inds = ((nonzerox > (left_fit[0]*(nonzeroy**2) + left_fit[1]*nonzeroy +
    left_fit[2] - margin)) & (nonzerox < (left_fit[0]*(nonzeroy**2) +
    left_fit[1]*nonzeroy + left_fit[2] + margin)))

    right_lane_inds = ((nonzerox > (right_fit[0]*(nonzeroy**2) + right_fit[1]*nonzeroy +
    right_fit[2] - margin)) & (nonzerox < (right_fit[0]*(nonzeroy**2) +
    right_fit[1]*nonzeroy + right_fit[2] + margin)))

    return left_lane_inds, right_lane_inds

def find_curves(binary_warped, nwindows=9, margin=100, minpix=50, detected=False, prev_left_fit=None, prev_right_fit=None, curve_diff=0):
    # get image size
    height = binary_warped.shape[0]
    width = binary_warped.shape[1]
    # crate an output image to draw on
    out_img = np.dstack((binary_warped, binary_warped, binary_warped))*255
    # find peaks of left and right lanes
    leftx_base, rightx_base = get_base_pos(binary_warped)
    # set height of windows
    window_height = height // nwindows
    # identify the x and y positions of all nonzeros pixels in the image
    nonzero_y, nonzero_x = binary_warped.nonzero()
    # current positions to be updated for each window
    leftx_current, rightx_current = leftx_base, rightx_base
    # create empty lists to receive left and right lane pixel indices
    left_lane_inds, right_lane_inds = [], []

    ploty = np.linspace(0, height-1, height)

    if detected:
        left_lane_inds, right_lane_inds = skip_slide_window(binary_warped, prev_left_fit, prev_right_fit, margin)

    else:
    # step through the windows one by one
        for window in range(nwindows):
          # identify window boundaries in x and y (and right and left)
          win_y_low = height - (window+1)*window_height
          win_y_high = height - window*window_height
          win_xleft_low, win_xleft_high = window_mask(leftx_current, margin)
          win_xright_low, win_xright_high = window_mask(rightx_current, margin)

          # draw the windows on the visualization image
          cv2.rectangle(out_img, (win_xleft_low, win_y_low), (win_xleft_high, win_y_high), (0,255,0),2)
          cv2.rectangle(out_img, (win_xright_low, win_y_low), (win_xright_high, win_y_high), (0,255,0),2)

          # identify the nonzero pixels in x and y within the window
          good_left_inds = good_inds(nonzero_y, nonzero_x, win_y_low, win_y_high, win_xleft_low, win_xleft_high)
          good_right_inds = good_inds(nonzero_y, nonzero_x, win_y_low, win_y_high, win_xright_low, win_xright_high)

          left_lane_inds.append(good_left_inds)
          right_lane_inds.append(good_right_inds)

          # if you found >  pixels, recenter next window on their mean position
          if len(good_left_inds) > minpix:
              leftx_current = np.int(np.mean(nonzero_x[good_left_inds]))

          if len(good_right_inds) > minpix:
              rightx_current = np.int(np.mean(nonzero_x[good_right_inds]))

        # concatenate the arrays of indices
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

    # extract left and right line pixel positions
    leftx, lefty = nonzero_x[left_lane_inds], nonzero_y[left_lane_inds]
    rightx, righty = nonzero_x[right_lane_inds], nonzero_y[right_lane_inds]

    detected = False if len(leftx) + len(rightx) < 450 else True

    # fit a second order polynomial to each
    if detected:
        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

    else:
        left_fit = prev_left_fit
        right_fit = prev_right_fit

    left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
    right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]

    out_img[nonzero_y[left_lane_inds], nonzero_x[left_lane_inds]] = [255, 0, 0]
    out_img[nonzero_y[right_lane_inds], nonzero_x[right_lane_inds]] = [0, 0, 255]

    left_cur = curvature(ploty, left_fitx, 30/720, 3.7/700)
    right_cur = curvature(ploty, right_fitx, 30/720, 3.7/700)
    direction = get_direction(left_cur, right_cur, curve_diff)
    camera_center = (left_fitx[-1] + right_fitx[-1])/2
    center_diff = (camera_center-width/2)*3.7/700

    # draw region
    left_line_pts, right_line_pts, inner_line_pts = get_region(left_fitx, right_fitx, margin, ploty)
    window_img = fill_region(out_img, left_line_pts, right_line_pts, inner_line_pts, direction)

    result = cv2.addWeighted(out_img, 1, window_img, 0.5, 0)

    return result, out_img, left_fit, right_fit, detected, left_cur, right_cur, center_diff
