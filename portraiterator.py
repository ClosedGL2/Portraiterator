import numpy as np
import cv2
import os

originalimgdir = input('Original image: ')
portraitimgdir = input('Directory containing images for portrait: ')
outputimgdir = input('Output image file: ')

# add / to end of portraitimgdir if there isn't one
if portraitimgdir[-1] != '/' or portraitimgdir[-1] != '\\':
    portraitimgdir += '/'

# load original image
print('Loading original image')
originalimg = cv2.imread(originalimgdir, cv2.IMREAD_COLOR)

# check if image dimensions are divisible by 25
if (originalimg.shape[0] / 25) != int(originalimg.shape[0] / 25) or (originalimg.shape[1] / 25) != int(originalimg.shape[1] / 25):
    print('Original image width and height must be divisible by 25!')
    exit()

# list directories, add portraitimgdir to beginning of each directory
print('Loading portrait images')
imgfiles = os.listdir(portraitimgdir)
for i in range(len(imgfiles)):
    imgfiles[i] = portraitimgdir + imgfiles[i]

# load portrait images, resizing them to 25x25
portraitimgs = []
for i in imgfiles:
    portraitimg = cv2.imread(i, cv2.IMREAD_COLOR)
    portraitimg = cv2.resize(portraitimg, (25, 25), interpolation=cv2.INTER_AREA)
    portraitimgs.append(portraitimg)

# delete unused variables to save RAM
del portraitimg
del imgfiles

# split original image into 25x25 squares
print('Splitting original image into 25x25 squares')
originalimgsquares = []
for y in range(int(originalimg.shape[0] / 25)):
    for x in range(int(originalimg.shape[1] / 25)):
        square = np.zeros((25, 25, 3), np.uint8)
        for xx in range(25):
            for yy in range(25):
                pxx = (x * 25) + xx
                pxy = (y * 25) + yy
                square[yy, xx] = originalimg[pxy, pxx]
        originalimgsquares.append(square)

# Create blank image for output
print('Creating blank canvas image')
outputimg = np.zeros((int(originalimg.shape[0]), int(originalimg.shape[1]), 3), np.uint8)

# delete unused variables to save RAM
del originalimg
del square

# assemble output image
print('Assembling output image...')
i = 0
for y in range(int(outputimg.shape[0] / 25)):
    for x in range(int(outputimg.shape[1] / 25)):
        # find portrait image with least loss
        print('Finding portrait image for square (' + str(x) + ', ' + str(y) + ')')
        lowestloss = 480000
        for img in portraitimgs:
            # calculate loss
            loss = 0
            for yy in range(25):
                for xx in range(25):
                    px1 = originalimgsquares[i][yy, xx]
                    px2 = img[yy, xx]
                    loss += abs(px1[0] - px2[0]) + abs(px1[1] - px2[1]) + abs(px1[2] - px2[2])

            # compare loss with lowest loss
            if loss < lowestloss:
                lowestloss = loss
                closestimg = img
        
        # draw portrait image on canvas
        print('Drawing square (' + str(x) + ', ' + str(y) + ')')
        for xx in range(25):
            for yy in range(25):
                pxx = (x * 25) + xx
                pxy = (y * 25) + yy
                outputimg[pxy, pxx] = closestimg[yy, xx]
        
        i += 1

# save output image
print('Saving image')
cv2.imwrite(outputimgdir, outputimg)