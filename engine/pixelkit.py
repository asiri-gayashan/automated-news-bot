"""Pixel-art kit for the 1:1 pixel news template.

Bright palette + reusable 8-bit sprites + scene helpers.
Build a scene:   scene = Scene(); scene.sky(); scene.add(SPRITES['rocket'], 40, 5); scene.ground()
Then:            post["pixel"] = scene.json()
"""

PALETTE = {
    "K": "#10123A",  # navy outline
    "D": "#2F5BFF",  # bright blue
    "d": "#1C3BCC",  # deep blue
    "G": "#C9D6FF",  # pale blue-grey
    "g": "#9BE7C4",  # mint (ground)
    "m": "#FF8FC7",  # pink
    "n": "#C7B5FF",  # lavender
    "W": "#FFFFFF",  # white
    "C": "#FF3B5C",  # hot red
    "L": "#FFD23F",  # gold
    "Y": "#FFE14D",  # yellow
    "N": "#3DFF8A",  # neon green
    "B": "#22D3EE",  # cyan
    "P": "#FF4FD8",  # hot pink
    "S": "#BFE6FF",  # sky
    "R": "#FF3B30",  # red
    "O": "#FF9F1C",  # orange
    "V": "#8B5CF6",  # violet
    "T": "#FFB4A2",  # peach
    "Z": "#5B4636",  # brown
}

