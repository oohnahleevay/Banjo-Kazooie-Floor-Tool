import matplotlib.pyplot as plt
import struct
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from display_list import *
from texture_handler import *
from collision import *
from vertex_handler import *
from geometry_layout import *


def promptMapFile():
    complete = False
    sg.theme("Default 1")
    file_prompt = [
        [sg.Text("Select a Model File.")],
        [
            sg.Text("File please."),
            sg.In(readonly=True, enable_events=True, key="-FILE-"),
            sg.FileBrowse(file_types=(("Map Files", "*.bin"),))
        ],
        [sg.Button("Choose", disabled=True), sg.Button("Cancel")],
    ]

    window = sg.Window("Select a map bin", file_prompt)

    while 1:
        fileName = None
        event, values = window.read()
        if event == "Cancel" or event == sg.WIN_CLOSED:
            break
        if values["-FILE-"]:
            window["Choose"].update(disabled=False)
        if event == ("Choose"):
            fileName = values["-FILE-"]
            if isModelFile(fileName):
                complete = showImportProgress(fileName)
                break
    window.close(); del window
    return fileName, complete


def showImportProgress(fileName):
    complete = False

    layout = [
        [sg.Text(key="-STATUS-")],
        [sg.ProgressBar(0, "h", size=(30,20), expand_x=True, key="-PROGRESS-")],
        [sg.Text(key="-COUNT-")]
    ]

    window = sg.Window("Opening File", layout, finalize=True)
    window.write_event_value("-BOOP-", True)

    while 1:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

        if event == "-END KEY-":
            complete = True
            break

        if event == "-BOOP-":
            window.perform_long_operation(lambda: parseFile(fileName, window), "-END KEY-")

    window.close(); del window
    return complete


