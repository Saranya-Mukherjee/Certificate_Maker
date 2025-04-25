import cv2
import numpy as np
import colours
import pytesseract
import time

padding = 10

img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask_of_area = cv2.inRange(hsv, colours.c1, colours.c2)

# certif = cv2.imread("results/Soham Kanti Paira.jpg", cv2.IMREAD_COLOR)
# certif = cv2.imread("results/Subhadeep Mukherjee.jpg", cv2.IMREAD_COLOR)
# Payra is an example of well formed text, the later is an example of not well formed.

def get_text_from_img(image, text_bounds):
    global n
    mask = np.zeros(image.shape[:2], dtype="uint8")
    cv2.rectangle(mask, (text_bounds[0]-padding, text_bounds[1]-padding), (text_bounds[2]+padding, text_bounds[3]+padding), 255, -1)
    mask = cv2.bitwise_and(mask, mask, mask=mask_of_area)
    masked = cv2.bitwise_and(image, image, mask=mask)
    gray = cv2.cvtColor(masked, cv2.COLOR_BGR2GRAY)
    _, masked = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # cv2.imshow("Rectangular Mask", masked)
    config = '--oem 1 --psm 7'
    text = pytesseract.image_to_string(masked, config=config)
    processed = ""
    for t in text:
        if t.isalpha():
            processed += t
        else:
            processed += " "
    processed = processed.strip()
    processed = processed.lower()
    processed = processed.title()
    print("HEHEHE", processed)
    return processed