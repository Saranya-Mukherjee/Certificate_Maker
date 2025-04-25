import pandas as pd
import find_start
import cv2
import os

df = pd.read_csv('names.csv')
x = df.iloc[:].values

total = len(x)
no = 0
MAX_RECURSION_LIMIT = 50
SCALE_START = 1
STEP = 0.05 # adjust to get the needed speed or accuracy

for data in x:
    no += 1
    print("===================", no, "OUT OF", total, "===================")

    d = data[0]
    d = d.lower()
    d = d.title()
    print(d)

    certificate = find_start.do_the_fucking_ai_type_shit(d,SCALE_START, STEP, MAX_RECURSION_LIMIT)
    cv2.imwrite("results/"+d+".jpg",certificate)
