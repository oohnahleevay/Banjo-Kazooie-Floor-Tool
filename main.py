from display_list import displayTri
from vertex_handler import vertex
from GUI import promptMapFile, showTriViewer
from geometry_layout import bones
from bone_handler import getBoneTree
from hitbox_handler import getHitbox

outputFileName = "output.txt" #lol

#print this shit to a file for now
def printToFile(fileName):
        with open(fileName, "w") as file:
            #tri_count = 0
            #for tri in displayTri:
                #file.write("Tri #{}: \n\t Vertices: \n\t\t{}, {}, {}\n\t\t{}, {}, {} \n\t\t{}, {}, {} \n\tCollision: {} \n\tTexture: {} \n".format(
                    #tri_count, vertex[tri.VertexA].positionX, vertex[tri.VertexA].positionY, vertex[tri.VertexA].positionZ,
                    #vertex[tri.VertexB].positionX, vertex[tri.VertexB].positionY, vertex[tri.VertexB].positionZ, vertex[tri.VertexC].positionX,
                    #vertex[tri.VertexC].positionY, vertex[tri.VertexC].positionZ, tri.collision if tri.collision is not None else "No Collision", tri.texture))
                #tri_count += 1
            if len(bones):
                for bone in bones:
                    file.write("Bone #{}:\n\tDisplay List Offset: {}\n\tUnknown Value: {}\n".format(bone.index, hex(bone.displayList), hex(bone.unkA)))

fileName, complete = promptMapFile()
if fileName and complete:
    getBoneTree(fileName)
    getHitbox(fileName)
    showTriViewer(fileName)
    printToFile(outputFileName)


