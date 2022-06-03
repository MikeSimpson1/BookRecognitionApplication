from skimage.metrics import structural_similarity as ssim
from skimage.transform import resize
import cv2
import numpy as np

import warnings
warnings.filterwarnings("ignore")

def orb_sim(img1, img2):
    orb = cv2.ORB_create()
    _, desc1 = orb.detectAndCompute(img1, None)
    _, desc2 = orb.detectAndCompute(img2, None)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    matches = bf.match(desc1, desc2)
    similar_regions = [i for i in matches if i.distance < 50]
    if len(matches) == 0:
        return 0
    return len(similar_regions) / len(matches)

def structural_sim(img1, img2):
    sim, diff = ssim(img1, img2, full=True, channel_axis=2)
    return sim

def compareImages(img1, img2):
    nums = []
    nums.append(orb_sim(img1,img2))
    img1 = resize(img1, (img2.shape[0], img2.shape[1]), anti_aliasing=True, preserve_range=True)
    nums.append(structural_sim(img2,img1))
    return nums

def Test():
    img1 = cv2.imread('C:/Users/Mike/Desktop/BookAppraisalApplication/book.jpg')
    img2 = cv2.imread('C:/Users/Mike/Desktop/BookAppraisalApplication/petSematary.jpg')
    computeS = compareImages(img1, img2)
    print("ORB similarity is:", computeS[0])
    print("Structural Sim is:", computeS[1])
