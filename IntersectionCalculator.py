import cv2
import numpy as np
import imutils
import math


def FindSlope(pt1, pt2):
    if (pt1[0] == pt2[0]):
        return 0
    m = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
    return m

def FindYIntercept(pt, m):
    b = pt[1] - (m * pt[0])
    return b

def FindIntersection(line1,line2):
    if (line1[0] == line2[0]):
        return [0,0]
    x = (line2[1] - line1[1]) / (line1[0] - line2[0])
    y = (line1[0] * x) + line1[1]
    return [x,y]

def EquationOfLine(pt1, pt2):
    m = FindSlope(pt1,pt2)
    b = FindYIntercept(pt1, m)
    return [m, b]

def FindIntersectionWithPoints(pointsForLine1, pointsForLine2):
    line1 = EquationOfLine(pointsForLine1[0], pointsForLine1[1])
    line2 = EquationOfLine(pointsForLine2[0], pointsForLine2[1])
    return FindIntersection(line1,line2)

def FindDistanceBetweenPoints(a, b):
    return math.dist(a,b)

def FindNearestPoint(listOfPoints, point):
    smallestDistance = None
    smallestPoint = None
    for p in listOfPoints:
        distance = FindDistanceBetweenPoints(p, point)
        if smallestDistance == None or smallestDistance > distance:
            smallestDistance = distance
            smallestPoint = p
    return smallestPoint

def FindEdgePoints(listOfPoints, canvasSize):
    topLeft = (0,0)
    topRight = (0, canvasSize[0])
    bottomLeft = (canvasSize[1], 0)
    bottomRight = (canvasSize[1], canvasSize[0])
    extremePoints = []
    extremePoints.append(FindNearestPoint(listOfPoints, topLeft))
    extremePoints.append(FindNearestPoint(listOfPoints, topRight))
    extremePoints.append(FindNearestPoint(listOfPoints, bottomLeft))
    extremePoints.append(FindNearestPoint(listOfPoints, bottomRight))
    return extremePoints

def Testing():
    line1 = EquationOfLine([5,7],[6,3])
    print(EquationOfLine([5,7],[6,3]))
    line2 = EquationOfLine([2,3],[6,2])
    print(line2)
    intersection = FindIntersection(line1,line2)
    print(intersection)
    pointsA = [[5,7],[6,3]]
    pointsB = [[2,3],[6,2]]
    print(FindIntersectionWithPoints(pointsA, pointsB))
