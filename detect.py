import pickle

import cv2 as cv
import numpy as np
from moviepy.video.io.VideoFileClip import VideoFileClip

from base import app


# def perform_detection():
def load_camera_matrix():
    camera = pickle.load(open("base/service/models/camera_matrix.pkl", "rb"))
    mtx = camera['mtx']
    dist = camera['dist']
    camera_img_size = camera['imagesize']
    return mtx, dist, camera_img_size


def distort_correct(img, mtx, dist, camera_img_size):
    img_size1 = (img.shape[1], img.shape[0])
    assert (img_size1 == camera_img_size), 'image size is not compatible'
    undist = cv.undistort(img, mtx, dist, None, mtx)
    return undist


def binary_pipeline(img):
    img_copy = cv.GaussianBlur(img, (3, 3), 0)
    s_binary = hls_select(img_copy, sthresh=(140, 255), lthresh=(120, 255))
    x_binary = abs_sobel_thresh(img_copy, thresh=(25, 200))
    y_binary = abs_sobel_thresh(img_copy, thresh=(25, 200), orient='y')
    xy = cv.bitwise_and(x_binary, y_binary)
    mag_binary = mag_threshold(img_copy, sobel_kernel=3, thresh=(30, 100))
    dir_binary = dir_threshold(img_copy, sobel_kernel=3, thresh=(0.8, 1.2))
    gradient = np.zeros_like(s_binary)
    gradient[((x_binary == 1) & (y_binary == 1)) | (
            (mag_binary == 1) & (dir_binary == 1))] = 1
    final_binary = cv.bitwise_or(s_binary, gradient)
    return final_binary


def abs_sobel_thresh(img, orient='x', thresh=(0, 255)):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    if orient == 'x':
        abs_sobel = np.absolute(cv.Sobel(gray, cv.CV_64F, 1, 0))
    if orient == 'y':
        abs_sobel = np.absolute(cv.Sobel(gray, cv.CV_64F, 0, 1))
    scaled_sobel = np.uint8(255 * abs_sobel / np.max(abs_sobel))
    binary_output = np.zeros_like(scaled_sobel)
    binary_output[
        (scaled_sobel >= thresh[0]) & (scaled_sobel <= thresh[1])] = 1
    return binary_output


def mag_threshold(img, sobel_kernel=3, thresh=(0, 255)):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    x = cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=sobel_kernel)
    y = cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=sobel_kernel)
    mag = np.sqrt(x ** 2 + y ** 2)
    scale = np.max(mag) / 255
    eightbit = (mag / scale).astype(np.uint8)
    binary_output = np.zeros_like(eightbit)
    binary_output[(eightbit > thresh[0]) & (eightbit < thresh[1])] = 1
    return binary_output


def dir_threshold(img, sobel_kernel=3, thresh=(0, np.pi / 2)):
    gray = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    x = np.absolute(cv.Sobel(gray, cv.CV_64F, 1, 0, ksize=sobel_kernel))
    y = np.absolute(cv.Sobel(gray, cv.CV_64F, 0, 1, ksize=sobel_kernel))
    direction = np.arctan2(y, x)
    binary_output = np.zeros_like(direction)
    binary_output[(direction > thresh[0]) & (direction < thresh[1])] = 1
    return binary_output


def hls_select(img, sthresh=(0, 255), lthresh=()):
    hls_img = cv.cvtColor(img, cv.COLOR_RGB2HLS)
    L = hls_img[:, :, 1]
    S = hls_img[:, :, 2]
    binary_output = np.zeros_like(S)
    binary_output[(S >= sthresh[0]) & (S <= sthresh[1]) & (L > lthresh[0]) & (
            L <= lthresh[1])] = 1
    return binary_output


def warp_image(img):
    image_size = (img.shape[1], img.shape[0])
    x = img.shape[1]
    y = img.shape[0]
    source_points = np.float32([
        [0.117 * x, y],
        [(0.5 * x) - (x * 0.078), (2 / 3) * y],
        [(0.5 * x) + (x * 0.078), (2 / 3) * y],
        [x - (0.117 * x), y]
    ])
    destination_points = np.float32([
        [0.25 * x, y],
        [0.25 * x, 0],
        [x - (0.25 * x), 0],
        [x - (0.25 * x), y]
    ])
    perspective_transform = cv.getPerspectiveTransform(source_points,
                                                       destination_points)
    inverse_perspective_transform = cv.getPerspectiveTransform(
        destination_points, source_points)
    warped_img = cv.warpPerspective(img, perspective_transform, image_size,
                                    flags=cv.INTER_LINEAR)
    return warped_img, inverse_perspective_transform


