"""
SpectralGUI class
GUI for the SpectralOne Class
Displays NDVI images from the Sentera camera
Developed for Remote Sensing TIPS project (2019)
Keegan Campanelli
Still In Development:
    2D Calibration of NDVI images
    Live view of images
"""

from tkinter import *
from PIL import ImageTk, Image
from enum import Enum
import SpectralControl as sc

class SpectralGUI:

    def __init__(self):
        self.initUI()
        self.packUI()
        self.spect = sc.SpectralControl()
        self.state = 0

        self.window.mainloop()

    def initUI(self):
        self.window = Tk()
        self.window.title('SpectralOne')

        #UI Elements
        self.imgFrame =Frame(self.window, borderwidth=5)
        self.buttonFrame = Frame(self.window, borderwidth=5, relief = RIDGE)

        #button declarations
        #self.save_button = Button(self.buttonFrame, text='Save', command = self.saveImg)
        self.next_button = Button(self.buttonFrame, text='Next Image', command = self.nextImg)
        self.cal_button = Button(self.buttonFrame, text='Calibrate Image', command = self.calibrateImg)

        #Image frame
        self.path = self.saveImg()
        self.img = ImageTk.PhotoImage(Image.open(self.path))

        #UI Elements
        self.panel = Label(self.imgFrame, image = self.img)
        self.panel.bind("<Button-1>", self.getMouseCoords)


    def packUI(self):
        #Pack elements
        self.imgFrame.pack(fill = X)
        self.buttonFrame.pack(fill = BOTH)
        self.next_button.pack(side = RIGHT, padx = 5, pady = 5)
        #self.save_button.pack(side = RIGHT, padx = 5, pady = 5)
        self.cal_button.pack(side = RIGHT, padx = 5, pady = 5)
        self.panel.pack()

    def saveImg(self):
        return self.spect.getImg();

    def nextImg(self):
        #print("Next Image")
        self.path = self.saveImg()
        self.img = ImageTk.PhotoImage(Image.open(self.path))
        self.panel.configure(image = self.img)
        self.panel.img = self.img
        print(self.path)

    def calibrateImg(self):
        if(self.state == 0):
            self.state = 1
            self.cal_button.config(text='Cancel Calibration')
            self.window.config(cursor='target')
        else:
            self.state = 0
            self.cal_button.config(text='Calibrate Image')
            self.window.config(cursor='arrow')

    def getImgPath(self):
        return "C:\\Users\\Keegan\\Documents\\HoloLens\\2D GUI\\tips_test1_nir.jpg"

    def getMouseCoords(self, event):
        if(self.state == 1):
            print('X:', event.x)
            print('Y:', event.y)

gui = SpectralGUI()
