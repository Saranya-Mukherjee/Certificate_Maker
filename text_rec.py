import cv2
import numpy as np
import colours

img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
certif = cv2.imread("results/Soham Kanti Paira.jpg", cv2.IMREAD_COLOR)
# certif = cv2.imread("results/Subhadeep Mukherjee.jpg", cv2.IMREAD_COLOR)
# Payra is an example of well formed text, the later is an example of not well formed.
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, colours.c1, colours.c2)
masked = cv2.bitwise_and(certif, certif, mask=mask)

# TODO: Write a function to take in the masked image as an
#  argument and process it to get the text in that

cv2.imshow("masked", masked)
cv2.imshow("certificate", certif)
cv2.waitKey(0)
cv2.destroyAllWindows()