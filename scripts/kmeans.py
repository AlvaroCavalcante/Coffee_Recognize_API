import cv2
import numpy as np
import utils as ut
import operator
from matplotlib import pyplot as plt
from functools import reduce
from sklearn.cluster import KMeans
import os

ut.convert_file()

img = cv2.imread('/home/alvaro/Desktop/Coffe_Recognize_API/img_hsv/fitossanidade.png')
rect = (430, 196, 800, 310)
clusters = 5

plt.imshow(img)
plt.show()

bar, porcentagens = ut.toKmeans(ut.black_back(img, rect), clusters)
contaminacao = (porcentagens[-1]*100)/reduce(operator.add, porcentagens)

folha_doenca = round(reduce(operator.add, porcentagens), 2)
contaminacao = round(contaminacao, 2)

#return img, bar, folha_doenca, contaminacao