SPRITES = {
    "sun": ["...RRR...", ".RRORORR.", ".RORRROR.", "RRRRRRRRR", "RORRRRROR", "RRRRRRRRR", ".RORRROR.", ".RRORORR.", "...RRR..."],
    "cloud": ["....WWWW......", "..WWWWWWWW.WW.", ".WWWWWWWWWWWWW", "WWWWWWWWWWWWWW", ".GGGGGGGGGGGG."],
    "spark_p": [".P.", "PWP", ".P."],
    "spark_b": [".B.", "BWB", ".B."],
    "spark_y": [".Y.", "YWY", ".Y."],
    "bolt": ["...KKKKK", "..KYYYYK", "..KYYYK.", ".KYYYK..", ".KYYYYYK", "KYYYYYK.", "KKKYYYK.", "..KYYK..", "..KYK...", ".KYK....", ".KK....."],
    "coin": ["...KKKKK...", ".KKLLLLLKK.", ".KLLLRLLLK.", "KLLLRRRRLLK", "KLLRLRLLLLK", "KLLLRRRLLLK", "KLLLLRLRLLK", "KLLRRRRLLLK", ".KLLLRLLLK.", ".KKLLLLLKK.", "...KKKKK..."],
    # tall rocket 11 wide x 30 tall
    "rocket": [
        ".....K.....", "....KWK....", "....KWK....", "...KWWWK...", "...KWWWK...", "..KWWWWWK..", "..KCCCCCK..",
        "..KWWWWWK..", "..KWBBBWK..", "..KWBKBWK..", "..KWBBBWK..", "..KWWWWWK..", "..KWWWWWK..", "..KDDDDDK..",
        "..KWWWWWK..", "..KWWWWWK..", "..KWWWWWK..", "..KWWWWWK..", "..KWWWWWK..", "..KDDDDDK..", "..KWWWWWK..",
        "..KWWWWWK..", ".KKWWWWWKK.", "KCKWWWWWKCK", "KCKWWWWWKCK", "KCKKKKKKKCK", "KK.KKKKK.KK", "....KKK....",
    ],
    # launch tower 7 wide x 34 tall
    "tower": ["KKKKKKK"] + ["K.K.K.K", "KK.K.KK"] * 16 + ["KKKKKKK"],
    "smoke": ["....WWW......WW....", "..WWWWWWW..WWWWW...", ".WWWGWWWWWWWWGWWWW.", "WWWGGGWWWWWWGGGWWWW", ".WGGGGGWWWWGGGGGWW.", "..GGGGG.GGGGGGGG..."],
    "flame": ["..OYYYO..", ".OYYWYYO.", ".OYWWWYO.", "..OYWYO..", "..ORYRO..", "...ORO...", "....R...."],
    "calendar": ["KKKKKKKKKKKKK", "KCKCCCCCCCKCK", "KCCCCCCCCCCCK", "KKKKKKKKKKKKK", "KWWWWWWWWWWWK", "KWWWWWWWWWWWK",
                 "KWWWWWWWWWWWK", "KWWWWWWWWWWWK", "KWWWWWWWWWWWK", "KWWWWWWWWWWWK", "KWWWWWWWWWWWK", "KKKKKKKKKKKKK"],
    "controller": [
        "...KKKKKKKKKKKKKKKK...", "..KVVVVVVVVVVVVVVVVK..", ".KVVVKVVVVVVVVVVPVVVK.", ".KVVKKKVVVVVVVVPVPVVK.",
        ".KVVVKVVVKKVKKVVPVVVVK", "KVVVVVVVVVVVVVVVVVVVVK", "KVVVVVVVKKKKKKVVVVVVVK", "KVVVVVVK......KVVVVVVK",
        "KVVVVVK........KVVVVVK", ".KVVVK..........KVVVK.", "..KKK............KKK..",
    ],
    "palm": [
        "..NN.....NN..", ".NNNN...NNNN.", "NN..NN.NN..NN", "N....NNN....N", ".....NZN.....", "....NNZNN....", "...N..Z..N...",
        "......Z......", "......Z......", ".....ZZ......", ".....Z.......", ".....Z.......", ".....ZZ......", "......Z......",
        "......Z......", ".....ZZZ.....",
    ],
    "download": ["....KKK....", "....KNK....", "....KNK....", "....KNK....", ".KKKKNKKKK.", "..KNNNNNK..", "...KNNNK...", "....KNK....", ".....K.....", "KKKKKKKKKKK"],
    "computer": [
        "KKKKKKKKKKKKKKKKKKKK", "KGGGGGGGGGGGGGGGGGGK", "KGKKKKKKKKKKKKKKKKGK",
        "KGKddddddddddddddKGK", "KGKdNdddddddddddKKGK".replace("KKGK","dKGK"), "KGKddddddddddddddKGK",
        "KGKdNNNddddddddddKGK", "KGKddddddddddddddKGK", "KGKdNNdddddddddddKGK", "KGKddddddddddddddKGK",
        "KGKKKKKKKKKKKKKKKKGK", "KGGGGGGGGGGGGGGGGGGK", "KGGRGOGNGGGGGGKKKKGK", "KGGGGGGGGGGGGGGGGGGK",
        "KKKKKKKKKKKKKKKKKKKK", "......KGGGGGGK......", ".....KKKKKKKKKK.....",
    ],
    "moth": [
        "..K.......K..", "...K.....K...", "....KKKKK....", "KKKKZKZKZKKKK", "KTTTKZZZKTTTK", "KTmTTKZKTTmTK", "KTTTTKZKTTTTK",
        ".KTTTKZKTTTK.", "..KTKZZZKTK..", "..KK.KZK.KK..", "......K......",
    ],
    "magnifier": ["..KKKKK....", ".KBBBBBK...", "KBWWBBBBK..", "KBWBBBBBK..", "KBBBBBBBK..", "KBBBBBBBK..", ".KBBBBBK...", "..KKKKKKK..", ".......KKK.", "........KKK", ".........KK"],
    }


def rack(leds):
    """Server rack 12x27. leds: list of 6 (a,b) colour-char pairs."""
    rows = ["KKKKKKKKKKKK", "KDDDDDDDDDDK"]
    for a, b in leds:
        rows += ["KDKKKKKKKKDK", "KDK%sK%sKGGKDK" % (a, b), "KDKKKKKKKKDK", "KDDDDDDDDDDK"]
    return rows + ["KKKKKKKKKKKK"]


