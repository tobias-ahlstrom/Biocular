import numpy as np
import cv2

def localMaxima(src, squareSize):
    if (squareSize == 0):
        return src

    dst = np.copy(src)
    sqrCenter = (squareSize - 1)/2
    localWindowMask = np.zeros((squareSize, squareSize),np.bool_)
    localWindowMask[sqrCenter, sqrCenter] = 1
    height, width = dst.shape
    for row in range(sqrCenter, height - sqrCenter):
        for col in range(sqrCenter, width - sqrCenter):
            if (dst[row, col] == 0):
                continue
            m0 = dst[row - sqrCenter:row + sqrCenter + 1,col - sqrCenter:col + sqrCenter + 1]
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(m0)
            if (maxLoc[0] == sqrCenter and maxLoc[1] == sqrCenter):
                dst[row - sqrCenter:row + sqrCenter + 1,col - sqrCenter:col + sqrCenter + 1] = localWindowMask*255
                # m0 = np.multiply(m0,localWindowMask)
                col += sqrCenter
    return dst
