import xml.etree.cElementTree as ET
from random import randrange

class GenerateXml(object):
    def __init__(self, box_array):
        self.box_array = box_array

    def gerenate_basic_structure(self):
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "filename").text = "name10.jpg"
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = "4000"
        ET.SubElement(size, "height").text = "2250"
        ET.SubElement(size, "depth").text = "3"
        
        for i in self.box_array:
            objectBox = ET.SubElement(annotation, "object")
            ET.SubElement(objectBox, "name").text = "ferrugem"
            ET.SubElement(objectBox, "pose").text = "Unspecified"
            ET.SubElement(objectBox, "truncated").text = "0"
            ET.SubElement(objectBox, "difficult").text = "0"
            bndBox = ET.SubElement(objectBox, "bndbox")
            ET.SubElement(bndBox, "xmin").text = str(i['xmin'])
            ET.SubElement(bndBox, "ymin").text = str(i['ymin'])
            ET.SubElement(bndBox, "xmax").text = str(i['xmax'])
            ET.SubElement(bndBox, "ymax").text = str(i['ymax'])

        arquivo = ET.ElementTree(annotation)
        arquivo.write("folha" + str(randrange(10)) + ".xml")

def main():
    xml = GenerateXml([{'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}, {'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}, {'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}, {'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}])
    xml.gerenate_basic_structure()    