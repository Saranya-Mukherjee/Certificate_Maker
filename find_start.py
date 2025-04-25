import cv2
import numpy as np
import colours
import text_rec

img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
certif = cv2.imread("1st.png", cv2.IMREAD_COLOR)
# certif = cv2.resize(certif, (0, 0), fx=0.5, fy=0.5)
certificate = cv2.imread("1st.png", cv2.IMREAD_COLOR)
# certificate = cv2.resize(certificate, (0, 0), fx=0.5, fy=0.5)
# img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

height, width, _ = certif.shape
width_box = width
print('width:  ', width)
print('height: ', height)

def text_contour(x, y, w, h, col, scale, text):
    # centering the text in the rectangle
    blank = 255 * np.ones_like(certif, dtype=np.uint8)
    blank_cp = 255 * np.ones_like(certif, dtype=np.uint8)
    font = cv2.FONT_HERSHEY_TRIPLEX
    org = (x + w // 2, int(y + h / 1.2))
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
    text, _ = text_contour(x, y, w, h, col=col, scale=scale, text = text_in)
    x,y,w,h = x,y,w,h
    diff = width_box
    print("ok",width_box, width//2)
    counter = 0
    while abs(diff)>10:
        center_text = [(text[0] + text[2]) // 2, (text[1] + text[3]) // 2]
        diff = width_box - center_text[0]
        print(center_text, diff)
        x, y, w, h = x, y, w + diff * 2, h
        text, _ = text_contour(x, y, w, h, col = col, scale= scale, text = text_in)
        counter += 1
        if counter>10:
            break
    return x,y,w,h,diff

def do_all_the_fucking_work(name, scale_trial):
    global width_box
    SCALE = scale_trial
    img = cv2.imread("1st_ref.png", cv2.IMREAD_COLOR)
    certif = cv2.imread("1st.png", cv2.IMREAD_COLOR)
    # certif = cv2.resize(certif, (0, 0), fx=0.5, fy=0.5)
    certificate = cv2.imread("1st.png", cv2.IMREAD_COLOR)
    # certificate = cv2.resize(certificate, (0, 0), fx=0.5, fy=0.5)
    # img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
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
        width_box = x+w//2
        print("hu", x, w, width_box)
        cv2.rectangle(certif, (x, y), (x + w, y + h), (150, 150, 150), 2)
        text, _ = text_contour(x, y, w, h, col=0, scale=SCALE, text = name)

        cv2.rectangle(certif, (text[0], text[1]), (text[2], text[3]), (255, 255, 0), 2)
        diff = width
        counter = 0
        sc = SCALE
        # while abs(diff) > 10:
        #     sc -= 0.05
        #     x, y, w, h, diff = center_test(x, y, w, h, col=120, scale=sc, text_in=name)
        #     print(sc)
        x, y, w, h, diff = center_test(x, y, w, h, col=120, scale=sc, text_in=name)
        text, text_img = text_contour(x, y, w, h, col=255, scale=SCALE, text = name)
        # cv2.rectangle(certif, (text[0], text[1]), (text[2], text[3]), (255, 0, 0), 2)
        # cv2.rectangle(certif, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # cv2.rectangle(certif, (text[0], text[1]), (text[2], text[3]), (0, 0, 255), 2)
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
    # cv2.imshow(name, text_img)
    text_got = text_rec.get_text_from_img(certificate, text)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return certificate, text, text_got

def get_precent_match(base, to_cpr):
    l = len(base)
    l2 = len(to_cpr)
    if l == 0 or l2 == 0:
        return 0
    if 0.7 < l2/l < 1.3:
        pass
    else:
        return 0
    cnt = 0

    chk_len = None
    if l<l2:
        chk_len = l
    elif l>=l2:
        chk_len = l2
    for n in range(chk_len):
        if to_cpr[n] == base[n]:
            cnt += 1
    percent_of_match = (cnt/l)*100
    print("precent", percent_of_match)
    return percent_of_match

def do_the_fucking_ai_type_shit(name, scale_start, step, max_limit):
    scale = scale_start
    step = step
    dir = 1 # 1 for increase, -1 for decrease

    certificate_last = None
    flipped = False

    while True:
        print("SCALE", scale)
        try:
            certificate, _, text_got = do_all_the_fucking_work(name, scale)
        except:
            scale += dir * step
            continue
        certificate_last = certificate
        if get_precent_match(text_got, name)>=50:
            if dir == 1:
                while True:
                    print("SCALE", scale)
                    try:
                        certificate, _, text_got = do_all_the_fucking_work(name, scale)
                    except:
                        scale += dir * step
                        continue
                    if get_precent_match(text_got, name)>70:
                        scale += dir * step
                        certificate_last = certificate
                    else:
                        break
            break
        elif scale > 0.2 and not flipped:
            dir = -1
        else:
            dir = 1
            flipped = True
        scale += dir * step
    print("SCALE FINAL", scale)
    return certificate_last