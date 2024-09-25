import pandas as pd
import find_start
import cv2

df = pd.read_csv('names.csv')
x = df.iloc[:].values

for data in x:
    d = data[0]
    print(d)
    certificate = find_start.do_all_the_fucking_work(d)
    cv2.imwrite("results/"+d+".jpg",certificate)