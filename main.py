from colorHandler import getTextureInfo, isModelFile, texture, drawTexture

collisionTri = []
outputFileName = "output.txt" #lol

#TODO: Move class defs to separate file
class Tri():
    def __init__(self, VertexA, VertexB, VertexC, Flags):
        self.VertexA = VertexA
        self.VertexB = VertexB
        self.VertexC = VertexC
        self.Flags = []
        self.trueFlags = []

        #turn the bitfield into a list for ease of access
        for i in range(0x20):
            self.Flags.append(bool(Flags & (2 ** i) != 0))

        #might be useful later idk
        for index, flag in enumerate(self.Flags):
            if (flag == True):
                index = hex(index)
                self.trueFlags.append(index)

def getCollisionTris(fileName):
    with open(fileName, "rb") as file:
        if (isModelFile(file) == "False"):
            return
        file.seek(0x1c, 0)
        collisionOffset = int.from_bytes(file.read(4),"big")
        if(collisionOffset == 0):
            print("This file has no collisions!")
            return
        file.seek(collisionOffset,0)
        file.seek(16, 1)

        #count the unknown block so I can skip it
        unknownSize = int.from_bytes(file.read(2),"big") * 4
        file.seek(2, 1)

        triCount = int.from_bytes(file.read(2),"big")
        file.seek(2,1)
        file.seek(unknownSize,1)

        for tri in range(triCount):
            BufferA = int.from_bytes(file.read(2),"big")
            BufferB = int.from_bytes(file.read(2),"big")
            BufferC = int.from_bytes(file.read(2),"big")
            file.seek(2,1)
            FlagBuffer = int.from_bytes(file.read(4),"big")
            collisionTri.append(Tri(BufferA, BufferB, BufferC, FlagBuffer))
        print("success")

#print this shit to a file for now
def printToFile(fileName):
        with open(fileName, "w") as file:
            tri_count = 0
            for tri in collisionTri:
                file.write("Tri #{}: \n\t Vertex IDs: {}, {}, {} \n\t Flags: {} \n".format(tri_count, hex(tri.VertexA), hex(tri.VertexB), hex(tri.VertexC), tri.trueFlags))
                tri_count += 1
            tex_count = 0
            for tex in texture:
                file.write("Texture #{}: \n\t Color Type: {}: \n".format(tex_count, tex.type))
                tex_count += 1
                for pix in tex.pixel:
                    file.write("\t Pixel ({}, {}): {}, {}, {}, {} \n".format(pix.positionX, pix.positionY, pix.red, pix.green, pix.blue, pix.alpha))

fileName = input("fileName: ")
getTextureInfo(fileName)
getCollisionTris(fileName)
dumpAll = input("Dump all textures? ([y]/n)")
if (dumpAll == "n"):
    texName = input("Which Texture?: ")
    drawTexture(texName)
else:
    for index in range(len(texture)):
        texName = index
        drawTexture(texName)
printToFile(outputFileName)