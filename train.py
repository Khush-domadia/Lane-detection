import glob
import pickle

import cv2 as cv
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

images = glob.glob(
    'D:\projectworkspace\LinesOfDestiny/base/service/camera_cal/calibration*')

img = mpimg.imread(images[0])
plt.imshow(img)

# store chessboard coordinates
chess_points = []
# store points from transformed img
image_points = []

# board is 6 rows by 9 columns. each item is one (xyz) point
# remember, only care about inside points. that is why board is 9x6, not 10x7
chess_point = np.zeros((9 * 6, 3), np.float32)
# z stays zero. set xy to grid values
chess_point[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

for image in images:

    img = mpimg.imread(image)
    # convert to grayscale
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)

    # returns boolean and coordinates
    success, corners = cv.findChessboardCorners(gray, (9, 6), None)

    if success:
        image_points.append(corners)
        # these will all be the same since it's the same board
        chess_points.append(chess_point)
    else:
        print('corners not found {}'.format(image))

image = mpimg.imread('/base/service/camera_cal/calibration2.jpg')

plt.figure()
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(image)
ax1.set_title('Captured Image', fontsize=30)

gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
ret, corners = cv.findChessboardCorners(gray, (9, 6), None)
if ret == False:
    print('corners not found')
img1 = cv.drawChessboardCorners(image, (9, 6), corners, ret)

ax2.imshow(img1)
ax2.set_title('Corners drawn Image', fontsize=30)
plt.tight_layout()
plt.savefig('saved_figures/chess_corners.png')
plt.show()
points_pkl = {}
points_pkl["chesspoints"] = chess_points
points_pkl["imagepoints"] = image_points
points_pkl["imagesize"] = (img.shape[1], img.shape[0])
pickle.dump(points_pkl, open("models/object_and_image_points.pkl", "wb"))
