import numpy as np
import cv2
from matplotlib import pyplot as plt

def hysteres(tLow, tHigh):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    arr = np.copy(tHigh)
    arr = cv2.dilate(arr, kernel)
    arr = np.multiply(arr, tLow)
    while not np.array_equal(arr, tHigh):
        tHigh = np.copy(arr)
        arr = cv2.dilate(arr, kernel)
        arr = np.multiply(arr, tLow)
    return arr

def mywatershed(image):

    imageR = image[:, :, 2]

    # Calculate and show Histogram
    # plt.hist(image.ravel(), 256, [0, 256])
    hist = cv2.calcHist([imageR], [0], None, [256], [0, 256])
    # plt.show()

    # Threshhold and show result
    # ret, thresh = cv2.threshold(image, 0, 255,
    #                             cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    _, thresh1 = cv2.threshold(imageR, hist.argmax()+1, 1, cv2.THRESH_BINARY)

    _, thresh2 = cv2.threshold(imageR, 220, 1, cv2.THRESH_BINARY)

    hyst = hysteres(thresh1, thresh2)*255
    cv2.namedWindow("Hysteresis", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Hysteresis", hyst)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    openClose = cv2.morphologyEx(hyst, cv2.MORPH_OPEN, None, iterations=5)
    openClose = cv2.morphologyEx(openClose, cv2.MORPH_CLOSE, None, iterations=10)

    cv2.namedWindow("openClose", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("openClose", openClose)

    # # Use morphological opening and the closing to remove noise and show result
    # # kernel = np.ones((5, 5), np.uint8)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    # opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel, iterations=1)
    # cv2.namedWindow("After opening", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("After opening", opening)
    #
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # # sure_bg = cv2.dilate(opening, kernel, iterations=9)
    # sure_bg = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=10)
    # sure_bg = cv2.dilate(sure_bg, kernel, iterations=10)
    # cv2.namedWindow("Sure bg", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Sure bg", sure_bg)
    #
    # dist_transform = cv2.distanceTransform(sure_bg, cv2.DIST_L2, 5)
    # ret, sure_fg = cv2.threshold(dist_transform, 0.2*dist_transform.max(),
    #                              255, 0)
    # cv2.namedWindow("Dist trans", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Dist trans", cv2.normalize(dist_transform, dist_transform, 0, 1., cv2.NORM_MINMAX))
    #
    # cv2.namedWindow("Sure fg", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Sure fg", sure_fg)
    #
    # unknown = cv2.subtract(sure_bg, sure_fg.astype(np.uint8))
    # cv2.namedWindow("unknown", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("unknown", unknown)
    #
    # ret, markers = cv2.connectedComponents(sure_fg.astype(np.uint8))
    # markers = markers+1
    # markers[unknown == 255] = 0
    # markers = markers.astype(np.int32)
    # markers = cv2.watershed(image, markers)
    # image[markers == -1] = [0, 255, 255]
    #
    # cv2.namedWindow("Watershed", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Watershed", image)

    # plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return
