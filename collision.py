import PySimpleGUI as sg
from geo_objects import CollisionTri

dumpUnknownBlock = False
collisionTri = []

def getCollisionTris(fileName, window:sg.Window):
    with open(fileName, "rb") as file:
        file.seek(0x1c, 0)
        collisionOffset = int.from_bytes(file.read(4),"big")
        if(collisionOffset == 0):
            print("This file has no collisions!")
            return
        file.seek(collisionOffset,0)
        file.seek(16, 1)

        #count the unknown block so I can skip it
        unknownCount = int.from_bytes(file.read(2),"big")
        unknownSize = unknownCount * 4
        file.seek(2, 1)

        triCount = int.from_bytes(file.read(2),"big")
        window["-PROGRESS-"].update(0, triCount)
        file.seek(2,1)

        #this will be used to parse the unknown block once I know what it does
        if dumpUnknownBlock:
            unknownEntry = []
            unknownOffset = []
            unkDump = []
            unkString = None
            count = 0
            for unk in range(unknownCount + 1):
                unknownEntry.append(hex(int.from_bytes(file.read(2), "big")))
                unknownOffset.append(int.from_bytes(file.read(2), "big"))
                if unknownOffset[unk] == 0:
                    count += 1
                    if count > 1:
                        unkString = "({}, {}) x {}".format(unknownEntry[unk], unknownOffset[unk], count)
                    else:
                        if unkString:
                            unkDump.append(unkString)
                            unkString = " {}, {}".format(unknownEntry[unk], unknownOffset[unk])
                else:
                    count = 0
                    unkDump.append(unkString)
                    unkString = " {}, {}".format(unknownEntry[unk], unknownOffset[unk])
            for unk in range(len(unkDump)):
                print("{}".format(unkDump[unk]))
        else:
            file.seek(unknownSize, 1)

        #store each collision tri as an instance of Tri object
        for tri in range(triCount):
            BufferA = int.from_bytes(file.read(2),"big")
            BufferB = int.from_bytes(file.read(2),"big")
            BufferC = int.from_bytes(file.read(2),"big")
            unk8 = int.from_bytes(file.read(2), "big")
            FlagBuffer = int.from_bytes(file.read(4),"big")
            collisionTri.append(CollisionTri(BufferA, BufferB, BufferC, FlagBuffer, unk8))
            if tri % (int(triCount / 5)) == 0:
                window["-PROGRESS-"].update(tri)
                window["-COUNT-"].update("{}/{} tris".format(tri, triCount))