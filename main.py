from display_list import displayTri
from vertex_handler import vertex
from GUI import promptMapFile, showTriViewer

outputFileName = "output.txt" #lol

#print this shit to a file for now
def printToFile(fileName):
        with open(fileName, "w") as file:
            tri_count = 0
            for tri in displayTri:
                file.write("Tri #{}: \n\t Vertices: \n\t\t{}, {}, {}\n\t\t{}, {}, {} \n\t\t{}, {}, {} \n\tCollision: {} \n\tTexture: {} \n".format(
                    tri_count, vertex[tri.VertexA].positionX, vertex[tri.VertexA].positionY, vertex[tri.VertexA].positionZ,
                    vertex[tri.VertexB].positionX, vertex[tri.VertexB].positionY, vertex[tri.VertexB].positionZ, vertex[tri.VertexC].positionX,
                    vertex[tri.VertexC].positionY, vertex[tri.VertexC].positionZ, tri.collision if tri.collision is not None else "No Collision", tri.texture))
                tri_count += 1
            #tex_count = 0
            #for tex in texture:
            #    file.write("Texture #{}: \n\t Color Type: {}: \n".format(tex_count, tex.type))
            #    tex_count += 1
            #    for pix in tex.pixel:
            #        file.write("\t Pixel ({}, {}): {}, {}, {}, {} \n".format(pix.positionX, pix.positionY, pix.red, pix.green, pix.blue, pix.alpha)
fileName, complete = promptMapFile()
if fileName and complete:
    showTriViewer(fileName)


