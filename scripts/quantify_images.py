# pixels_per_metric = tamanho objeto em px / tamanho real
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
 
def obj_mindpoint(ptA, ptB):
	return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path da imagem de input")
ap.add_argument("-w", "--width", type=float, required=True, help="largura real da folha (em centimetros)")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

#Filtros para detectar bordas (Canny, dilatação e erosão)
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)
 
# Econtra os contornos
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# Organiza os contornos da esquerda pra direita
(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None

# Percorre os pontos vendo se possuem um contorno valido (<100)
for single_cnts in cnts:
	if cv2.contourArea(single_cnts) < 100:
		continue

	# Calcula as bounding box dos contornos, rotaciona e desenha esboço com os pontos
	orig = img.copy()
	box = cv2.minAreaRect(single_cnts)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")

	box = perspective.order_points(box)
	cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)
	for (x, y) in box:
		cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

	# Encontra os centros dos bounding box e desenha o centro do objeto
	(tl, tr, br, bl) = box
	(tltrX, tltrY) = obj_mindpoint(tl, tr)
	(blbrX, blbrY) = obj_mindpoint(bl, br)
	(tlblX, tlblY) = obj_mindpoint(tl, bl)
	(trbrX, trbrY) = obj_mindpoint(tr, br)
	cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
	cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

	# Encontra a distancia euclidiana entre os centros e a medida real
	dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
	dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))
	if pixelsPerMetric is None:
		pixelsPerMetric = dB / args["width"]

	realA = dA / pixelsPerMetric
	realB = dB / pixelsPerMetric
	area = realA * realB
 
	# Escreve os textos e exibe as imagens
	cv2.putText(orig, "{:.1f}cm".format(realB), (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
	cv2.putText(orig, "{:.1f}cm".format(realA), (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
	cv2.putText(orig, "Area: {:.1f}".format(area), (int(blbrX), int(blbrY + 20)), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

	resized = imutils.resize(orig, width=450)
	resized2 = imutils.resize(edged, width=450)
	cv2.imshow("Contorno", resized2)
	cv2.imshow("Image", resized)
	cv2.waitKey(0)

cv2.destroyAllWindows()