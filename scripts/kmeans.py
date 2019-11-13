import cv2
import numpy as np
import utils as ut
import operator
from matplotlib import pyplot as plt
from functools import reduce
from sklearn.cluster import KMeans
import os

ut.convert_file()

img = cv2.imread('/home/alvaro/Área de Trabalho/Coffe_Recognize_API/img_hsv/fitossanidade.png')
rect = (188, 224, 382, 687)
clusters = 5

bar, porcentagens = ut.toKmeans(ut.black_back(img, rect), clusters)
contaminacao = (porcentagens[-1]*100)/reduce(operator.add, porcentagens)

folha_doenca = round(reduce(operator.add, porcentagens), 2)
contaminacao = round(contaminacao, 2)

print('leaf disease', folha_doenca, 'contamination', contaminacao)
#return img, bar, folha_doenca, contaminacao