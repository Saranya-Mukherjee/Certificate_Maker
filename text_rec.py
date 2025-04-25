import cv2
import numpy as np
import colours

img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
certif = cv2.imread("results/Soham Kanti Paira.jpg", cv2.IMREAD_COLOR)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, colours.c1, colours.c2)

cv2.imshow("certif", certif)
cv2.imshow("mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()