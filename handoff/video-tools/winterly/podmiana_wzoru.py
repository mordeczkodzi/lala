"""Podmiana wzoru na kurtynie w gotowym ujęciu (np. choinka -> bałwanek -> śnieżynki na TYM SAMYM balkonie).

Bierze jedną klatkę z ujęcia (stopklatkę), nakłada na kurtynę nowy wzór z kropek w perspektywie,
dodaje powolny najazd kamery i padający śnieg. Wynik to krótki klip, który wstawiasz do montażu
zaraz po oryginalnym ujęciu (z białym błyskiem "flash" na zmianie wzoru).

Użycie:  python3 -I podmiana_wzoru.py podmiana.json

Przykład podmiana.json (wartości z reklamy A, klatka 3,79 s z klipu balkonu):
{
  "frame": "stopklatka.png",          # ffmpeg -ss 3.79 -i balkon.mp4 -frames:v 1 stopklatka.png
  "out": "podmiana.mp4",
  "top":    [1005, -0.19],            # górna krawędź kurtyny: y = 1005 - 0.19 * x  (zmierz na klatce!)
  "bottom": [1392, -0.1037],          # dolna krawędź kurtyny
  "x_range": [-150, 1230],            # kurtyna wychodzi poza kadr: rozciągnij poza 0..1080
  "grid": [61, 20],                   # kropki w poziomie i pionie, tak jak na oryginalnej kurtynie
  "patterns": [["snowman", 0.83], ["flakes", 1.37]],   # wzór i czas w sekundach
  "pattern_col": 27,                  # kolumna, od której rysuje się bałwanek (wyśrodkowanie)
  "zoom": 0.05
}
Krawędzie mierzysz tak: narysuj linie na klatce (cv2.line), obejrzyj powiększenie i popraw o kilka pikseli,
aż pod spodem nie prześwituje stary wzór. Wymaga: numpy, opencv-python, ffmpeg.
"""
import json, math, os, random, subprocess, sys
import numpy as np, cv2

FPS, W, H, CELL = 30, 1080, 1920, 24
C = {'W': (255, 255, 255), 'R': (235, 30, 40), 'O': (255, 140, 20), 'G': (30, 210, 70), 'C': (150, 215, 255), 'P': (255, 140, 115)}
SNOWMAN = [
    ".......W.......", "......RRR......", ".....RRRRR.....", "....RRRRRRR....", "...WWWWWWWWW...",
    "....WWWWWWW....", "...WW.WWW.WW...", "...WWWWWOOOW...", "...WW.WWW.WW...", "....WW...WW....",
    "..GGGGGGGGGGG..", "...WWWWWWGGW...", "..WWWWWWWGGWW..", ".WWWWWWRWWWWWW.", ".WWWWWWWWWWWWW.",
    ".WWWWWWRWWWWWW.", ".WWWWWWWWWWWWW.", "..WWWWWWWWWWW..", "...WWWWWWWWW...", "..............."]
SANTA = [  # twarz Mikołaja 20x20 (tak naprawdę wygląda na kurtynie 3x2 m z 400 diodami)
    "....................", ".........RRR........", "........RRRRRR......", ".......RRRRRRRRWW...",
    "......RRRRRRRR.WW...", "......RRRRRRRR......", ".....WWWWWWWWWW.....", ".....WWWWWWWWWW.....",
    "......PPPPPPPP......", "......P.PPPP.P......", "......PPPPPPPP......", ".....WPPPRRPPPW.....",
    ".....WWWWPPWWWW.....", ".....WWWWWWWWWW.....", ".....WWWRRRRWWW.....", ".....WWWWWWWWWW.....",
    "......WWWWWWWW......", ".......WWWWWW.......", "........WWWW........", ".........WW........."]
FLAKE = ["...W...", ".W.W.W.", "..WWW..", "WWWWWWW", "..WWW..", ".W.W.W.", "...W..."]


