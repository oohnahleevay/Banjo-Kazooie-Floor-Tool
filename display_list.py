from geometry_layout import noCollisionTri
from texture_handler import texture
from collision import collisionTri
import numpy as np
import PySimpleGUI as sg
from geo_objects import *

displayTri = []

F3DEX_command = {
    0x00: "G_SPNOOP",
    0x01: "G_MTX",
    0x03: "G_MOVEMEM",
    0x04: "G_VTX",
    0x06: "G_DL",
    0xAF: "G_LOAD_UCODE",
    0xB0: "G_BRANCH_Z",
    0xB1: "G_TRI2",
    0xB2: "G_MODIFYVTX",
    0xB3: "G_RDPHALF_2",
    0xB4: "G_RDPHALF_1",
    0xB5: "G_QUAD",
    0xB6: "G_CLEARGEOMETRYMODE",
    0xB7: "G_SETGEOMETRYMODE",
    0xB8: "G_ENDDL",
    0xB9: "G_SetOtherMode_L",
    0xBA: "G_SetOtherMode_H",
    0xBB: "G_TEXTURE",
    0xBC: "G_MOVEWORD",
    0xBD: "G_POPMTX",
    0xBE: "G_CULLDL",
    0xBF: "G_TRI1",
    0xC0: "G_NOOP",
    0xE4: "G_TEXRECT",
    0xE5: "G_TEXRECTFLIP",
    0xE6: "G_RDPLOADSYNC",
    0xE7: "G_RDPPIPESYNC",
    0xE8: "G_RDPTILESYNC",
    0xE9: "G_RDPFULLSYNC",
    0xEA: "G_SETKEYGB",
    0xEB: "G_SETKEYR",
    0xEC: "G_SETCONVERT",
    0xED: "G_SETSCISSOR",
    0xEE: "G_SETPRIMDEPTH",
    0xEF: "G_RDPSetOtherMode",
    0xF0: "G_LOADTLUT",
    0xF2: "G_SETTILESIZE",
    0xF3: "G_LOADBLOCK",
    0xF4: "G_LOADTILE",
    0xF5: "G_SETTILE",
    0xF6: "G_FILLRECT",
    0xF7: "G_SETFILLCOLOR",
    0xF8: "G_SETFOGCOLOR",
    0xF9: "G_SETBLENDCOLOR",
    0xFA: "G_SETPRIMCOLOR",
    0xFB: "G_SETENVCOLOR",
    0xFC: "G_SETCOMBINE",
    0xFD: "G_SETTIMG",
    0xFE: "G_SETZIMG",
    0xFF: "G_SETCIMG"
}

def getDisplayList(fileName):
    with open(fileName, "rb") as file:
        file.seek(0xC)
        displayListOffset = int.from_bytes(file.read(4), "big")
        if (displayListOffset == 0):
            print("what")
            return
        file.seek(displayListOffset, 0)
        displayCommandCount = int.from_bytes(file.read(4), "big")
        file.seek(4, 1)
        vertex_buffer = []
        currentTextureOffset = 0xFFFFFF
        currentCommand = 0
        for command in range(displayCommandCount):
            commandType = F3DEX_command[int.from_bytes(file.read(1), "big")]
            if commandType == "G_DL":
                displayList = True
                vertex_buffer = np.zeros(200, "int")
                file.seek(7, 1)
            elif commandType == "G_ENDDL":
                displayList = False
                currentTextureOffset = 0xFFFFFF
                file.seek(7, 1)
            elif commandType == "G_SETTIMG":
                file.seek(3, 1)
                targetedSegment = int.from_bytes(file.read(1), "big")
                currentTextureOffset = int.from_bytes(file.read(3), "big")
            elif commandType == "G_VTX":
                vertexStart = int.from_bytes(file.read(1), "big")
                vertexReadCount = (int.from_bytes(file.read(2), "big") & 0xFC00) / 0x400
                targetedSegment = int.from_bytes(file.read(1), "big")
                vertexRelOffset = int.from_bytes(file.read(3), "big")

                for vtx in range(int(vertexReadCount)):
                    vertex_buffer[vtx] = vertexRelOffset / 0x10 + vtx + vertexStart
                #print(vertex_buffer)
            elif commandType == "G_TRI2":
                for glcommand in noCollisionTri:
                    if currentCommand == glcommand:
                        triIsLOD = True
                        break
                    else:
                        triIsLOD = False
                if not noCollisionTri:
                    triIsLOD = False
                currentTriVertices = [0, 0, 0]
                for i in range(3):
                    currentTriVertices[i] = int(int.from_bytes(file.read(1), "big") /2)
                getDisplayTris(currentTextureOffset, vertex_buffer, currentTriVertices, triIsLOD)
                file.seek(1, 1)
                for i in range(3):
                    currentTriVertices[i] = int(int.from_bytes(file.read(1), "big") /2)
                getDisplayTris(currentTextureOffset, vertex_buffer, currentTriVertices, triIsLOD)
            elif commandType == "G_TRI1":
                for glcommand in noCollisionTri:
                    if currentCommand == glcommand:
                        triIsLOD = True
                        break
                    else:
                        triIsLOD = False
                if not noCollisionTri:
                    triIsLOD = False
                currentTriVertices = [0, 0, 0]
                file.seek(4, 1)
                for i in range(3):
                    currentTriVertices[i] = int(int.from_bytes(file.read(1), "big") /2)
                getDisplayTris(currentTextureOffset, vertex_buffer, currentTriVertices, triIsLOD)
            else:
                file.seek(7, 1)
                #print(hex(file.tell() - 1), commandType, hex(int.from_bytes(file.read(7), "big")))
            currentCommand += 1

def getDisplayTris(display_texture_offset, vertex_buffer, display_tri_vertices, tri_is_lod):
    displayTextureID = None
    for tex in texture:
        if tex.Offset <= display_texture_offset < tex.nextOffset:
            displayTextureID = texture.index(tex)
    if displayTextureID == None:
        print("something went wrong")
    #print(display_texture_offset, displayTextureID)
    displayTriVertex = [0, 0, 0]
    for vtx in display_tri_vertices:
        displayTriVertex[display_tri_vertices.index(vtx)] = vertex_buffer[vtx]
    #print(display_tri_vertices, displayTriVertex)
    if tri_is_lod:
        displayTri.append(DisplayTri(displayTextureID, displayTriVertex, tri_is_lod, None))
    else:
        displayTri.append(DisplayTri(displayTextureID, displayTriVertex, False, None))



# match duplicate collision tris to tri in display list
def matchCollisionTri(window:sg.Window):
    window["-PROGRESS-"].update(0, len(displayTri))
    for disp_tri in displayTri:
        disp_tri.index = displayTri.index(disp_tri)
        if not disp_tri.triIsLOD:
            try:
                disp_tri.collision = collisionTri.index(disp_tri)
                #print("matched with collisionTri {}, {} == {}!".format(disp_tri.collision, disp_tri.VertexLookup, coll_tri.VertexLookup))
                disp_tri.Flags = collisionTri[disp_tri.collision].Flags
                disp_tri.unk = collisionTri[disp_tri.collision].unk
                collisionTri[disp_tri.collision].matched = True
            except ValueError:
                continue
            #if disp_tri.collision is None:
                #print("disp_tri not matched!: {} ({})".format(disp_tri.VertexLookup, disp_tri.index))
        if disp_tri.index % (int(len(displayTri) / 10)) == 0:
            window["-PROGRESS-"].update(disp_tri.index)
            window["-COUNT-"].update("{}/{} matched".format(disp_tri.index, len(displayTri)))

