import PySimpleGUI as sg
from geo_objects import *

vertex = []

def getVertices(fileName, window:sg.Window):
    with open(fileName, "rb") as file:
        file.seek(0x10)
        vertexSetupOffset = int.from_bytes(file.read(4), "big")
        file.seek(0x32, 0)
        vertexCount = int.from_bytes(file.read(2), "big")
        file.seek(vertexSetupOffset, 0)

        #get these values and keep them for later
        drawMinX = int.from_bytes(file.read(2), "big", signed = True)
        drawMinY = int.from_bytes(file.read(2), "big", signed = True)
        drawMinZ = int.from_bytes(file.read(2), "big", signed = True)
        drawMaxX = int.from_bytes(file.read(2), "big", signed = True)
        drawMaxY = int.from_bytes(file.read(2), "big", signed = True)
        drawMaxZ = int.from_bytes(file.read(2), "big", signed = True)
        minObjectRange = int.from_bytes(file.read(2), "big", signed = True)
        maxObjectRange = int.from_bytes(file.read(2), "big", signed = True)
        unk10 = int.from_bytes(file.read(2), "big", signed = True)
        unk12 = int.from_bytes(file.read(2), "big", signed = True)
        file.seek(2, 1)
        #vertexCount = int.from_bytes(file.read(2), "big")
        unk16 = int.from_bytes(file.read(2), "big", signed = True)
        #print((drawMinX, drawMinY, drawMinZ), (drawMaxX, drawMaxY, drawMaxZ), [minObjectRange, maxObjectRange], unk10, unk12, vertexCount, unk16)
        window["-PROGRESS-"].update(0, vertexCount)

        for vtx in range(vertexCount):
            BufferX = int.from_bytes(file.read(2), "big", signed = True)
            BufferY = int.from_bytes(file.read(2), "big", signed = True)
            BufferZ = int.from_bytes(file.read(2), "big", signed = True)
            file.seek(2,1)
            BufferU = int.from_bytes(file.read(2), "big", signed = True)
            BufferV = int.from_bytes(file.read(2), "big", signed = True)
            BufferR = int.from_bytes(file.read(1), "big", signed = True)
            BufferG = int.from_bytes(file.read(1), "big", signed = True)
            BufferB = int.from_bytes(file.read(1), "big", signed = True)
            BufferA = int.from_bytes(file.read(1), "big", signed = True)
            vertex.append(Vertex(BufferX, BufferY, BufferZ, BufferU, BufferV, BufferR, BufferG, BufferB, BufferA))
            if int(vertexCount / 10) >= 1:
                if vtx % (int(vertexCount / 10)) == 0:
                    window["-PROGRESS-"].update(vtx)
                    window["-COUNT-"].update("{}/{} vertices".format(vtx, vertexCount))