# Hand Gesture Recognition
Recognize hand gestures real time?

## Problems to solve to accomplish task
1. Segment hand region from background
2. Recognize the hand and figure positions into a single gesture

## Segmenting the Hand Region
# Background Subtraction
Use a running average to identify the background, which we will then use to isolate the foreground.

current frame (hand + background) - background = isolated foreground (just hand)

# Motion Detection and Thresholding
Take the absolute difference obtained above and threshold is so values above a certain threshold is 1 and below is 0.

# Contour Extraction
With the threshold, we extract the contour