def showTriViewer(fileName):
    sg.theme("Default 1")
    edits_made = False
    currentTri = displayTri[0]
    currentTexture = sg.Image(data=drawTexture(currentTri.texture), key="-TEXTURE-")
    fig = drawCurrentTriSelection(currentTri.VertexA, currentTri.VertexB, currentTri.VertexC)
    flag_block = [sg.Checkbox("{}".format(hex(index)), default=val if val else False, size=(4,1),
                              disabled=currentTri.collision is None, enable_events=True,
                              key="-FLAG {}-".format(index)) for index, val in enumerate(currentTri.Flags)]

    menu_bar = [
        ["File", ["&Save", "&Open"]]
    ]

    tri_select = [
        [sg.Checkbox("Exclude Tris Without Collision", enable_events=True, key="-EXCLUDE-")],
        [
            sg.Checkbox("Filter by Texture: ", key="-FILTER-", enable_events=True),
            sg.DropDown([i for i in range(len(texture))], default_value=0, enable_events=True, key="-FILTER ID-")
        ],
        [sg.Checkbox("Edit All Tris with Texture", disabled=True, enable_events=True, key="-EDIT ALL-")],
        [sg.Listbox(values=displayTri, expand_x=True, expand_y=True, font=("Segoe UI", "14"), key="-TRILIST-", enable_events=True)],
    ]

    tri_params = [
        [currentTexture],
        [
            sg.Text("Texture: {}".format(currentTri.texture), key="-TEXTURE ID-"),
            sg.Text("Mystery Val: {}".format(hex(currentTri.unk) if currentTri.unk else None), key="-MYSTERY-")
        ],
        [sg.Text("Vertex 1: {}, {}, {}".format(
                 vertex[currentTri.VertexA].positionX,
                 vertex[currentTri.VertexA].positionY,
                 vertex[currentTri.VertexA].positionZ
                 ),
         key="-VERTEX 1-")
         ],
        [sg.Text("Vertex 2: {}, {}, {}".format(
                 vertex[currentTri.VertexB].positionX,
                 vertex[currentTri.VertexB].positionY,
                 vertex[currentTri.VertexB].positionZ
                 ),
         key="-VERTEX 2-")
         ],
        [sg.Text("Vertex 3: {}, {}, {}".format(
                 vertex[currentTri.VertexC].positionX,
                 vertex[currentTri.VertexC].positionY,
                 vertex[currentTri.VertexC].positionZ
                 ),
         key="-VERTEX 3-")
         ]
    ]

    tri_unpack = [
        [sg.Menu(menu_bar, key="-MENU-")],
        [sg.Column(tri_params), sg.Canvas(key="-CANVAS-")],
        [flag_block[i] for i in range(0, 8)],
        [flag_block[i] for i in range(8, 16)],
        [flag_block[i] for i in range(16, 24)],
        [flag_block[i] for i in range(24, 32)]
    ]

    layout = [
       [sg.Column(tri_select, expand_y=True),
        sg.VSeparator(),
        sg.Column(tri_unpack)]
    ]

    window = sg.Window("BK Tri Viewer", layout, finalize=True, enable_close_attempted_event=True)
    window["-TRILIST-"].update(set_to_index=0)
    flag_keys = ["-FLAG {}-".format(i) for i in range(32)]
    for flag in flag_keys:
        window[flag].widget.pack(fill="x")

    triangle_plot = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)
    triangle_plot.draw()
    triangle_plot.get_tk_widget().pack(fill=None, side="bottom")

    while 1:
        event, values = window.read()

        if event == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            if edits_made:
                ch = sg.popup_yes_no("Would you like to save?", title="Save Changes?")
                if ch == "Yes":
                    if saveUpdatedCollisions(fileName):
                        break
                    else:
                        sg.popup("Something happened.")
            break

        if event == "-TRILIST-":
            currentTri = values["-TRILIST-"][0]
            window["-TEXTURE-"].update(data=drawTexture(currentTri.texture))
            window["-MYSTERY-"].update("Mystery Val: {}".format(hex(currentTri.unk) if currentTri.unk else None))
            window["-TEXTURE ID-"].update("Texture: {}".format(currentTri.texture))

            updated_verts = [
                (vertex[currentTri.VertexA].positionX, vertex[currentTri.VertexA].positionY, vertex[currentTri.VertexA].positionZ),
                (vertex[currentTri.VertexB].positionX, vertex[currentTri.VertexB].positionY, vertex[currentTri.VertexB].positionZ),
                (vertex[currentTri.VertexC].positionX, vertex[currentTri.VertexC].positionY, vertex[currentTri.VertexC].positionZ)
            ]
            triangle_plot.get_tk_widget().forget()
            fig = drawCurrentTriSelection(currentTri.VertexA, currentTri.VertexB, currentTri.VertexC)
            triangle_plot = FigureCanvasTkAgg(fig, window["-CANVAS-"].TKCanvas)
            triangle_plot.draw()
            triangle_plot.get_tk_widget().pack(fill=None, side="bottom")
            plt.close()
            window["-VERTEX 1-"].update("Vertex 1: {}, {}, {}".format(updated_verts[0][0], updated_verts[0][1], updated_verts[0][2]))
            window["-VERTEX 2-"].update("Vertex 2: {}, {}, {}".format(updated_verts[1][0], updated_verts[1][1], updated_verts[1][2]))
            window["-VERTEX 3-"].update("Vertex 3: {}, {}, {}".format(updated_verts[2][0], updated_verts[2][1], updated_verts[2][2]))
            for index, val in enumerate(currentTri.Flags):
                window["-FLAG {}-".format(index)].update(value=val if val else False, disabled=currentTri.collision is None)


        if event == "-EXCLUDE-":
            window["-TRILIST-"].update(values=handleFilters(values["-FILTER-"], values["-EXCLUDE-"], values["-FILTER ID-"]))

        if event == "-FILTER-":
            window["-TRILIST-"].update(values=handleFilters(values["-FILTER-"], values["-EXCLUDE-"], values["-FILTER ID-"]))
            if values["-FILTER-"]:
                window["-EDIT ALL-"].update(disabled=False)
            else:
                window["-EDIT ALL-"].update(disabled=True)

        if event == "-FILTER ID-" and values["-FILTER-"]:
            window["-TRILIST-"].update(values=handleFilters(values["-FILTER-"], values["-EXCLUDE-"], values["-FILTER ID-"]))

        if event in flag_keys:
            currentTri.Flags = [values[flag] for flag in flag_keys]
            currentTri.edited = True
            edits_made = True
            if values["-EDIT ALL-"]:
                for disp_tri in displayTri:
                    if disp_tri.texture == values["-FILTER ID-"]:
                        disp_tri.Flags = [values[flag] for flag in flag_keys]
                        disp_tri.edited = True
            window.perform_long_operation(lambda: storeUpdatedCollisions(), "-STORED-")

        if event == "Save":
            saved = saveUpdatedCollisions(fileName)
            if saved: sg.Window("Save Successful", [[sg.Text("Saved!", font=("Verdana","12"))], [sg.Button("OK", bind_return_key=True)]], element_justification="c", element_padding=(150, 7), modal=True).read(close=True)

        if event == "Open":
            fileName = sg.popup_get_file("Choose Map Bin.", file_types=(("Map Files", "*.bin"),), no_window=True)
            if fileName:
                clearTris()
                showImportProgress(fileName)
                window.refresh()
                window["-TRILIST-"].update(set_to_index=0)
                window.write_event_value("-TRILIST-", displayTri)


    window.close(); del window


