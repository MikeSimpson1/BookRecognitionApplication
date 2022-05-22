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
    return intersects

kernel = np.ones((5,5))

img = cv2.imread('C:/Users/Mike/Desktop/BookAppraisalApplication/book.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray_img,(7,7),0)

_, threshold = cv2.threshold(blur, 75, 255, cv2.THRESH_BINARY_INV)
edges = cv2.Canny(threshold, 80, 255)
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

cv2.imshow("Source", img)
cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", blank_image)
blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
contours = cv2.findContours(blank_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
if (len(contours) != 0):
    cv2.drawContours(blank_image, contours, -1, (0, 255, 0), 3)
cv2.imshow("contours", blank_image)

image = np.zeros_like(img , dtype = np.uint8)

intersections = FindIntersections(pointLines)
print(image.shape)
for i in intersections:
    x = math.floor(i[0])
    y = math.floor(i[1])
    print(x)
    if (not(x < 0 or x > image.shape[1] or y < 0 or y > image.shape[0])):
        print(x)
        img = cv2.circle(img, (x,y), radius=5, color=(255,0,0), thickness=-1)
image = cv2.dilate(image,kernel, iterations=1)
cv2.imshow("contours", img)
cv2.waitKey()
