import xml.etree.cElementTree as ET
from random import randrange
import os

class GenerateXml(object):
    def __init__(self, box_array, im_width, im_height):
        self.box_array = box_array
        self.im_width = im_width
        self.im_height = im_height

    def get_file_number(self, name_file):
        file = list(name_file)
        number = file[(file.index('.') - 1)]
        return number

    def get_file_name(self):
        upload_path = '/home/alvaro/Desktop/Coffe_Recognize_API/xml'
        directory = os.path.basename(upload_path)
        file_list = os.listdir(directory)
        if file_list == []:
            return 1
        else:
            last_file = file_list[(len(file_list) - 1)]
            number_file = self.get_file_number(last_file)
            return int(number_file) + 1

    def gerenate_basic_structure(self):
        file_name = "name" + str(self.get_file_name()) + ".xml"
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "filename").text = file_name
        size = ET.SubElement(annotation, "size")
        ET.SubElement(size, "width").text = str(self.im_width)
        ET.SubElement(size, "height").text = str(self.im_height)
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
        arquivo.write("/home/alvaro/Desktop/Coffe_Recognize_API/xml/" + file_name)

def main():
    xml = GenerateXml([{'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}, {'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}, {'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}, {'xmin': 0.5406094193458557, 'xmax': 0.6001364588737488, 'ymin': 0.6876631379127502, 'ymax': 0.7547240853309631}], '4000', '2000')
    xml.gerenate_basic_structure()    

main()