def main(cfg_path):
    cfg = json.load(open(cfg_path)); base = os.path.dirname(os.path.abspath(cfg_path))
    p = lambda x: x if os.path.isabs(x) else os.path.join(base, x)
    img0 = cv2.imread(p(cfg['frame'])).astype(np.float32) / 255.0
    COLS, ROWS = cfg.get('grid', [61, 20]); TW, TH = COLS * CELL, ROWS * CELL
    (ta, tb), (ba, bb) = cfg['top'], cfg['bottom']; X0, X1 = cfg.get('x_range', [-150, 1230])
    top = lambda x: ta + tb * x; bot = lambda x: ba + bb * x
    quad = np.float32([[X0, top(X0) + 3], [X1, top(X1) + 3], [X1, bot(X1) + 4], [X0, bot(X0) + 4]])
    Hm = cv2.getPerspectiveTransform(np.float32([[0, 0], [TW, 0], [TW, TH], [0, TH]]), quad)
    rnd = random.Random(7)
    sparks = [(rnd.randrange(COLS), rnd.randrange(ROWS), rnd.random() * 6.28) for _ in range(42)]
    flakes = [(4, 2, 'W'), (14, 9, 'C'), (23, 1, 'W'), (31, 10, 'W'), (39, 3, 'C'), (48, 11, 'W'), (55, 2, 'W'), (19, 16, 'C'), (44, 18, 'W')]
    oc = cfg.get('pattern_col', COLS // 2 - 7)

    def texture(t, mode):
        lit = {}
        if mode in ('snowman', 'santa'):
            art = SNOWMAN if mode == 'snowman' else SANTA
            off = oc if mode == 'snowman' else oc - 3
            for r, row in enumerate(art):
                for c, k in enumerate(row):
                    if k in C and r < ROWS: lit[(off + c, r)] = C[k]
        else:  # flakes: śnieżynki spadają w dół
            fall = t * 5.0
            for fx, fy, col in flakes:
                yy = int(fy + fall) % (ROWS + 7) - 7
                for r, row in enumerate(FLAKE):
                    for c, k in enumerate(row):
                        if k == 'W' and 0 <= yy + r < ROWS and 0 <= fx + c - 3 < COLS:
                            lit[(fx + c - 3, yy + r)] = C[col]
        img = np.zeros((TH, TW, 3), np.float32); img[:] = (60 / 255, 12 / 255, 8 / 255)  # granatowe tło (BGR)
        for r in range(ROWS):
            for c in range(COLS):
                cx, cy = c * CELL + CELL // 2, r * CELL + CELL // 2
                if (c, r) in lit:
                    rr, g, b = lit[(c, r)]
                    cv2.rectangle(img, (cx - 9, cy - 9), (cx + 9, cy + 9), (b / 255, g / 255, rr / 255), -1, cv2.LINE_AA)
                else:
                    cv2.circle(img, (cx, cy), 3, (1.0, 0.75, 0.55), -1, cv2.LINE_AA)
        for c, r, ph in sparks:
            if (c, r) in lit: continue
            a = 0.55 + 0.45 * math.sin(t * 7 + ph)
            cv2.circle(img, (c * CELL + CELL // 2, r * CELL + CELL // 2), 6, (a, a, a), -1, cv2.LINE_AA)
        return img

    mask = cv2.GaussianBlur(cv2.warpPerspective(np.ones((TH, TW), np.float32), Hm, (W, H)), (3, 3), 0)[..., None]
    snow = [(rnd.uniform(0, W), rnd.uniform(-H, H), rnd.uniform(1.5, 4.5), rnd.uniform(60, 160), rnd.random() * 6.28) for _ in range(160)]
    pats = cfg.get('patterns', [['snowman', 0.83], ['flakes', 1.37]])
    TOT = sum(d for _, d in pats); N = int(round(TOT * FPS)); Z = cfg.get('zoom', 0.05)
    zc = tuple(cfg.get('zoom_center', [540, 1080]))
    enc = subprocess.Popen(['ffmpeg', '-nostdin', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                            '-c:v', 'libx264', '-preset', 'fast', '-crf', '14', '-pix_fmt', 'yuv420p', p(cfg['out'])], stdin=subprocess.PIPE)
    for k in range(N):
        t = k / FPS; acc = 0.0; mode, tl = pats[-1][0], 0.0
        for m, d in pats:
            if t < acc + d: mode, tl = m, t - acc; break
            acc += d
        warped = cv2.warpPerspective(texture(tl, mode), Hm, (W, H), flags=cv2.INTER_AREA)
        fr = img0 * (1 - mask) + warped * mask
        bright = np.clip(warped * mask - 0.35, 0, 1)
        fr = fr + cv2.GaussianBlur(bright, (0, 0), 9) * 0.9 + cv2.GaussianBlur(bright, (0, 0), 30) * 0.5
        M = cv2.getRotationMatrix2D(zc, 0, 1.0 + Z * (k / max(1, N - 1)))
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        for x, y, rad, sp, ph in snow:
            yy = (y + sp * t) % (2 * H) - H * 0.5; xx = x + 18 * math.sin(t * 1.3 + ph)
            if 0 <= yy < H: cv2.circle(fr, (int(xx), int(yy)), int(rad), (0.92, 0.92, 0.95), -1, cv2.LINE_AA)
        enc.stdin.write((np.clip(fr, 0, 1) * 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    print('OK', p(cfg['out']), f'{TOT:.2f}s')


if __name__ == '__main__':
    main(sys.argv[1])
