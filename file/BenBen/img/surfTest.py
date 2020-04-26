#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 00:14:36 2020

@author: shuaiwang
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
reprojThresh=4.0
ratio=0.75

WINDOW_NAME = "Test Stitching On Mac"

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)
initialtime = time.time()
cv2.startWindowThread()

img1 =cv2.imread('2.jpg', cv2.IMREAD_GRAYSCALE)
img2 =cv2.imread('1.jpg', cv2.IMREAD_GRAYSCALE)

img11 =cv2.imread('2.jpg', cv2.IMREAD_COLOR)
img22 =cv2.imread('1.jpg', cv2.IMREAD_COLOR)
# img2 =cv2.imread('1.jpg', cv2.IMREAD_COLOR)
sift = cv2.xfeatures2d.SIFT_create()
surf = cv2.xfeatures2d.SURF_create()
orb = cv2.ORB_create(nfeatures=1500)

# keypoints_sift, descriptors = sift.detectAndCompute(img, None)
keypoints_surf11, descriptors1 = surf.detectAndCompute(img1, None)
# keypoints_orb, descriptors = orb.detectAndCompute(img, None)
keypoints_surf22, descriptors2 = surf.detectAndCompute(img2, None)

keypoints_surf1 = np.float32([kp.pt for kp in keypoints_surf11])
keypoints_surf2 = np.float32([kp.pt for kp in keypoints_surf22])
# BFMatcher with default params
bf = cv2.BFMatcher()
matches = bf.knnMatch(descriptors1,descriptors2,k=2)

# Apply ratio test
good = []
for m in matches:
    if len(m) == 2 and m[0].distance < m[1].distance * ratio:
        good.append((m[0].trainIdx, m[0].queryIdx))
        
# computing a homography requires at least 4 matches
if len(good) > 4:
    # construct the two sets of points
    ptsA = np.float32([keypoints_surf1[i] for (_, i) in good])
    ptsB = np.float32([keypoints_surf2[i] for (i, _) in good])

    # compute the homography between the two sets of points
    (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,reprojThresh)


result = cv2.warpPerspective(img11, H,
            (img11.shape[1] + img22.shape[1], img11.shape[0]))

result[0:img22.shape[0], 0:img22.shape[1]] = img22
        
# cv.drawMatchesKnn expects list of lists as matches.
# img3 = cv2.drawMatchesKnn(img11,keypoints_surf1,img22,keypoints_surf2,good,None,flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
# plt.imshow(img3),plt.show()
# img2 = cv2.drawKeypoints(img2, keypoints_sift, (255, 0, 0))
# img2 = cv2.drawKeypoints(img2, keypoints_surf, (0, 255, 0))
# img2 = cv2.drawKeypoints(img2, keypoints_orb, (0, 0, 255))
cv2.waitKey(1000)

cv2.waitKey(1)

# cv2.imshow("Image", img3)
cv2.imshow("Result", result)
cv2.imwrite('result_02_matching_success_myroom.png',result)
cv2.waitKey(0)
cv2.destroyAllWindows()

for i in range (1,5):
    cv2.waitKey(1)
    
initialtime2 = time.time()
print(initialtime2-initialtime2)