from geo_objects import *
import matplotlib.pyplot as plt
import struct
import numpy as np

bones = []


def getBoneTree(fileName):
    with open(fileName, "rb") as file:
        file.seek(0x18)
        animSetupOffset = int.from_bytes(file.read(4), "big")
        if animSetupOffset == 0:
            print("this file has no bones")
            return
        file.seek(animSetupOffset)
        (scale, boneCount) = struct.unpack(">fH2x", file.read(8))
        print(scale, boneCount)

        fig = plt.figure(figsize=(5, 5))
        ax = plt.axes(projection="3d")

        for bone in range(boneCount):
            (posX, posY, posZ, bone_id, parent_bone) = struct.unpack(">3f2H", file.read(16))
            print(bone, posX, posY, posZ, bone_id, parent_bone if parent_bone != 0xFFFF else "Root")
            bones.append([posX, posY, posZ, bone_id, parent_bone])
        valX, valY, valZ = [], [], []
        for bone in bones:
            valX.append(bone[0])
            valY.append(bone[2])
            valZ.append(bone[1])

        max_range = np.array([abs(max(valX) - min(valX)), abs(max(valY) - min(valY)), abs(max(valZ) - min(valZ))]).max()
        Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (max(valX) + min(valX))
        Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (max(valY) + min(valY))
        Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (max(valZ) + min(valZ))

        for xb, yb, zb in zip(Xb, Yb, Zb):
            ax.plot([xb], [yb], [zb], 'w')

        ax.set_xlim3d([min(Xb), max(Xb)] if min(valX) != max(valX) else [min(valX) - 0.05, max(valX) + 0.05])
        ax.set_zlim3d([min(Zb), max(Zb)] if min(valZ) != max(valZ) else [min(valZ) - 0.05, max(valZ) + 0.05])
        ax.set_ylim3d([min(Yb), max(Yb)] if min(valY) != max(valY) else [min(valY) - 0.05, max(valY) + 0.05])

        for bone in bones:
            if bone[4] == 0xFFFF:
                ax.scatter(bone[0], bone[2], bone[1])
            else:
                ax.scatter([bone[0], bones[bone[4]][0]], [bone[2], bones[bone[4]][2]], [bone[1], bones[bone[4]][1]], color="red", s=10)
                ax.plot([bone[0], bones[bone[4]][0]], [bone[2], bones[bone[4]][2]], [bone[1], bones[bone[4]][1]], color="black")
                ax.text(bone[0], bone[2], bone[1], "{}".format(bone[3]), color="blue", zorder=0)
        plt.show()
