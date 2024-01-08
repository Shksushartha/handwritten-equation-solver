from Utils import detect_contours
import cv2
from matplotlib import pyplot as plt
def LineSegmentation(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh2 = cv2.threshold(img_gray, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (400, 2))
    mask = cv2.morphologyEx(thresh2, cv2.MORPH_DILATE, kernel)

    bboxes = []
    bboxes_img = img.copy()
    contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    for cntr in contours:
        x, y, w, h = cv2.boundingRect(cntr)
        cv2.rectangle(bboxes_img, (x, y), (x + w, y + h), (0, 0, 255), 1)
        bboxes.append((x, y, w, h))

    return bboxes

def CharacterSegmentation(img1, x,y,w,h):
    keep = detect_contours(x, y, w, h, img1)
    return keep