# ---- character & effect sprites (from the computer-bug animation) ----
SPRITES.update({
    "moth_open": ["..K.......K..", "...K.....K...", "....KKKKK....", "....KWKWK....", "KKKKKZZZKKKKK", "KTTTKKZKKTTTK", "KTmTTKZKTTmTK", "KTTTTKZKTTTTK", ".KTTTKZKTTTK.", "..KKKZZZKKK..", ".....KZK.....", "......K......"],
    "moth_shut": ["..K.......K..", "...K.....K...", "....KKKKK....", "....KWKWK....", "...KKZZZKK...", "..KTTKZKTTK..", "..KTmKZKmTK..", "..KTTKZKTTK..", "..KTTKZKTTK..", "...KKZZZKK...", ".....KZK.....", "......K......"],
    "puff": ["..WW...", ".WWWWW.", "WWGWWWW", "WGGGWWW", ".WWWWW."],
    "heart": [".P.P.", "PPPPP", "PPPPP", ".PPP.", "..P.."],
    "bang": [".KKKKK.", "KWWCWWK", "KWWCWWK", "KWWCWWK", "KWWWWWK", "KWWCWWK", ".KKKKK.", "..KK...", "..K...."],
    "mag_small": ["..KKKKK..", ".KBBBBBK.", "KBWWBBBBK", "KBWBBBBBK", "KBBBBBBBK", ".KBBBBBK.", "..KKKKKKK", "......KKK"],
})
_PERSON_HEAD = ["....KKKK....", "...KZZZZK...", "..KZZZZZZK..", "..KTTTTTTK..", "..KKWKKWKK..", "..KTKTTKTK..", "..KTTTTTTK..",
                "..KTTCCTTK..", "...KTTTTK...", "..KKWWWWKK..", ".KWWWWBWWWK.", ".KWWWWBWWWK.", ".KTKWWBWWKTK", "..KWWWWWWK..",
                "..KWWWWWWK..", "..KDDKKDDK.."]
SPRITES["person_a"] = _PERSON_HEAD + ["..KDDK.KDDK.", "..KKK..KKK.."]   # walk frame A (cartoon engineer, lab coat)
SPRITES["person_b"] = _PERSON_HEAD + ["...KDDKDDK..", "...KKKKKK..."]   # walk frame B


def recolor(rows, mapping):
    """Return a copy of a sprite with characters swapped, e.g. recolor(S['computer'], {'d':'C','N':'W'})."""
    return ["".join(mapping.get(c, c) for c in r) for r in rows]


MINI_FONT = {"E": "111100110100111", "R": "110101110101101", "O": "010101101101010", "K": "101101110101101", "!": "010010010000010",
             "N": "10011101101110011001", "W": "1000110001101011010101010", "X": "101101010101101", "?": "110001010000010"}


def stamp(rows, txt, x0, y0, c):
    """Write tiny pixel text into a sprite (e.g. 'ERR' on a screen)."""
    rows = [list(r) for r in rows]; cx = x0
    for ch in txt:
        g = MINI_FONT[ch]; gw = len(g) // 5
        for j in range(5):
            for i in range(gw):
                if g[j * gw + i] == "1": rows[y0 + j][cx + i] = c
        cx += gw + 1
    return ["".join(r) for r in rows]


class Scene:
    def __init__(self, w=90, h=44, scale=10):
        self.w, self.h, self.scale, self.layers = w, h, scale, []

    def sky(self, c="S"):
        self.layers += [
            {"type": "rect", "x": 1, "y": 1, "w": self.w - 2, "h": 39, "c": c},
            {"type": "rect", "x": 0, "y": 2, "w": 1, "h": 38, "c": c},
            {"type": "rect", "x": self.w - 1, "y": 2, "w": 1, "h": 38, "c": c},
            {"type": "rect", "x": 2, "y": 0, "w": self.w - 4, "h": 1, "c": c},
        ]
        return self

    def add(self, rows, x, y, flip=False):
        self.layers.append({"type": "sprite", "x": x, "y": y, "rows": rows, "flipX": flip}); return self

    def rect(self, x, y, w, h, c):
        self.layers.append({"type": "rect", "x": x, "y": y, "w": w, "h": h, "c": c}); return self

    def mountain(self, x, w, h, c, snow="W", base=40):
        self.layers.append({"type": "mountain", "x": x, "base": base, "w": w, "h": h, "c": c, "snow": snow}); return self

    def text(self, s, x, y, c="K"):
        self.layers.append({"type": "text", "x": x, "y": y, "text": s, "c": c}); return self

    def ground(self, c="g"):
        self.rect(0, 40, self.w, 1, "K"); self.rect(0, 41, self.w, 3, c); return self

    def json(self):
        return {"w": self.w, "h": self.h, "scale": self.scale, "palette": PALETTE, "layers": self.layers}
