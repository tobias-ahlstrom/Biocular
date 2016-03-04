"""Cell counter."""
import cv2
import LocalMaxima as lm
import MyWaterShed as ws
import numpy as np


def gradMagn(image):
    image = cv2.GaussianBlur(image, (3, 3), 0)
    sobelx = cv2.Sobel(image, cv2.CV_32F, 1, 0)
    sobely = cv2.Sobel(image, cv2.CV_32F, 0, 1)
    return cv2.magnitude(sobelx, sobely).astype(np.uint8)

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


def countCells(imagePath):
    """Function for counting cells."""
    # Load and show image
    image = cv2.imread(imagePath, cv2.IMREAD_COLOR)

    cv2.namedWindow("Original Image", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Original Image", image)

    # Extract red channel and show it
    imageR = image[:, :, 2]
    cv2.namedWindow("Red Channel", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Red Channel", imageR)

    # Calculate histogram
    hist = cv2.calcHist([imageR], [0], None, [256], [0, 256])

    # Do hysteres
    _, thresh1 = cv2.threshold(imageR, hist.argmax()+2, 1, cv2.THRESH_BINARY)
    _, thresh2 = cv2.threshold(imageR, 230, 1, cv2.THRESH_BINARY)

    hyst = hysteres(thresh1, thresh2)*255
    cv2.namedWindow("Hysteresis", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Hysteresis", hyst)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    openClose = cv2.morphologyEx(hyst, cv2.MORPH_CLOSE, kernel, iterations=1)
    openClose = cv2.morphologyEx(openClose, cv2.MORPH_OPEN, kernel, iterations=5)
    openClose = cv2.morphologyEx(openClose, cv2.MORPH_CLOSE, kernel, iterations=10)

    cv2.namedWindow("openClosed Hysteresis", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("openClosed Hysteresis", openClose)

    # Laplacian
    imageR = cv2.GaussianBlur(imageR, (3, 3), 0)
    imageR_laplacian = np.zeros(imageR.shape, imageR.dtype)
    imageR = np.multiply(imageR, openClose.astype(np.bool_))
    imageR_laplacian = cv2.Laplacian(imageR, cv2.CV_8U, imageR_laplacian, 1, -2)
    cv2.namedWindow("Laplacian", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Laplacian", imageR_laplacian)

    # Threshold
    ret, iRT = cv2.threshold(imageR_laplacian, 0, 255,
                             cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    iRT = cv2.dilate(iRT, kernel)
    cv2.namedWindow("Thresholded", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Thresholded", iRT)

    # Find contours
    contourImage, contours, hierarchy = cv2.findContours(iRT, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Create empty mask
    mask = np.zeros(imageR.shape, np.uint8)

    # Draw contours for small objects
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 4 < area < 600:
            cv2.drawContours(image, [cnt], 0, (0, 255, 0), 1)
            cv2.drawContours(mask, [cnt], 0, 255, -1)

    cv2.namedWindow("Contours on original", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Contours on original", image)

    cv2.namedWindow("Mask", cv2.WINDOW_AUTOSIZE)
    cv2.imshow("Mask", mask)

    # ws.mywatershed(image, openClose)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # # Filter with negative laplacian filter and show result
    # imageR_laplacian = None
    # imageR_laplacian = cv2.Laplacian(imageR, -1, imageR_laplacian, 3, -1)
    #
    # cv2.namedWindow("Laplacian", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Laplacian", imageR_laplacian)
    #
    # # Threshold the filtered image
    # retval, imageR_laplacian_t = cv2.threshold(imageR_laplacian, 200, 1,
    #                                            cv2.THRESH_BINARY)
    #
    # cv2.namedWindow("Thresholded", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Thresholded", imageR_laplacian_t*255)
    #
    # # Multiply the thresholded image and the filtered one
    # imageR_mult = cv2.multiply(imageR_laplacian, imageR_laplacian_t)
    #
    # cv2.namedWindow("Multiplied", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Multiplied", imageR_mult)
    #
    # # Find regional maxima of the multiplied image
    # imageR_regionalmax = lm.localMaxima(imageR_mult, 15)
    #
    # cv2.namedWindow("imageR_regionalmax", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("imageR_regionalmax", imageR_regionalmax)
    #
    # # Make circels around the red dots
    # height, width = imageR_regionalmax.shape
    # for i in range(0, height):
    #     for j in range(0, width):
    #         if (imageR_regionalmax[i, j] != 0):
    #             cv2.circle(image, (j, i), 4, (0, 255, 255))
    #
    # # Show the circled image
    # cv2.namedWindow("Original Image with circles", cv2.WINDOW_AUTOSIZE)
    # cv2.imshow("Original Image with circles", image)
    #
    # # Print out the number of pixels
    # numberOfPixels = cv2.countNonZero(imageR_regionalmax)
    # return numberOfPixels, image
    return