def track_lanes_initialize(binary_warped):
    histogram = np.sum(binary_warped[int(binary_warped.shape[0] / 2):, :],
                       axis=0)
    out_img = np.dstack((binary_warped, binary_warped, binary_warped)) * 255
    midpoint = np.int_(histogram.shape[0] / 2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint
    nwindows = 9
    window_height = np.int_(binary_warped.shape[0] / nwindows)
    nonzero = binary_warped.nonzero()
    nonzeroy = np.array(nonzero[0])
    nonzerox = np.array(nonzero[1])
    leftx_current = leftx_base
    rightx_current = rightx_base
    margin = 100
    minpix = 50
    left_lane_inds = []
    right_lane_inds = []
    for window in range(nwindows):
        win_y_low = int(binary_warped.shape[0] - (window + 1) * window_height)
        win_y_high = int(binary_warped.shape[0] - window * window_height)
        win_xleft_low = leftx_current - margin
        win_xleft_high = leftx_current + margin
        win_xright_low = rightx_current - margin
        win_xright_high = rightx_current + margin
        good_left_inds = ((nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (
                nonzerox >= win_xleft_low) & (
                                  nonzerox < win_xleft_high)).nonzero()[0]
        good_right_inds = (
                (nonzeroy >= win_y_low) & (nonzeroy < win_y_high) & (
                nonzerox >= win_xright_low) & (
                        nonzerox < win_xright_high)).nonzero()[0]
        left_lane_inds.append(good_left_inds)
        right_lane_inds.append(good_right_inds)
        if len(good_left_inds) > minpix:
            leftx_current = np.int_(np.mean(nonzerox[good_left_inds]))
        if len(good_right_inds) > minpix:
            rightx_current = np.int_(np.mean(nonzerox[good_right_inds]))
    try:
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)
    except ValueError:
        pass
    leftx = nonzerox[left_lane_inds]
    lefty = nonzeroy[left_lane_inds]
    rightx = nonzerox[right_lane_inds]
    righty = nonzeroy[right_lane_inds]
    return leftx, lefty, rightx, righty, out_img


def fit_polynomial(binary_warped):
    leftx, lefty, rightx, righty, out_img = track_lanes_initialize(
        binary_warped)
    left_fit = np.polyfit(lefty, leftx, 2)
    right_fit = np.polyfit(righty, rightx, 2)
    return left_fit, right_fit


def draw_lane_lines(undist, binary_warped, Minv, left_fit, right_fit):
    ploty = np.linspace(0, binary_warped.shape[0] - 1, binary_warped.shape[0])
    left_fitx = left_fit[0] * ploty ** 2 + left_fit[1] * ploty + left_fit[2]
    right_fitx = right_fit[0] * ploty ** 2 + right_fit[1] * ploty + right_fit[
        2]
    warp_zero = np.zeros_like(binary_warped).astype(np.uint8)
    color_warp = np.dstack((warp_zero, warp_zero, warp_zero))
    pts_left = np.array([np.transpose(np.vstack([left_fitx, ploty]))])
    pts_right = np.array(
        [np.flipud(np.transpose(np.vstack([right_fitx, ploty])))])
    pts = np.hstack((pts_left, pts_right))
    cv.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))
    newwarp = cv.warpPerspective(color_warp, Minv,
                                 (undist.shape[1], undist.shape[0]))
    result = cv.addWeighted(undist, 1, newwarp, 0.3, 0)
    return result


def process_image(img):
    mtx, dist, camera_img_size = load_camera_matrix()
    undist = distort_correct(img, mtx, dist, camera_img_size)
    binary_img = binary_pipeline(undist)
    warped_img, Minv = warp_image(binary_img)
    left_fit, right_fit = fit_polynomial(warped_img)
    result = draw_lane_lines(undist, warped_img, Minv, left_fit, right_fit)
    return result


def ai_inference(input_video):
    output_video_file_name = "output_" + input_video.split('/')[-1]
    output_video = app.config['output_video_path'] + output_video_file_name
    clip1 = VideoFileClip(input_video)
    new_clip = clip1.set_fps(15)
    white_clip = new_clip.fl_image(process_image)
    white_clip.write_videofile(output_video, audio=False)
    return output_video_file_name
