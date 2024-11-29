from struct import *
from geo_objects import *

noCollisionTri = []
bones = []

GL_Commands = {
    0x0: "UNKNOWN 0x0",
    0x1: "SORT",
    0x2: "BONE",
    0x3: "LOAD DL",
    0x4: "BLANK ENTRY",
    0x5: "SKINNING",
    0x6: "BRANCH",
    0x7: "UNKNOWN 0x7",
    0x8: "LOD",
    0x9: "BLANK ENTRY",
    0xA: "REFERENCE POINT",
    0xB: "BLANK ENTRY",
    0xC: "SELECTOR",
    0xD: "DRAW DISTANCE",
    0xE: "UNKNOWN 0xE",
    0xF: "UNKNOWN 0xF",
    0x10: "UNKNOWN 0x10"
}

mipMapDLType = {
    1: "Clamp",
    2: "Wrap"
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

        # command 0x0: UNKNOWN
            if commandType == "UNKNOWN 0x0":
                print("This is command type 0. We didn't know about it until literally now.")
                break

        # command 0x1: SORT
            elif commandType == "SORT":
                length = int.from_bytes(file.read(4), "big")
                (childOneX, childOneY, childOneZ,
                 childTwoX, childTwoY, childTwoZ) = unpack(">6f", file.read(24))
                childOne = [childOneX, childOneY, childOneZ]
                childTwo = [childTwoX, childTwoY, childTwoZ]
                drawNearerOnly = bool(int.from_bytes(file.read(2), "big") & 1)
                childOneOffset = int.from_bytes(file.read(2), "big")
                childTwoOffset = int.from_bytes(file.read(4), "big")

                print(commandOffset, commandType, length, childOne, childTwo, drawNearerOnly, childOneOffset, childTwoOffset)

        # command 0x2: BONE
            elif commandType == "BONE":
                commandIndex = int.from_bytes(file.read(4), "big")
                length = int.from_bytes(file.read(1), "big")
                boneID = int.from_bytes(file.read(1), "big")
                unkA = int.from_bytes(file.read(2), "big")

                if length == 0x10:
                    pad = file.read(4)
                bones.append(Bone(boneID, commandIndex, unkA))
                print(commandOffset, commandType, hex(commandIndex), length, boneID, hex(unkA), pad if pad else None)

        # command 0x3: LOAD DL
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
                print(commandOffset, commandType, length, hex(commandIndex), hex(triCount))

        # command 0x4: BLANK ENTRY

        # command 0x5: SKINNING
            elif commandType == "SKINNING":
                length = int.from_bytes(file.read(4), "big")
                commandIndex = int.from_bytes(file.read(2), "big")
                bone_dl = []
                next_dl = int.from_bytes(file.read(2), "big")
                odd = True
                while next_dl != 0:
                    odd = not odd
                    bone_dl.append(next_dl)
                    next_dl = int.from_bytes(file.read(2), "big")
                if not odd:
                    file.seek(-2, 1)
                check_for_padding = True
                count = 0
                while check_for_padding:
                    pad = int.from_bytes(file.read(4), "big")
                    count += 1
                    if pad == 0 and count > 3:
                        nextCommand = False
                        break
                    if pad != 0:
                        file.seek(-4, 1)
                        break
                print(commandOffset, commandType, length, commandIndex, bone_dl)

        # command 0x6: BRANCH
            elif commandType == "SORT":
                print("Command type 6. Dunno how to parse this yet.")
                break

        # command 0x7: UNKNOWN
            elif commandType == "UNKNOWN 0x7":
                print("7?! WAS THAT 7?!")
                break

        # command 0x8: LOD
            elif commandType == "LOD":
                length = int.from_bytes(file.read(4), "big")
                (maxDistance, minDistance, testX, testY, testZ) = unpack(">5f", file.read(20))
                distRange = [minDistance, maxDistance]
                testCoords = [testX, testY, testZ]
                glOffset = int.from_bytes(file.read(4), "big")

                if minDistance > 0.0:
                    glIsLOD = True

                print(commandOffset, commandType, length, distRange, testCoords, hex(glOffset))

        # command 0x9: BLANK ENTRY

        # command 0xA: REFERENCE POINT
            elif commandType == "REFERENCE POINT":
                length = int.from_bytes(file.read(4), "big")
                referencePointIndex = int.from_bytes(file.read(2), "big")
                boneIndex = int.from_bytes(file.read(2), "big")
                boneOffset = unpack(">3f", file.read(12))
                check_for_end = int.from_bytes(file.read(8), "big")
                print(check_for_end)
                if check_for_end == 0:
                    nextCommand = False

                file.seek(-8, 1)

                print(commandOffset, commandType, length, referencePointIndex, boneIndex, boneOffset)

        # command 0xB: BLANK ENTRY
            elif commandType == "BLANK ENTRY":
                print("This entry should be blank.")
                break

        # command 0xC: SELECTOR
            elif commandType == "SELECTOR":
                length = int.from_bytes(file.read(4), "big")
                childCount = int.from_bytes(file.read(2), "big")
                selectorIndex = int.from_bytes(file.read(2), "big")
                children = []
                for child in range(childCount):
                    children.append(int.from_bytes(file.read(4), "big"))
                if int.from_bytes(file.read(4), "big") != 0:
                    file.seek(-4, 1)

                print(commandOffset, commandType, length, childCount, selectorIndex, children)

        # command 0xD: DRAW DISTANCE
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
                print(commandOffset, commandType, length, negativeDraw, positiveDraw, unk20)

        # command 0xE: UNKNOWN
            elif commandType == "UNKNOWN 0xE":
                print("What the heck? E?")
                break

        # command 0xF: UNKNOWN
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
                print(commandOffset, commandType, length, headerLength, unkCount, unkB, unkList)

        # command 0x10: UNKNOWN
            elif commandType == "UNKNOWN 0x10":
                length = int.from_bytes(file.read(4), "big")
                unk8 = int.from_bytes(file.read(4), "big")
                file.seek(4, 1)
                print(commandOffset, commandType, length, mipMapDLType[unk8])
        print("Complete")


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
