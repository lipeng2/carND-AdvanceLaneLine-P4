import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from math import ceil

def plots_images(images, titles=None, rows=1, cmap=None, figsize=(14, 6)):
    '''
    Input:
    images -- list of images
    titles -- optional, titles of images
    rows -- rows of the subplots
    cmap -- optional, if gray, displays for grayscale images
    figsize -- figure size

    Return: None
    '''
    if images == None:
        print('No images found')
        return
    f = plt.figure(figsize=figsize)
    n = len(images)
    cols = ceil(n/rows)
    for i in range(n):
        plt.subplot(rows,cols, i+1 )
        plt.imshow(images[i], cmap=cmap)
        if titles != None:
            plt.title(titles[i])
        plt.axis('off')
    plt.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=None)
    plt.show()

def get_images(dir):
    '''
    Input:
    dir -- directory where images are stored

    Return:
    images -- list of images in RGB format
    '''
    root = os.getcwd()
    images, titles = [], []
    file_path = os.path.join(root,dir)
    for file in os.listdir(file_path):
        img = cv2.imread(os.path.join(root, dir, file))
        images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        titles.append(file)
    return images, titles

def save_images(images, save_dir, titles='no title', prefix='', cmap=None):
    '''
    Input:
    images -- list of images
    save_dir -- desired directory for saving results
    titles -- optional, titles of images
    prefix -- optional, prefix that can be added to images' titles
    cmap -- optional, if gray, images are going to be stored in grayscale

    Return: None
    '''
    if images == None:
        print('No images found')
        return
    num = 0
    for i, img in enumerate(images):
        if titles == 'no title':
            plt.imsave(f'{save_dir}/{prefix}-{i}', img, cmap=cmap)
        else:
            plt.imsave(f'{save_dir}/{prefix}-{titles[i]}', img, cmap=cmap)
        num += 1

    print('Total {} images are saved in {}'.format(num, save_dir))

def get_corners(img_size, top_bot=(0.6, 0.93), top_lr=(0.4, 0.6), bot_lr=(0.2, 0.8)):
    w, h = img_size
    top, bot = top_bot
    top_l, top_r = top_lr
    bot_l, bot_r = bot_lr

    top_left = [int(w*top_l), int(h*top)]
    bot_left = [int(w*bot_l), int(h*bot)]
    bot_right = [int(w*bot_r), int(h*bot)]
    top_right = [int(w*top_r), int(h*top)]
    return np.float32([top_left, bot_left, bot_right, top_right])

def draw_polygon(ims, src):
    for img in ims:
        cv2.polylines(img, [np.int32(src)], True, (255,10,10), 3)
    plots_images(ims, rows=2)

def roi(image, src):
    mask = np.zeros(image.shape, dtype=np.uint8)
    roi_corners = src
    
    channel_count = image.shape[2]  
    ignore_mask_color = (255,)*channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)
    
    # apply the mask
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image
