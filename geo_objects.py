
colorFormat = {
    1: "CI4",
    2: "CI8",
    4: "RGBA5551",
    8: "RGBA8888",
    16: "IA8"
}

class Texture:
    def __init__(self, Offset, nextOffset, Type, X, Y):
        self.Offset = Offset
        self.nextOffset = nextOffset
        self.type = colorFormat[Type]
        if self.type == "IA8":
            self.colorbytes = 1
        else:
            self.colorBytes = Type/2
        self.x_dim = X
        self.y_dim = Y

class Pixel:
    def __init__(self, positionAbs, positionX, positionY, R, G, B, A):
        self.positionAbs = positionAbs
        self.positionX = positionX
        self.positionY = positionY
        self.red = R
        self.green = G
        self.blue = B
        self.alpha = A

class DisplayTri:
    def __init__(self, Texture, Vertices, LOD, index):
        self.texture = Texture
        self.VertexLookup = Vertices
        self.VertexA = Vertices[0]
        self.VertexB = Vertices[1]
        self.VertexC = Vertices[2]
        self.triIsLOD = LOD
        self.collision = None
        self.Flags = [False for i in range(0x20)]
        self.index = index
        self.edited = False
        self.unk = None

    def __str__(self):
        return "Triangle #{}".format(self.index)

class CollisionTri:
    def __init__(self, VertexA, VertexB, VertexC, Flags, unk8):
        self.VertexLookup = [VertexA, VertexB, VertexC]
        self.Flags = []
        self.trueFlags = []
        self.matched = False
        self.flags_as_bytes = 0
        self.updated = False
        self.unk = unk8

        #turn the bitfield into a list for ease of access
        for i in range(0x20):
            self.Flags.append(bool(Flags & (2 ** i) != 0))

    def __eq__(self, other):
        if self.VertexLookup == other.VertexLookup:
            return True
        else:
            return False

class Vertex:
    def __init__(self, Xpos, Ypos, Zpos, U, V, R, G, B, A):
        self.positionX = Xpos
        self.positionY = Ypos
        self.positionZ = Zpos
        self.textureU = U
        self.textureV = V
        self.red = R
        self.green = G
        self.blue = B
        self.alpha = A

        self.hex_string = hex(self.red)[2:] + hex(self.green)[2:] + hex(self.blue)[2:] + hex(self.alpha)[2:]
