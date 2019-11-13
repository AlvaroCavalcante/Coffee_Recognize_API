import cv2
import numpy as np
import utils as ut
import operator
from matplotlib import pyplot as plt
from functools import reduce
from sklearn.cluster import KMeans
import os

ut.convert_file()

img = cv2.imread('/home/alvaro/Coffee_Recognize_API/img_hsv/fitossanidade.png')
rect = (188, 224, 382, 687)
clusters = 5

results = []

bar, porcentagens = ut.toKmeans(ut.black_back(img, rect), clusters)
contamination = (porcentagens[-1]*100)/reduce(operator.add, porcentagens)

leaf_disease = round(reduce(operator.add, porcentagens), 2)
contamination = round(contamination, 2)

results.append(leaf_disease)
results.append(contamination)
print(results)
