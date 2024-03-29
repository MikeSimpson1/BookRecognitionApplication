import cv2
import numpy as np
import imutils
import math
import IntersectionCalculator as ic

def FindIntersections(pointsLines):
    intersects = []
    for i in range(len(pointsLines)):
        for j in range(len(pointsLines)):
            intersects.append(ic.FindIntersectionWithPoints(pointsLines[i],pointsLines[j]))
    while([0,0] in intersects):
        intersects.remove([0,0])
    return intersects

def SaveImages(originalImage, processedImage):
    filename = 'C:/Users/Mike/Desktop/BookAppraisalApplication/currBookNumber.txt'
    currentNum = None
    try:
        with open(filename, "r") as f:
            c = f.read()
            currentNum = int(c)+1
            f.close()
            f = open(filename, "w")
            f.write(str(currentNum))
            f.close()
    except FileNotFoundError:
        f = open(filename, "x")
        f.write("0")
        f.close()
        currentNum = 0
    SaveOriginalImage(originalImage, currentNum)
    SaveProcessedBookCover(processedImage, currentNum)

def SaveOriginalImage(img, num):
    imgName = "image" + str(num) + ".jpg"
    cv2.imwrite("C:/Users/Mike/Desktop/BookAppraisalApplication/OriginalImages/" + imgName, img)

def SaveProcessedBookCover(img, num):
    imgName = "processedBookCover" + str(num) + ".jpg"
    cv2.imwrite("C:/Users/Mike/Desktop/BookAppraisalApplication/ProcessedBookCovers/" + imgName, img)

def IsolateBookCover(fileName):
    kernel = np.ones((5,5))

    img = cv2.imread(fileName)
    img = cv2.resize(img,(1000,1200))
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray_img,(7,7),0)

    _, threshold = cv2.threshold(blur, 120, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(threshold, 70, 255)
    #cv2.imshow("eee", threshold)
    # Copy edges to the images that will display the results in BGR
    cdst = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    pointLines = []
    lines = cv2.HoughLines(edges, 1, np.pi / 180, 150, None, 0, 0)
    blank_image = np.ones_like(img , dtype = np.uint8)
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            pointLines.append([pt1,pt2])
            cv2.line(blank_image, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)


    linesP = cv2.HoughLinesP(edges, 1, np.pi / 180, 50, None, 50, 10)

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

    #cv2.imshow("Source", img)
    #cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    #cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", blank_image)
    blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(blank_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    if (len(contours) != 0):
        cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
    #cv2.imshow("contours", blank_image)

    image = np.zeros_like(img , dtype = np.uint8)

    intersections = FindIntersections(pointLines)
    intersections = np.float32(ic.FindEdgePoints(intersections, image.shape))

    resizeSize = np.float32([[0,0], [0, image.shape[0]],[image.shape[1], 0], [image.shape[1], image.shape[0]]])
    matrix = cv2.getPerspectiveTransform(intersections, resizeSize)
    outputImg = cv2.warpPerspective(img, matrix, (image.shape[1], image.shape[0]))
    #cv2.imshow("warped", outputImg)
    SaveImages(img, outputImg)
    #cv2.waitKey()
    return outputImg
