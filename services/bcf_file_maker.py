import zipfile
import xml.etree.ElementTree as ET
from models.bcf_model import Markup, ViewPoint, BCFZipCreate
import os

def createMarkupFile(markup: Markup):
    markup = ET.Element("Markup", xmlns="http://www.buildingsmart-tech.org/bcf/markup/1.0")
    topic = ET.SubElement(markup, "Topic", Guid=markup.Guid)
    ET.SubElement(topic, "Title").text = markup.Title
    ET.SubElement(topic, "Priority").text = markup.Priority
    ET.SubElement(topic, "Status").text = markup.Status
    ET.SubElement(topic, "CreationDate").text = markup.CreationDate
    ET.SubElement(topic, "CreationAuthor").text = markup.CreationAuthor
    ET.SubElement(topic, "ModifiedDate").text = markup.ModifiedDate
    ET.SubElement(topic, "ModifiedAuthor").text = markup.ModifiedAuthor
    ET.SubElement(topic, "AssignTo").text = markup.AssignedTo
    ET.SubElement(topic, "Priority").text = markup.Description
    tree = ET.ElementTree(markup)
    folder_name = markup.Filename + "/" + "issue_" + markup.Guid
    os.makedirs(folder_name, exist_ok=True)
    tree.write(folder_name + "/markup.bcf", encoding="utf-8", xml_declaration=True)

def createViewpoinFile(viewpoint: ViewPoint) :
    rootViewpoint = ET.Element("Viewpoint", xmlns="http://www.buildingsmart-tech.org/bcf/markup/1.0")
    cameraViewpoint = ET.SubElement(rootViewpoint, "CameraViewPoint")
    cameraDirection = ET.SubElement(cameraViewpoint, "CameraDirection")
    ET.SubElement(cameraDirection, "X").text = viewpoint.CameraDirection_X
    ET.SubElement(cameraDirection, "Y").text = viewpoint.CameraDirection_Y
    ET.SubElement(cameraDirection, "Z").text = viewpoint.CameraDirection_Z
    cameraUpVector = ET.SubElement(cameraViewpoint, "CameraUpVector")
    ET.SubElement(cameraUpVector, "X").text = viewpoint.CameraUp_X
    ET.SubElement(cameraUpVector, "Y").text = viewpoint.CameraUp_Y
    ET.SubElement(cameraUpVector, "Z").text = viewpoint.CameraUp_Z
    cameraPosition = ET.SubElement(cameraViewpoint, "CameraPosition")
    ET.SubElement(cameraPosition, "X").text = viewpoint.CameraPosition_X
    ET.SubElement(cameraPosition, "Y").text = viewpoint.CameraPosition_Y
    ET.SubElement(cameraPosition, "Z").text = viewpoint.CameraPosition_Z
    tree = ET.ElementTree(rootViewpoint)
    folder_name = viewpoint.Filename + "/" + "issue_" + viewpoint.Guid
    os.makedirs(folder_name, exist_ok=True)
    tree.write(folder_name + "/viewpoint.bcfv", encoding="utf-8", xml_declaration=True)

def createBCFZipFile(bcffile: BCFZipCreate) :
    folder_name = bcffile.Filename + "/" + "issue_" + bcffile.Guid
    with zipfile.ZipFile("contoh.bcfzip", "w") as bcfzip:
        bcfzip.write("markup.bcf", arcname = folder_name + "/markup.bcf")
        bcfzip.write("viewpoint.bcfv", arcname = folder_name + "/viewpoint.bcfv")
        bcfzip.write(bcffile.FilePNGName, arcname = folder_name + "/snapshot.png")
        with open("bcf.version", "w") as f:
            f.write("2.1")
        bcfzip.write("bcf.version")