import cv2
import imutils
import numpy as np
from sklearn.metrics import pairwise

def count(thresholded, segmented):
    """

    :param thresholded: threshold of hand
    :param segmented: contour of hand
    :return: number of fingers held up
    """
    # calculates the convexhull of hand contour
    chull = cv2.convexHull(segmented)

    # finds extreme top, bottom, left, and right points of convexhull
    extreme_top = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_bottom = tuple(chull[chull[:, :, 1].argmax()][0])
    extreme_left = tuple(chull[chull[:, :, 0].argmax()][0])
    extreme_right = tuple(chull[chull[:, :, 0].argmax()][0])

    # finds the center of the palm using the extreme points
    cY = int((extreme_top[1] + extreme_bottom[1])/2)
    cX = int((extreme_left[0] + extreme_right[0])/2)

    # find the largest possible radius between center and the extreme points
    distance = pairwise.euclidean_distances(X=[(cX, cY)],
                                            Y=[extreme_bottom, extreme_left, extreme_right, extreme_top])[0]
    maximum_distance = distance[distance.argmax()]

    # create the largest circle
    radius = int(0.8 * maximum_distance)
    circumference = (2 * np.pi * radius)
    circular_roi = np.zeros(thresholded.shape[:2], dtype="uint8")

    # draw the circular ROI
    cv2.circle(circular_roi, (cX, cY), radius, 255, 1)

    # create cuts needed to count fingers
    circular_roi = cv2.bitwise_and(thresholded, thresholded, mask=circular_roi)

    # compute the contours in the circular ROI
    (cnts, _) = cv2.findContours(circular_roi.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # initialize finger count
    count = 0

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)

        # increment finger count as long as not wrist and number of points along contour
        # is less than 25% of circumference
        if ((cY + (cY * 0.25)) > (y + h)) and ((circumference * 0.25) > c.shape[0]):
            count += 1

    return count