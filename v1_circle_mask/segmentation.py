import cv2
import imutils
from count import count

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
    thresholded = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)[1]

    # get contours from thresholded which is now a binary image
    (cnts, _) = cv2.findContours(thresholded.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # return None if no contours detected
    if len(cnts) == 0:
        return
    else:
        # get the maximum contour obtaining the hand
        segmented = max(cnts, key=cv2.contourArea)
        return (thresholded, segmented)

if __name__ == "__main__":
    aWeight = 0.5

    # get default camera of device
    camera = cv2.VideoCapture(0)

    # region of interest (ROI) coordinates
    top, right, bottom, left = 10, 350, 225, 590

    # initialize the number of frames
    num_frames = 0
    while(True):
        # grabs, decodes, and returns current frame
        (grabbed, frame) = camera.read()

        # resize the frame
        frame = imutils.resize(frame, width=700)

        # flip frame to avoid mirror image
        frame = cv2.flip(frame, 1)

        # clone the frame
        clone = frame.copy()

        # get the height and width of the frame
        (height, width) = frame.shape[:2]

        # get the ROI, numpy slicing
        roi = frame[top:bottom, right:left]

        # findContours requires a monochrome image, so we must turn frame to black and white
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (7, 7), 0)

        # compute the running average over 30 frames, this is now the background
        # after 30 frames, we segment. Anything added is now the foreground
        if num_frames<30:
            run_avg(gray, aWeight)
        else:
            hand = segment(gray)

            if hand is not None:
                (thresholded, segmented) = hand
                cv2.drawContours(clone, [segmented + (right, top)], -1, (0, 0, 255))
                cv2.imshow("Thesholded", thresholded)

                # count the number of fingers
                fingers = count(thresholded, segmented)
                cv2.putText(clone, str(fingers), (70, 45), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # draw the segmented hand
        cv2.rectangle(clone, (left, top), (right, bottom), (0, 255, 0), 2)

        # increment frames
        num_frames += 1

        cv2.imshow("Video Feed", clone)

        keypress = cv2.waitKey(1) & 0xFF
        if keypress == ord("q"):
            break

camera.release()
cv2.destroyAllWindows()

