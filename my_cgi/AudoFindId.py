#!/usr/bin/python
# coding=utf-8
__author__ = 'wangxiunian'
#
# 用于android layout findviewbyID
#
from xml.dom import minidom, Node
import os

l = []


def scan_files(directory, prefix=None, postfix=None):
    files_list = []
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root, special_file))
            elif prefix:
                if special_file.startswith(prefix):
                    files_list.append(os.path.join(root, special_file))
            else:
                files_list.append(os.path.join(root, special_file))

    return files_list


def add_list(name, id):
    l.append([name, id])


def scanner(doc):
    for child in doc.childNodes:
        if child.nodeType == Node.ELEMENT_NODE:
            elementId = child.getAttribute("android:id")
            tagName = child.tagName
            if elementId.strip():
                add_list(tagName, elementId)
            scanner(child)


def dealId(posId):
    idSplit = posId.split("/");
    realId = idSplit[0] if len(idSplit) <= 1 else idSplit[1]
    realIdSplit = realId.split("_")
    for i in range(0, len(realIdSplit)):
        realIdSplit[i] = realIdSplit[i].capitalize()

    resultStr = "m"
    for i in range(1, len(realIdSplit)):
        resultStr = resultStr + realIdSplit[i]

    resultStr = resultStr + realIdSplit[0]
    return resultStr, realId


files = scan_files("../", None, ".xml")
for inputPath in files:
    del l[:]
    isActivity = os.path.split(inputPath)[-1].startswith("activity_")
    outputPath = inputPath.replace(inputPath.split(".")[-1], "") + "txt"
    file_output = open(outputPath, "w")

    doc = minidom.parse(inputPath)
    scanner(doc)
    for element in l:
        result = dealId(element[1])
        element[0] = element[0].split(".")[-1]
        element[1] = result[1]
        element.append(result[0])
    print(l)
    print("---------------------------------------")
    for item in l:
        out = "private " + item[0] + " " + item[2] + ";"
        print(out)
        file_output.write(out + "\n")
    print()
    if isActivity:
        file_output.write(
            "\n----------------copy following text,you should  give the rootView of Fragment-----------------------\n\n")
    else:
        file_output.write("\n----------------copy following text to your code-----------------------\n\n")
    for item in l:
        if isActivity:
            out = item[2] + " = (" + item[0] + ")findViewById(R.id." + item[1] + ");"
        else:
            out = item[2] + " = (" + item[0] + ")rootView.findViewById(R.id." + item[1] + ");"
        print(out)
        file_output.write(out + "\n")

    file_output.write("----------------final InjectView -----------------------\n\n")
    for item in l:
        out = "@ViewInject(id = " + item[1] + ")\nprivate " + item[0] + " " + item[2] + ";"
        print(out)
        file_output.write(out + "\n")
    print()
    file_output.close()