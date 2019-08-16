import xml.etree.cElementTree as ET

class GenerateXml(object):
    def __init__(self, left, right, top, bottom):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def gerenate_basic_structure(self):
        annotation = ET.Element("annotation")
        ET.SubElement(annotation, "folder").text = "resultados"
        ET.SubElement(annotation, "filename").text = "name10.jpg"
        ET.SubElement(annotation, "path").text = "/home/alvaro/Documentos/doenças/ferrugem/name10.jpg"
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
        ET.SubElement(bndBox, "xmin").text = str(self.left)
        ET.SubElement(bndBox, "ymax").text = str(self.right) 
        ET.SubElement(bndBox, "xmin").text = str(self.top)
        ET.SubElement(bndBox, "ymax").text = str(self.bottom)

        arquivo = ET.ElementTree(annotation)
        arquivo.write("meu_xml.xml")

def main():
    xml = GenerateXml(10, 20, 30, 40)
    xml.gerenate_basic_structure()    

main()