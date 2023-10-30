from geo_objects import *
from struct import *

noCollisionTri = []

GL_Commands = {
    0x1: "SORT",
    0x2: "BONE",
    0x3: "LOAD DL",
    0x5: "SKINNING",
    0x6: "BRANCH",
    0x8: "LOD",
    0xA: "REFERENCE POINT",
    0xC: "SELECTOR",
    0xD: "DRAW DISTANCE",
    0xF: "UNKNOWN 0xF",
    0x10: "UNKNOWN 0x10"
}

#TODO: Add processing info for other gl commands
def getGeometryLayouts(fileName):
    with open (fileName, "rb") as file:
        file.seek(4)
        geometryLayoutOffset = int.from_bytes(file.read(4), "big")
        file.seek(geometryLayoutOffset, 0)
        glIsLOD = False
        nextCommand = True
        while nextCommand:
            commandOffset = hex(file.tell())
            commandType = GL_Commands[int.from_bytes(file.read(4), "big")]
            if commandType == "SORT":
                length = int.from_bytes(file.read(4), "big")
                (childOneX, childOneY, childOneZ,
                 childTwoX, childTwoY, childTwoZ) = unpack(">6f", file.read(24))
                childOne = [childOneX, childOneY, childOneZ]
                childTwo = [childTwoX, childTwoY, childTwoZ]
                drawNearerOnly = bool(int.from_bytes(file.read(2), "big") & 1)
                childOneOffset = int.from_bytes(file.read(2), "big")
                childTwoOffset = int.from_bytes(file.read(4), "big")
                #print(commandOffset, commandType, length, childOne, childTwo, drawNearerOnly, childOneOffset, childTwoOffset)
            elif commandType == "LOAD DL":
                length = int.from_bytes(file.read(4), "big")
                commandIndex = int.from_bytes(file.read(2), "big")
                triCount = int.from_bytes(file.read(2), "big")
                pad = file.read(4)
                check_for_end = int.from_bytes(file.read(4), "big")

                if not pad or check_for_end == 0:
                    nextCommand = False

                if glIsLOD:
                    setTriAsLOD(commandIndex, file)
                    glIsLOD = False
                file.seek(-4, 1)
                #print(commandOffset, commandType, length, hex(commandIndex), hex(triCount))
            elif commandType == "LOD":
                length = int.from_bytes(file.read(4), "big")
                (maxDistance, minDistance, testX, testY, testZ) = unpack(">5f", file.read(20))
                distRange = [minDistance, maxDistance]
                testCoords = [testX, testY, testZ]
                glOffset = int.from_bytes(file.read(4), "big")

                if minDistance > 0.0:
                    glIsLOD = True

                #print(commandOffset, commandType, length, distRange, testCoords, hex(glOffset))
            elif commandType == "DRAW DISTANCE":
                length = int.from_bytes(file.read(4), "big")
                negativeDrawX = int.from_bytes(file.read(2), "big", signed=True)
                negativeDrawY = int.from_bytes(file.read(2), "big", signed=True)
                negativeDrawZ = int.from_bytes(file.read(2), "big", signed=True)
                negativeDraw = [negativeDrawX, negativeDrawY, negativeDrawZ]
                positiveDrawX = int.from_bytes(file.read(2), "big", signed=True)
                positiveDrawY = int.from_bytes(file.read(2), "big", signed=True)
                positiveDrawZ = int.from_bytes(file.read(2), "big", signed=True)
                positiveDraw = [positiveDrawX, positiveDrawY, positiveDrawZ]
                unk20 = hex(int.from_bytes(file.read(4), "big"))
                #print(commandOffset, commandType, length, negativeDraw, positiveDraw, unk20)
            elif commandType == "UNKNOWN 0xF":
                length = int.from_bytes(file.read(4), "big")
                headerLength = int.from_bytes(file.read(2), "big")
                unkCount = int.from_bytes(file.read(1), "big")
                unkB = int.from_bytes(file.read(1), "big")
                unkList = []
                for unk in range(unkCount):
                    unkList.append(int.from_bytes(file.read(1),"big"))
                endOfHeader = (headerLength - 12) - (unkCount)
                file.seek(endOfHeader, 1)
                #print(commandOffset, commandType, length, headerLength, unkCount, unkB, unkList)
            elif commandType == "UNKNOWN 0x10":
                length = int.from_bytes(file.read(4), "big")
                unkC = int.from_bytes(file.read(4), "big")
                file.seek(4, 1)
                #print(commandOffset, commandType, length, unkC)
def setTriAsLOD(command, file):
    returnAddress = file.tell()
    file.seek(0xC, 0)
    displayBlockOffset = int.from_bytes(file.read(4), "big")
    displayListOffset = displayBlockOffset + (command + 1) * 8
    file.seek(displayListOffset, 0)
    readDisplayList = True
    while readDisplayList:
        commandID = int.from_bytes(file.read(1), "big")
        if commandID == (0xB1 or 0xBF):
            noCollisionTri.append(command)
        if commandID == (0xB8):
            readDisplayList = False
        file.seek(7, 1)
        command += 1
    file.seek(returnAddress, 0)
    return
