import xml.etree.cElementTree as ET
from random import randrange

class GenerateXml(object):
    def __init__(self, left, right, top, bottom):
        self.xmin = left
        self.xmax = right
        self.ymin = top
        self.ymax = bottom

    def gerenate_basic_structure(self):
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "filename").text = "name10.jpg"
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = "100"
        ET.SubElement(size, "height").text = "100"
        ET.SubElement(size, "depth").text = "100"

        objectBox = ET.SubElement(annotation, "object")
        ET.SubElement(objectBox, "name").text = "ferrugem"
        ET.SubElement(objectBox, "pose").text = "Unspecified"
        ET.SubElement(objectBox, "truncated").text = "0"
        ET.SubElement(objectBox, "difficult").text = "0"
        bndBox = ET.SubElement(objectBox, "bndbox")
        ET.SubElement(bndBox, "xmin").text = str(self.xmin)
        ET.SubElement(bndBox, "ymin").text = str(self.ymin) 
        ET.SubElement(bndBox, "xmax").text = str(self.xmax)
        ET.SubElement(bndBox, "ymax").text = str(self.ymax)

        arquivo = ET.ElementTree(annotation)
        arquivo.write("folha" + str(randrange(10)) + ".xml")

# def main():
#     xml = GenerateXml(10, 20, 30, 40)
#     xml.gerenate_basic_structure()    

# main()