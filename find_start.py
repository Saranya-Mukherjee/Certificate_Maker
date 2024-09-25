import cv2
import numpy as np
import colours

img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
certif = cv2.imread("1st.png", cv2.IMREAD_COLOR)
certif = cv2.resize(certif, (0, 0), fx=0.5, fy=0.5)
certificate = cv2.imread("1st.png", cv2.IMREAD_COLOR)
certificate = cv2.resize(certificate, (0, 0), fx=0.5, fy=0.5)
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

height, width, _ = certif.shape
print('width:  ', width)
print('height: ', height)

def text_contour(x, y, w, h, col, scale, text):
    # centering the text in the rectangle
    blank = 255 * np.ones_like(certif, dtype=np.uint8)
    blank_cp = 255 * np.ones_like(certif, dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (x + w // 2, int(y + h / 1))
    fontScale = scale
    color = (0, 0, 0)
    thickness = 2
    text_im = str(text)
    blank = cv2.putText(blank, text_im, org, font, fontScale, color, thickness, cv2.LINE_AA)
    blank_cp = cv2.putText(blank_cp, text_im, org, font, fontScale, color, thickness, cv2.LINE_AA)
    blank = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)
    contours2, _ = cv2.findContours(image=blank, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(image=certif, contours=contours2, contourIdx=-1, color=(col, 255, 0), thickness=2,
                     lineType=cv2.LINE_AA)
    contours2 = list(contours2)
    contours2.pop(0)
    a, b, c, d = cv2.boundingRect(contours2[0])
    text = [a, b, a + c, b + d]
    for contour2 in contours2:
        x, y, w, h = cv2.boundingRect(contour2)
        # cv2.rectangle(certif, (x, y), (x + w, y + h), (0, 255, 255), 2)
        # print(x, y, x + w, y + h, text)
        if text[0] > x:
            text[0] = x
        if text[1] > y:
            text[1] = y
        if text[2] < (x + w):
            text[2] = (x + w)
        if text[3] < (y + h):
            text[3] = (y + h)
    pad = 5
    text[0] -= pad
    text[1] -= pad
    text[2] += pad
    text[3] += pad
    return text, blank_cp

def center_test(x,y,w,h,col,scale, text_in):
    text, _ = text_contour(x, y, w, h, col=255, scale=1, text = text_in)
    x,y,w,h = x,y,w,h
    diff = width
    counter = 0
    while abs(diff)>10:
        center_text = [(text[0] + text[2]) // 2, (text[1] + text[3]) // 2]
        diff = (width // 2) - center_text[0]
        print(center_text, diff)
        x, y, w, h = x, y, w + diff * 2, h
        text, _ = text_contour(x, y, w, h, col = col, scale= scale, text = text_in)
        counter += 1
        if counter>10:
            break
    return x,y,w,h,diff

def do_all_the_fucking_work(name):
    img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
    certif = cv2.imread("1st.png", cv2.IMREAD_COLOR)
    certif = cv2.resize(certif, (0, 0), fx=0.5, fy=0.5)
    certificate = cv2.imread("1st.png", cv2.IMREAD_COLOR)
    certificate = cv2.resize(certificate, (0, 0), fx=0.5, fy=0.5)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, colours.c1, colours.c2)

    #  we perform bitwise and operation here
    # resulting_img = cv2.bitwise_and(img, img, mask=mask)

    # detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
    contours, _ = cv2.findContours(image=mask, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
    # cv2.drawContours(image=certif, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
    # lineType=cv2.LINE_AA)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < 50:
            continue
        cv2.rectangle(certif, (x, y), (x + w, y + h), (150, 150, 150), 2)
        text, _ = text_contour(x, y, w, h, col=0, scale=1, text = name)

        cv2.rectangle(certif, (text[0], text[1]), (text[2], text[3]), (255, 255, 0), 2)
        diff = width
        counter = 0
        sc = 1.05
        while abs(diff) > 10:
            sc -= 0.05
            x, y, w, h, diff = center_test(x, y, w, h, col=120, scale=sc, text_in = name)
            print(sc)
        text, text_img = text_contour(x, y, w, h, col=255, scale=1, text = name)
        cv2.rectangle(certif, (text[0], text[1]), (text[2], text[3]), (150, 255, 150), 2)
        cv2.rectangle(text_img, (text[0], text[1]), (text[2], text[3]), (150, 255, 150), 2)
        text_img = text_img[text[1] + 5:text[3] - 5, text[0] + 5:text[2] - 5]
        finder = cv2.cvtColor(text_img, cv2.COLOR_BGR2GRAY)
        ctrs, _ = cv2.findContours(image=finder, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        r, c = 0, 0
        for row in text_img:
            c = 0
            for pnt in row:
                if sum(pnt) != 255 * 3:
                    certificate[text[1] + 5 + r, text[0] + 5 + c] = pnt
                c += 1
            r += 1

    # cv2.imshow(name, certificate)
    # cv2.imshow(name+"_test", certif)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return certificate