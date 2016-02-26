import numpy as np
import cv2
import Tkinter
import tkFileDialog
import os
import CellCounter as cc

imageNameList = []

def browseButtonCallBack():
    dirName = tkFileDialog.askdirectory()
    (_, _, filenames) = os.walk(dirName).next()
    for filename in filenames:
        if (filename.endswith('.tif')):
            imageNameList.append(filename)

    for imageName in imageNameList:
        cc.countCells(imageName)



top = Tkinter.Tk()
browseButton = Tkinter.Button(top, text ="Choose directory", command = browseButtonCallBack)
browseButton.pack()
top.mainloop()
