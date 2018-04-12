from utils import *
import numpy as np
import pickle
import cv2


def get_obj_img(ims, nx, ny, t=None):
    '''
    Input:
    ims -- list of images for calibrations
    nx -- x dimension of image for calibration
    ny -- y dimension of image for calibration
    t -- optional, titles of images

    Return:
    objpoints -- 3D points in real world
    imgpoints -- 2D points in image plane
    images -- list of images
    titles -- list of titles of images
    '''
    # arrays for storing return values
    objpoints, imgpoints, images, titles = [], [], [], []
    objp = np.zeros((nx*ny, 3), np.float32)
    objp[:,:2] = np.mgrid[0:nx,0:ny].T.reshape(-1,2) # x, y coordinates

    for i, img in enumerate(ims):
        # convert images to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

        # find corners
        ret, corners = cv2.findChessboardCorners(gray, (nx,ny), None)

        # if corners found, add object points, image points
        if ret == True:
            imgpoints.append(corners)
            objpoints.append(objp)
            img = cv2.drawChessboardCorners(img, (nx, ny), corners, ret)
            images.append(img)
            if t!=None:
                titles.append(t[i])

    return objpoints, imgpoints, images, titles


def cal_undistort(img, objpoints, imgpoints):
    '''
    Input:
    img -- an image
    objpoints -- 3D points in real world
    imgpoints -- 2D points in image plane

    Return:
    undistorted version of given image
    '''
    # use cv2.calibrateCamera to get distortion coefficients
    _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, img.shape[1::-1], None, None)

    # use cv2.undistort to undistort the given image
    return mtx, dist


def undistort(img, mtx, dist):
    '''
    Input:
    ims -- an image
    objpoints -- 3D points in real world
    imgpoints -- 2D points in image plane

    Return:
    undists -- undistorted version of given image
    '''

    return cv2.undistort(img, mtx, dist, None, mtx)



# # get images for calibrations
# cal_images, cal_titles = get_images('camera_cal')
# nx, ny = 9, 6

# # get objpoints and imgpoints for calibrations
# objpoints, imgpoints, corner_images, cor_titles = get_obj_img(cal_images,nx, ny,  t=cal_titles)
# # save objpoints and imgpoints
# dist_pickle = {}
# dist_pickle["objpoints"] = objpoints
# dist_pickle["imgpoints"] = imgpoints
# pickle.dump( dist_pickle, open( "calibration.p", "wb" ) )

# # visualize corners drawn on chessboard
# plots_images(corner_images, titles=cor_titles, rows=4)
#
# # save corner_images
# save_images(corner_images, titles=cor_titles, save_dir='progress/find_corners', prefix='corners')

# # get undistorted images
# undists = undistort(cal_images, objpoints, imgpoints)

# # visulize undistorted images
# plots_images(undists[0], cal_titles, rows=1)
# # save undistorted images
# save_images(undists, titles=cal_titles, save_dir='progress/undistortion', prefix='undistorted')

# read in the store info and get undistorted images
# dist_pickle = pickle.load( open( "calibration.p", "rb" ) )
# objpoints = dist_pickle["objpoints"]
# imgpoints = dist_pickle["imgpoints"]
# undists = undistort(cal_images, objpoints, imgpoints)
# plt.imshow(undists[0])
# plt.show()
