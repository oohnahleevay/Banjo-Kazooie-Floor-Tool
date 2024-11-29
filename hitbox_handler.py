import PySimpleGUI as sg
import matplotlib.pyplot as plt
import struct
import numpy as np

def getHitbox(fileName):
    with open(fileName, "rb") as file:
        file.seek(0x14)
        hitboxSetupOffset = int.from_bytes(file.read(4), "big")
        if hitboxSetupOffset == 0:
            print("this file has no bounding box")
            return
        file.seek(hitboxSetupOffset)
        type1structCount = int.from_bytes(file.read(2), "big")
        type2structCount = int.from_bytes(file.read(2), "big")
        type3structCount = int.from_bytes(file.read(2), "big")
        header_unk4 = int.from_bytes(file.read(2), "big")
        for i in range(type1structCount):
            vtx1_x,vtx1_y,vtx1_z,vtx2_x,vtx2_y,vtx2_z,vtx3_x,vtx3_y,vtx3_z = struct.unpack(">9h", file.read(18))
            unk1,unk2,unk3 = struct.unpack(">3B", file.read(3))
            unk4, unk5 = struct.unpack(">2B", file.read(2))
            file.seek(1, 1)
            print("Type 1 Struct #{}: [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], [{}, {}, {}], {}, {}".format(i,vtx1_x,vtx1_y,vtx1_z,vtx2_x,vtx2_y,vtx2_z,vtx3_x,vtx3_y,vtx3_z,unk1,unk2,unk3, unk4, unk5))
        for i in range(type2structCount):
            unk1,unk2 = struct.unpack(">2h", file.read(4))
            vtx_x,vtx_y,vtx_z = struct.unpack(">3h", file.read(6))
            unk3,unk4,unk5 = struct.unpack(">3B", file.read(3))
            unk6, unk7 = struct.unpack(">Bb", file.read(2))
            file.seek(1, 1)
            print("Type 2 Struct #{}: {}, {}, [{}, {}, {}], [{}, {}, {}], {}, {}".format(i, unk1,unk2, vtx_x, vtx_y, vtx_z, unk3, unk4, unk5, unk6, unk7))
        for i in range(type3structCount):
            (unk1,) = struct.unpack(">h", file.read(2))
            vtx_x,vtx_y,vtx_z = struct.unpack(">3h", file.read(6))
            unk3,unk4 = struct.unpack(">Bb", file.read(2))
            file.seek(2, 1)
            print("Type 3 Struct #{}: {}, [{}, {}, {}], {}, {}".format(i, unk1, vtx_x, vtx_y, vtx_z, unk3, unk4))

        #fig = plt.figure(figsize=(5, 5))
        #ax = plt.axes(projection="3d")

        #for bone in range(boneCount):
            #(posX, posY, posZ, bone_id, parent_bone) = struct.unpack(">3f2H", file.read(16))
            #print(bone, posX, posY, posZ, bone_id, parent_bone if parent_bone != 0xFFFF else "Root")
            #bones.append([posX, posY, posZ, bone_id, parent_bone])
        #valX, valY, valZ = [], [], []
        #for bone in bones:
            #valX.append(bone[0])
            #valY.append(bone[2])
            #valZ.append(bone[1])

        #max_range = np.array([abs(max(valX) - min(valX)), abs(max(valY) - min(valY)), abs(max(valZ) - min(valZ))]).max()
        #Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (max(valX) + min(valX))
        #Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (max(valY) + min(valY))
        #Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (max(valZ) + min(valZ))

        #for xb, yb, zb in zip(Xb, Yb, Zb):
            #ax.plot([xb], [yb], [zb], 'w')

        #ax.set_xlim3d([min(Xb), max(Xb)] if min(valX) != max(valX) else [min(valX) - 0.05, max(valX) + 0.05])
        #ax.set_zlim3d([min(Zb), max(Zb)] if min(valZ) != max(valZ) else [min(valZ) - 0.05, max(valZ) + 0.05])
        #ax.set_ylim3d([min(Yb), max(Yb)] if min(valY) != max(valY) else [min(valY) - 0.05, max(valY) + 0.05])

        #for bone in bones:
            #if bone[4] == 0xFFFF:
                #ax.scatter(bone[0], bone[2], bone[1])
            #else:
                #ax.scatter([bone[0], bones[bone[4]][0]], [bone[2], bones[bone[4]][2]], [bone[1], bones[bone[4]][1]], color="red", s=10)
                #ax.plot([bone[0], bones[bone[4]][0]], [bone[2], bones[bone[4]][2]], [bone[1], bones[bone[4]][1]], color="black")
                #ax.text(bone[0], bone[2], bone[1], "{}".format(bone[3]), color="blue", zorder=0)
        #plt.show()