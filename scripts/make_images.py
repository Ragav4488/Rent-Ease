"""Generate simple, flat-illustration property images for the RentEase demo.

No stock photos are downloaded — each card is drawn from primitives so the
repository stays self-contained and licence-free.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent.parent / "assets" / "properties"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 800, 500


def sky(draw, top, bottom):
    for y in range(H):
        t = y / H
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))


def windows(draw, x, y, cols, rows, ww, wh, gap, lit=(255, 226, 150), dark=(46, 64, 84),
            seed=1):
    for c in range(cols):
        for r in range(rows):
            x0 = x + c * (ww + gap)
            y0 = y + r * (wh + gap)
            on = ((c * 7 + r * 13 + seed * 3) % 4) != 0
            draw.rectangle([x0, y0, x0 + ww, y0 + wh], fill=lit if on else dark)


def apartment(path, base, accent, sky_top, sky_bottom, floors=6):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    sky(d, sky_top, sky_bottom)
    # distant blocks
    d.rectangle([40, 250, 170, 460], fill=(205, 214, 224))
    d.rectangle([640, 230, 780, 460], fill=(196, 206, 218))
    # main tower
    d.rectangle([230, 110, 570, 470], fill=base)
    d.rectangle([230, 110, 570, 132], fill=accent)
    windows(d, 262, 160, 4, 5, 54, 38, 22, seed=1)
    # entrance
    d.rectangle([365, 400, 435, 470], fill=(38, 50, 66))
    d.rectangle([380, 415, 420, 470], fill=(120, 190, 210))
    # ground
    d.rectangle([0, 460, W, H], fill=(110, 150, 120))
    d.rectangle([0, 468, W, H], fill=(96, 132, 106))
    img.save(OUT / path, quality=88)


def villa(path, base, accent, sky_top, sky_bottom):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    sky(d, sky_top, sky_bottom)
    # roof
    d.polygon([(180, 230), (400, 120), (620, 230)], fill=accent)
    # body
    d.rectangle([210, 230, 590, 440], fill=base)
    # door
    d.rectangle([370, 340, 430, 440], fill=(92, 62, 40))
    d.ellipse([418, 383, 426, 391], fill=(230, 200, 120))
    # windows
    for x0 in (245, 470):
        d.rectangle([x0, 260, x0 + 75, 320], fill=(196, 232, 245))
        d.rectangle([x0 - 5, 255, x0 + 80, 262], fill=(250, 250, 250))
    # garden
    d.rectangle([0, 440, W, H], fill=(104, 160, 112))
    for i in range(8):
        cx = 60 + i * 95
        d.ellipse([cx, 452, cx + 44, 496], fill=(72, 130, 88))
    d.rectangle([300, 430, 500, 450], fill=(180, 180, 180))
    img.save(OUT / path, quality=88)


def studio(path, base, accent, sky_top, sky_bottom):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    sky(d, sky_top, sky_bottom)
    d.rectangle([150, 190, 650, 460], fill=base)
    d.rectangle([150, 190, 650, 212], fill=accent)
    windows(d, 190, 240, 5, 2, 62, 46, 26, seed=4)
    d.rectangle([350, 370, 450, 460], fill=(38, 50, 66))
    d.rectangle([368, 385, 432, 460], fill=(150, 205, 225))
    # stylised AC units
    for x0 in (205, 545):
        d.rectangle([x0, 350, x0 + 60, 376], fill=(232, 236, 240))
    d.rectangle([0, 460, W, H], fill=(120, 120, 128))
    d.rectangle([0, 460, W, 472], fill=(96, 96, 104))
    img.save(OUT / path, quality=88)


def pg(path, base, accent, sky_top, sky_bottom):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    sky(d, sky_top, sky_bottom)
    d.rectangle([120, 150, 680, 470], fill=base)
    d.rectangle([120, 150, 680, 172], fill=accent)
    windows(d, 160, 210, 6, 3, 58, 42, 24, seed=9)
    d.rectangle([360, 400, 440, 470], fill=(38, 50, 66))
    d.rectangle([0, 470, W, H], fill=(128, 140, 120))
    # gate + signpost
    d.rectangle([90, 300, 112, 470], fill=(120, 130, 140))
    d.rectangle([688, 300, 710, 470], fill=(120, 130, 140))
    img.save(OUT / path, quality=88)


def house(path, base, accent, sky_top, sky_bottom):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    sky(d, sky_top, sky_bottom)
    d.polygon([(200, 250), (400, 150), (600, 250)], fill=accent)
    d.rectangle([230, 250, 570, 440], fill=base)
    d.rectangle([370, 350, 430, 440], fill=(96, 66, 44))
    d.rectangle([265, 280, 335, 330], fill=(200, 234, 246))
    d.rectangle([465, 280, 535, 330], fill=(200, 234, 246))
    # terrace railing
    d.rectangle([230, 238, 570, 252], fill=accent)
    for x0 in range(240, 566, 26):
        d.rectangle([x0, 214, x0 + 6, 240], fill=accent)
    d.rectangle([0, 440, W, H], fill=(112, 158, 116))
    img.save(OUT / path, quality=88)


def kitchen(path, base, accent):
    img = Image.new("RGB", (W, H), (242, 236, 226))
    d = ImageDraw.Draw(img)
    # wall tiles
    for y in range(0, 230, 40):
        for x in range(0, W, 40):
            d.rectangle([x, y, x + 38, y + 38], fill=(250, 246, 238), outline=(232, 224, 210))
    d.rectangle([0, 230, W, 300], fill=base)
    d.rectangle([0, 300, W, H], fill=(236, 230, 218))
    # counter
    d.rectangle([60, 236, 740, 258], fill=accent)
    d.rectangle([60, 258, 740, 330], fill=(228, 232, 236))
    # cabinets
    for x0 in range(70, 730, 120):
        d.rectangle([x0, 336, x0 + 110, 424], fill=base)
        d.rectangle([x0 + 8, 344, x0 + 102, 416], fill=accent)
    # sink + tap
    d.rectangle([300, 268, 420, 322], fill=(196, 202, 210))
    d.rectangle([350, 236, 360, 272], fill=(120, 128, 138))
    d.line([(355, 240), (392, 240), (392, 268)], fill=(120, 128, 138), width=6)
    # hob
    d.rectangle([500, 262, 650, 328], fill=(60, 64, 72))
    for cx in (540, 610):
        d.ellipse([cx - 22, 276, cx + 22, 314], fill=(90, 94, 104))
    img.save(OUT / path, quality=88)


def bedroom(path, base, accent):
    img = Image.new("RGB", (W, H), (246, 243, 238))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 330], fill=base)
    d.rectangle([0, 330, W, H], fill=(214, 198, 176))
    # window
    d.rectangle([470, 60, 700, 250], fill=(196, 230, 240))
    d.rectangle([470, 60, 700, 250], outline=(250, 250, 250), width=10)
    d.line([(585, 60), (585, 250)], fill=(250, 250, 250), width=10)
    # bed
    d.rectangle([90, 260, 430, 430], fill=accent)
    d.rectangle([105, 236, 415, 330], fill=(250, 250, 252))
    d.rectangle([120, 246, 245, 292], fill=(226, 232, 240))
    d.rectangle([260, 246, 385, 292], fill=(226, 232, 240))
    # headboard
    d.rectangle([90, 200, 430, 262], fill=(120, 96, 74))
    # rug
    d.ellipse([150, 420, 520, 486], fill=(206, 214, 222))
    img.save(OUT / path, quality=88)


def balcony(path, sky_top, sky_bottom):
    img = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(img)
    sky(d, sky_top, sky_bottom)
    # sea
    d.rectangle([0, 330, W, 430], fill=(58, 132, 168))
    for i in range(9):
        y = 340 + i * 10
        d.line([(0, y), (W, y + 4)], fill=(78, 156, 190), width=3)
    d.rectangle([0, 430, W, H], fill=(206, 176, 132))
    # railing
    d.rectangle([0, 300, W, 316], fill=(236, 240, 244))
    for x0 in range(10, W, 46):
        d.rectangle([x0, 300, x0 + 10, 430], fill=(236, 240, 244))
    # plants
    for cx in (90, 700):
        d.rectangle([cx - 30, 360, cx + 30, 432], fill=(176, 124, 88))
        for k in range(5):
            d.ellipse([cx - 40 + k * 8, 300 + k * 6, cx + 34 - k * 4, 366], fill=(64, 140, 96))
    img.save(OUT / path, quality=88)


if __name__ == "__main__":
    apartment("peelamedu-2bhk.jpg", (222, 208, 190), (150, 110, 84),
              (150, 200, 232), (222, 238, 246))
    apartment("velachery-3bhk.jpg", (208, 216, 226), (96, 118, 140),
              (120, 178, 220), (208, 230, 244), floors=7)
    villa("villa-3bhk.jpg", (240, 232, 216), (158, 92, 74),
          (128, 186, 226), (216, 236, 246))
    studio("studio-gandhipuram.jpg", (232, 222, 208), (120, 132, 146),
           (146, 196, 226), (224, 240, 246))
    pg("pg-guindy.jpg", (226, 214, 198), (154, 112, 82),
       (138, 190, 224), (220, 238, 246))
    house("saibaba-1bhk.jpg", (238, 228, 210), (140, 96, 76),
          (134, 188, 224), (218, 238, 246))
    house("vadavalli-2bhk.jpg", (230, 222, 206), (110, 126, 96),
          (118, 178, 222), (212, 234, 244))
    apartment("besant-2bhk.jpg", (228, 224, 216), (88, 124, 148),
              (108, 170, 216), (200, 228, 244), floors=5)
    kitchen("peelamedu-kitchen.jpg", (156, 128, 104), (232, 236, 240))
    bedroom("saibaba-bedroom.jpg", (214, 224, 234), (146, 170, 196))
    balcony("besant-balcony.jpg", (110, 172, 216), (204, 230, 244))
    print("generated:", len(list(OUT.glob('*.jpg'))), "images in", OUT)
