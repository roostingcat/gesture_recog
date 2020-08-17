import cv2
import imutils
import numpy as np

# set background as global variable

bg = None

# finds the running average over the background
def run_avg(image, aWeight):
    """

    :param image: current frame
    :param aWeight: weight of input image, how fast the accumulator "forgets" about earlier images
    :return: None
    """
    global bg

    if bg is None:
        bg = image.copy().astype("float")
        return

    # calculates weighted average of background
    cv2.accumulateWeighted(image, bg, aWeight)

# segments the hand from the background
def segment(image, threshold=25):
    """

    :param image: current image
    :param threshold: threshold for the difference image
    :return:
    """
    global bg

    # calculates the absolute difference between the background and current frame
    # no difference would mean that the value at the certain position would be close to 0
    diff = cv2.absdiff(bg.astype("uint8"), image)

    # threshold the diff image
    # if certain pixels pass this threshold, we will consider it as the hand region, smaller than threshold = 0
    thresholded = cv2. threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get contours from thresholded which is now a binary image
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None if no contours detected
    if len(cnts) == 0:
        return
    else:
        # get the maximum contour obtaining the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)
