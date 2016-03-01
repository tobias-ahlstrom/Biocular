"""Cell counter."""
import cv2
import LocalMaxima as lm
import MyWaterShed as ws


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

    ws.mywatershed(image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

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
