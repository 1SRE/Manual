"""
The following code executes a couple functions to combine everything found in the repository into a single JSON file for the website to read from.
"""

import os
import json

def getFolders(dir):
    return [f.path for f in os.scandir(dir) if f.is_dir() and f.path != "../.git" and f.path != "../1SRE\Scripts"]

def getFiles(dir):
    return [f.path for f in os.scandir(dir) if f.is_file()]

def createSubContent(currDir, dirPath, jsonPointer):
    subFolders = getFolders(dirPath)
    print(f"The subFolders of {currDir} include: {subFolders}")
    
    for folder in subFolders:
        jsonPointer[folder.split(currDir+"/")[1]] = dict()
        newJSONPointer = jsonPointer[folder.split(currDir+"/")[1]]
        createSubContent(folder, folder, newJSONPointer)

    subFiles = getFiles(dirPath)
    print(f"The subFiles of {currDir} include: {subFiles}")
    for subFile in subFiles:
        with open(subFile, "r") as text:
            jsonPointer[subFile.split(currDir+"/")[1]] = text.read()
    
jsonObject = dict()

for folder in getFolders("../"):
    jsonObject[folder.split("/")[1]] = dict()
    currJSONPointer = jsonObject[folder.split("/")[1]]
    createSubContent(folder.split("/")[1], folder, currJSONPointer)

print("Done")

with open("manual.json", "w") as outFile:
    json.dump(jsonObject, outFile)