def drawCurrentTriSelection(current_vert1, current_vert2, current_vert3):
    fig = plt.figure(figsize=(3.2,3))
    ax = plt.axes(projection="3d")
    triX = [vertex[current_vert1].positionX, vertex[current_vert2].positionX, vertex[current_vert3].positionX]
    triZ = [vertex[current_vert1].positionY, vertex[current_vert2].positionY, vertex[current_vert3].positionY]
    triY = [vertex[current_vert1].positionZ, vertex[current_vert2].positionZ, vertex[current_vert3].positionZ]
    verts = [list(zip(triX, triY, triZ))]
    ax.add_collection3d(Poly3DCollection(verts, facecolors="#FFFFFF00", edgecolors="black"))

    max_range = np.array([abs(max(triX) - min(triX)), abs(max(triY) - min(triY)), abs(max(triZ) - min(triZ))]).max()
    Xb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][0].flatten() + 0.5 * (max(triX) + min(triX))
    Yb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][1].flatten() + 0.5 * (max(triY) + min(triY))
    Zb = 0.5 * max_range * np.mgrid[-1:2:2, -1:2:2, -1:2:2][2].flatten() + 0.5 * (max(triZ) + min(triZ))

    for xb, yb, zb in zip(Xb, Yb, Zb):
        ax.plot([xb], [yb], [zb], 'w')

    ax.set_xlim3d([min(Xb), max(Xb)] if min(triX) != max(triX) else [min(triX) - 0.05, max(triX) + 0.05])
    ax.set_zlim3d([min(Zb), max(Zb)] if min(triZ) != max(triZ) else [min(triZ) - 0.05, max(triZ) + 0.05])
    ax.set_ylim3d([min(Yb), max(Yb)] if min(triY) != max(triY) else [min(triY) - 0.05, max(triY) + 0.05])
    #ax.plot(triX, triY, triZ)
    return fig



def isModelFile(fileName):
    with open(fileName, "rb") as file:
        if int.from_bytes(file.read(4), "big") != 0xB:
            sg.popup("Not a model file!")
            return False
        file.seek(0,0)
        backup = file.read()
    with open("{}.bak".format(fileName), "wb") as file:
        file.write(backup)
        return True

def parseFile(fileName, window):
    window["-STATUS-"].update("Getting Textures")
    getTextureInfo(fileName, window)
    window["-STATUS-"].update("Getting Vertices")
    getVertices(fileName, window)
    window["-STATUS-"].update("Getting Collisions")
    getCollisionTris(fileName, window)
    window["-STATUS-"].update("Checking for tris without collisions.")
    getGeometryLayouts(fileName)
    window["-STATUS-"].update("Matching collisions to surface tris")
    getDisplayList(fileName)
    matchCollisionTri(window)
    window["-STATUS-"].update("Success!")

    dumpRequest = "n"
    #dumpRequest = input("Dump textures? ([y]/n)\n")
    if dumpRequest != "n":
        dumpAll = input("Dump ALL textures? ([y]/n)\n")
        if dumpAll == "n":
            texName = input("Which Texture?: ")
            dumpTexture(texName)
        else:
            for index in range(len(texture)):
                texName = index
                dumpTexture(texName)


def handleFilters(optTex, optColl, ID_list):
    new_list = [disp_tri for disp_tri in displayTri]
    if optColl:
        new_list.clear()
        for disp_tri in displayTri:
            if disp_tri.collision is not None:
                new_list.append(disp_tri)
    if optTex:
        buffer = [disp_tri for disp_tri in new_list]
        new_list.clear()
        for disp_tri in buffer:
            if disp_tri.texture == ID_list:
                new_list.append(disp_tri)
    return new_list


def clearTris():
    texture.clear()
    displayTri.clear()
    vertex.clear()
    collisionTri.clear()
    return


def saveUpdatedCollisions(fileName):
    with open(fileName, "rb+") as file:
        file.seek(0x1C)
        collisionSetupOffset = int.from_bytes(file.read(4), "big")
        file.seek(collisionSetupOffset, 0)
        file.seek(16, 1)
        unknownEntryCount = int.from_bytes(file.read(2), "big")
        file.seek(6, 1)
        file.seek(unknownEntryCount * 4, 1)
        for coll_tri in collisionTri:
            file.seek(8, 1)
            if collisionTri[collisionTri.index(coll_tri)].updated:
                print("saved {} as {}".format(hex(file.tell()), hex(collisionTri[collisionTri.index(coll_tri)].flags_as_bytes)))
                file.write(struct.pack(">L", collisionTri[collisionTri.index(coll_tri)].flags_as_bytes))
            else:
                file.seek(4, 1)
    return True


def storeUpdatedCollisions():
    for disp_tri in displayTri:
        if disp_tri.edited:
            collisionTri[disp_tri.collision].flags_as_bytes = 0
            for index, flag in enumerate(disp_tri.Flags):
                if flag:
                    collisionTri[disp_tri.collision].flags_as_bytes += 2 ** index
            collisionTri[disp_tri.collision].updated = True
            print("Updated Tri {}, Collision {} ({})".format(displayTri.index(disp_tri), disp_tri.collision, hex(collisionTri[disp_tri.collision].flags_as_bytes)))
    return True

