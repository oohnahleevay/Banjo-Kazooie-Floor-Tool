import math
import numpy as np
from PIL import Image as im

texture = []
colorFormat = {
    1:"CI4",
    2:"CI8",
    4:"RGBA5551",
    8:"RGBA8888",
    16: "IA8"
}

#TODO: Move class defs to their own file
class Texture():
    def __init__(self, Offset, nextOffset, Type, X, Y):
        self.Offset = Offset
        self.nextOffset = nextOffset
        self.type = colorFormat[Type]
        if (self.type == "IA8"):
            self.colorbytes = 1
        else:
            self.colorBytes = Type/2
        self.x_dim = X
        self.y_dim = Y

class Pixel():
    def __init__(self, positionAbs, positionX, positionY, R, G, B, A):
        self.positionAbs = positionAbs
        self.positionX = positionX
        self.positionY = positionY
        self.red = R
        self.green = G
        self.blue = B
        self.alpha = A

#This lives here now
def isModelFile(file):
    isModelFile = int.from_bytes(file.read(4), "big")
    if (isModelFile != 0xB):
        print("Not a model file!")
        return False

#Gets 5-bit color and shifts it into 8-bit color
def getRGBA(RGBA, splitRGBA):
    splitRGBA[0] = (RGBA & 0xF800) / 0x100
    splitRGBA[1] = (RGBA & 0x7C0) / 0x8
    splitRGBA[2] = (RGBA & 0x3E) * 0x4
    splitRGBA[3] = (RGBA & 0x1) * 0xFF
    return splitRGBA

#this is a monster
#TODO: Comment this
def getTextureInfo(fileName):
    with open(fileName, "rb") as file:
        if (isModelFile(file) == "False"):
            return
        file.seek(0x8, 0)
        textureSetupOffset = int.from_bytes(file.read(2), "big")
        if (textureSetupOffset == 0):
            print("This model has no textures!")
            return
        file.seek(textureSetupOffset,0)
        maxBytes = int.from_bytes(file.read(4), "big")
        textureCount = int.from_bytes(file.read(2), "big")
        file.seek(2, 1)
        for tex in range(textureCount):
            BufferOffset = int.from_bytes(file.read(4),"big")
            BufferType = int.from_bytes(file.read(2),"big")
            file.seek(2,1)
            BufferX = int.from_bytes(file.read(1),"big")
            BufferY = int.from_bytes(file.read(1),"big")
            file.seek(6,1)
            if (tex + 1 == textureCount):
                BufferNextOffset = maxBytes - (textureCount * 0x10 + 8)
            else:
                BufferNextOffset = int.from_bytes(file.read(4),"big")
                file.seek(-4, 1)
            texture.append(Texture(BufferOffset, BufferNextOffset, BufferType, BufferX, BufferY))
        for tx in texture:
            tx.pixel = []
            length = tx.nextOffset - tx.Offset
            print(tx.type)
            if (tx.type == "CI4"):
                tx.pixelCount = (length - 32) / tx.colorBytes
                tx.palette = []
                for color in range(16):
                    tx.palette.append(int.from_bytes(file.read(2),"big"))
            elif (tx.type == "CI8"):
                tx.pixelCount = length - 512
                tx.palette = []
                for color in range(256):
                    tx.palette.append(int.from_bytes(file.read(2),"big"))
            elif (tx.type == "IA8"):
                tx.pixelCount = length
            else:
                tx.pixelCount = length / tx.colorBytes
            for pix in range(int(tx.pixelCount)):
                BufferPosY = int(math.trunc(pix / tx.x_dim))
                BufferPosX = int(math.fmod(pix, tx.x_dim))
                splitRGBA = [0,0,0,0]
                if (tx.type == "CI4"):
                    readByte = int(math.fmod(pix, 2))
                    if (readByte == 0):
                        byte = int.from_bytes(file.read(1),"big")
                    nibble = [0,0]
                    nibble[0] = int((byte & 0xF0) / 0x10)
                    nibble[1] = byte & 0xF
                    RGBA = tx.palette[nibble[readByte]]
                    getRGBA(RGBA, splitRGBA)
                elif (tx.type == "CI8"):
                    index = int.from_bytes(file.read(1),"big")
                    RGBA = tx.palette[index]
                    getRGBA(RGBA, splitRGBA)
                elif (tx.type == "RGBA5551"):
                    RGBA = int.from_bytes(file.read(2),"big")
                    getRGBA(RGBA, splitRGBA)
                elif (tx.type == "RGB8888"):
                    splitRGBA[0] = int.from_bytes(file.read(1), "big")
                    splitRGBA[1] = int.from_bytes(file.read(1), "big")
                    splitRGBA[2] = int.from_bytes(file.read(1), "big")
                    splitRGBA[3] = int.from_bytes(file.read(1), "big")
                elif (tx.type == "IA8"):
                    byte = int.from_bytes(file.read(1), "big")
                    nibble = [0, 0]
                    nibble[0] = int((byte & 0xF0) / 10)
                    nibble[1] = byte & 0xF
                    Intensity = (nibble[0] * 0xFF) / 0xF
                    Alpha = (nibble[1] * 0xFF) / 0xF
                    splitRGBA = [Intensity, Intensity, Intensity, Alpha]
                tx.pixel.append(Pixel(pix, BufferPosX, BufferPosY, splitRGBA[0], splitRGBA[1], splitRGBA[2], splitRGBA[3]))

def drawTexture(ID):
    try:
        ID = int(ID)
    except ValueError:
        print("Give me a number.")
        return
    texArray = np.zeros((texture[ID].y_dim, texture[ID].x_dim, 4), 'uint8')
    for pix in texture[ID].pixel:
        if pix.positionY < texture[ID].y_dim:
            texArray[pix.positionY, pix.positionX] = [pix.red, pix.green, pix.blue, pix.alpha]
    showTexture = im.fromarray(texArray, mode="RGBA")
    showTexture.save("./textureOut/Texture{}.png".format(ID))
    return