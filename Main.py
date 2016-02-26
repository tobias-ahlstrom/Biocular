import numpy as np
import cv2
from Tkinter import *
import tkFileDialog
import os
import CellCounter as cc

imageNameList = []

class App:

    def __init__(self, master):
        frame = Frame(master)
        frame.pack()
        self.browseButton = Button(top, text ="Choose directory", command = self.browseButtonCallBack)
        self.browseButton.pack(side=LEFT)

        self.fileButton = Button(top, text ="Choose file", command = self.fileButtonCallBack)
        self.fileButton.pack(side=LEFT)

    def browseButtonCallBack(self):
        dirName = tkFileDialog.askdirectory()
        (_, _, filenames) = os.walk(dirName).next()
        for filename in filenames:
            if (filename.endswith('.tif')):
                imageNameList.append(dirName + '/' + filename)

        for imageName in imageNameList:
            numPix, im = cc.countCells(imageName)
            cv2.namedWindow(str(numPix), cv2.WINDOW_AUTOSIZE);
            cv2.imshow(str(numPix), im);

    def fileButtonCallBack(self):
        fileName = tkFileDialog.askopenfilename()
        numPix, im = cc.countCells(fileName)
        cv2.namedWindow(str(numPix), cv2.WINDOW_AUTOSIZE);
        cv2.imshow(str(numPix), im);


top = Tk()
app = App(top)

top.mainloop()
