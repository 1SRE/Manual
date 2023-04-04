"""
The following code executes a couple functions to combine everything found in the repository into a single JSON file for the website to read from.
"""

import os
import json

def getFolders(dir):
    return [f.path for f in os.scandir(dir) if f.is_dir() and f.path != "../.git" and f.path != "../pipeline" and f.path != "../.github"]

def getFiles(dir):
    return [f.path for f in os.scandir(dir) if f.is_file()]

def createSubContent(currDir, dirPath, jsonPointer):
    subFolders = getFolders(dirPath)
    
    for folder in subFolders:

        jsonPointer.append({"type": "folder", "title": folder.split(currDir+"/")[1], "content": list()})
        newJSONPointer = jsonPointer[len(jsonPointer)-1]["content"]
        createSubContent(folder, folder, newJSONPointer)

    subFiles = getFiles(dirPath)
    for subFile in subFiles:
        with open(subFile, "r") as text:
            jsonPointer.append({"type": "article", "title": subFile.split(currDir+"/")[1].split(".md")[0], "text": text.read()})
    
jsonObject = list()

for folder in getFolders("../"):
    jsonObject.append({"type": "folder", "title": folder.split("/")[1], "content": list()})
    
    currJSONPointer = jsonObject[len(jsonObject)-1]["content"]
    createSubContent(folder.split("/")[1], folder, currJSONPointer)

print("Done")

with open("manual.json", "w") as outFile:
    json.dump(jsonObject, outFile)