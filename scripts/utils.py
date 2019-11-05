import cv2
import numpy as np
from matplotlib import pyplot as plt
from functools import reduce
import operator
import collections
import os
from sklearn.cluster import KMeans

def resize(img, scale_percent=50):
    width = int(img.shape[1] * (scale_percent / 100))
    height = int(img.shape[0] * (scale_percent / 100))
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized


def toHSV(img):
    hsv = 0
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    H, S, V = cv2.split(img)
    return V


def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)
    hist = hist.astype("float")
    hist /= hist.sum()
    return hist


def plot_colors(hist, centroids):
    hist, centroids = organizarCorArray(hist, centroids)
    porcentagens = []
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0
    for (percent, color) in zip(hist, centroids):
        if color != [0, 0, 0]:
            porcentagens.append(round(percent*100, 2))
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color, -1)
        startX = endX
    return bar, porcentagens


def convert_file():
    upload_path = '/home/alvaro/Desktop/Coffe_Recognize_API/uploads'
    directory = os.path.basename(upload_path)
    img = os.listdir(directory)

    img = cv2.imread(upload_path + '/' + img[0])
    img = resize(img, 32)
    img = toHSV(img)
    cv2.imwrite('/home/alvaro/Desktop/Coffe_Recognize_API/img_hsv/fitossanidade.png', img)


def toKmeans(img, clusters):
    img = img.reshape((img.shape[0] * img.shape[1], 3))
    clt = KMeans(n_clusters=clusters)
    clt.fit(img)
    hist = centroid_histogram(clt)
    bar, porcentagens = plot_colors(hist, clt.cluster_centers_)
    return bar, porcentagens


def black_back(img, coord):
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    cv2.grabCut(img, mask, coord, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    output = img*mask2[:, :, np.newaxis]
    return output


def organizarCorArray(hist, centroids):
    aux = {}
    final_val = {}
    cores = []
    percents = []
    for (percent, color) in zip(hist, centroids):
        aux[reduce(operator.add, color.astype(
            "uint8").tolist())] = percent
        final_val[reduce(operator.add, color.astype(
            "uint8").tolist())] = color.astype("uint8").tolist()
    aux = collections.OrderedDict(sorted(aux.items()))
    for k, v in aux.items():
        cores.append(final_val[k])
        percents.append(v)
    return percents, cores
