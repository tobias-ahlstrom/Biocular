import numpy as np
import cv2


def mywatershed(image, imageT):

    # Use morphological opening and the closing to remove noise and show result
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    # opening = cv2.morphologyEx(imageT, cv2.MORPH_OPEN, kernel, iterations=1)
    # cv2.namedWindow("After opening", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("After opening", opening)
    #
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # sure_bg = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=10)
    sure_bg = cv2.dilate(imageT, kernel, iterations=5)
    cv2.namedWindow("Sure bg", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Sure bg", sure_bg)

    dist_transform = cv2.distanceTransform(sure_bg, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.2*dist_transform.max(),
                                 255, 0)
    cv2.namedWindow("Dist trans", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Dist trans", cv2.normalize(dist_transform, dist_transform, 0, 1., cv2.NORM_MINMAX))

    cv2.namedWindow("Sure fg", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Sure fg", sure_fg)

    unknown = cv2.subtract(sure_bg, sure_fg.astype(np.uint8))
    cv2.namedWindow("unknown", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("unknown", unknown)

    ret, markers = cv2.connectedComponents(sure_fg.astype(np.uint8))
    markers = markers+1
    markers[unknown == 255] = 0
    markers = markers.astype(np.int32)
    markers = cv2.watershed(image, markers)
    image[markers == -1] = [0, 255, 255]

    cv2.namedWindow("Watershed", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Watershed", image)

    return
