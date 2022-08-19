import cv2
import numpy as np
import os
import ImageComparison as iCompare
import BookIsolation as bIsolate
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

def CompareAllImages(processedBookCover):
    imageNames = os.listdir('C:/Users/Mike/Desktop/BookAppraisalApplication/BookCovers')
    comparisonData = []
    for fileName in imageNames:
        bookCover = cv2.imread('C:/Users/Mike/Desktop/BookAppraisalApplication/BookCovers/' + fileName)
        if bookCover is not None:
            comparisonData.append([iCompare.compareImages(bookCover, processedBookCover), fileName])
    return comparisonData

def ProcessImage(img):
    return bIsolate.IsolateBookCover(img, img)

def FindBestMatch(arr): #needs changing for different parameters
    best = None
    for nums in arr:
        if best == None or nums[0][0] > best[0][0] or nums[0][1] > best[0][1]:
            best = nums
    return best[1]
def main():
    img = ProcessImage('C:/Users/Mike/Desktop/BookAppraisalApplication/book3.jpg')
    a = CompareAllImages(img)
    print(FindBestMatch(a))

def buttonClick():
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    print("hello")
    ProcessImage(cv2image)

height, width = 480, 640
window = Tk()
window.geometry(str(width)+"x"+str(height))
label = Label(window)
label.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
button = Button(window, text="Capture", command = buttonClick)
button.place(x=(width//2)-10,y=height-30)

def show_frames():
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image = img)
    label.imgtk = imgtk
    label.configure(image=imgtk)
    label.after(5, show_frames)
show_frames()
window.mainloop()
