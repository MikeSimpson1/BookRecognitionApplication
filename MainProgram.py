import cv2
import numpy as np
import os
import ImageComparison as iCompare
import BookIsolation as bIsolate

def CompareAllImages(processedBookCover):
    imageNames = os.listdir('C:/Users/Mike/Desktop/BookAppraisalApplication/BookCovers')
    comparisonData = []
    for fileName in imageNames:
        bookCover = cv2.imread('C:/Users/Mike/Desktop/BookAppraisalApplication/BookCovers/' + fileName)
        comparisonData.append([iCompare.compareImages(bookCover, processedBookCover), fileName])
    return comparisonData

def ProcessImage(img):
    return bIsolate.IsolateBookCover(img)

def FindBestMatch(arr):
    best = None
    for nums in arr:
        if best == None or nums[0][0] > best[0][0]:
            best = nums
    return best[1]

img = ProcessImage('C:/Users/Mike/Desktop/BookAppraisalApplication/book2.png')
a = CompareAllImages(img)
print(FindBestMatch(a))
