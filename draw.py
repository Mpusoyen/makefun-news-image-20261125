#!/usr/bin/env python3
"""The Wednesday Record — news-image-20261125 v2. Deterministic PIL rendering."""
import math, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (16, 32, 56); NAVY2 = (26, 48, 80); CREAM = (250, 246, 236)
INK = (18, 18, 18); RED = (178, 38, 30); RED_LT = (255, 130, 110)
GOLD = (192, 138, 43); GREY = (105, 100, 92); LGREY = (214, 208, 196)
WHITE = (255, 255, 255); CARD = (255, 253, 247); SKY = (198, 216, 232)
GREEN = (30, 110, 60); BLUE = (30, 80, 170)

FD = "/usr/share/fonts/truetype/dejavu/"
FL = "/usr/share/fonts/truetype/liberation/"
def F(name, size):
    p = FD + name if name.startswith("DejaVu") else FL + name
    return ImageFont.truetype(p, size)
def serif(sz): return F("DejaVuSerif.ttf", sz)
def serifB(sz): return F("DejaVuSerif-Bold.ttf", sz)
def sans(sz): return F("DejaVuSans.ttf", sz)
def sansB(sz): return F("DejaVuSans-Bold.ttf", sz)
def ital(sz): return F("LiberationSerif-Italic.ttf", sz)

img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
rng = random.Random(20261125)

def tw(t, f): return d.textlength(t, font=f)
def fit(t, f, maxw):
    if tw(t, f) <= maxw: return t
    while t and tw(t + "…", f) > maxw: t = t[:-1]
    return t + "…"
def wrap(t, f, maxw, maxlines=99):
    words, lines, cur = t.split(), [], ""
    for w_ in words:
        s = (cur + " " + w_).strip()
        if tw(s, f) <= maxw or not cur: cur = s
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines[:maxlines]
def disc(cx, cy, r, n, fill=RED, txt=WHITE, fsz=11):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    f = sansB(fsz); s = str(n)
    d.text((cx - tw(s, f) / 2, cy - fsz * 0.62), s, font=f, fill=txt)
CHIP = {"CONFIRMED": (NAVY, WHITE), "OFFICIAL": (BLUE, WHITE),
        "REPORTED": (GOLD, INK), "CLAIM": (RED, WHITE)}
def chip(x, y, name, fsz=8):
    f = sansB(fsz); w_ = tw(name, f) + 10
    bg, fg = CHIP[name]
    d.rounded_rectangle([x, y, x + w_, y + fsz + 6], 3, fill=bg)
    d.text((x + 5, y + 3), name, font=f, fill=fg)
    return w_

# ============ 1. MASTHEAD (0-110) ============
d.rectangle([0, 0, W, 110], fill=NAVY)
f = serifB(28); t = "THE WEDNESDAY RECORD"
d.text(((W - tw(t, f)) / 2, 3), t, font=f, fill=CREAM)
f = sansB(11); t = "34 STORIES  ·  8 REGIONS  ·  15 FIELDS  ·  EVERY ONE DATED WEDNESDAY"
d.text(((W - tw(t, f)) / 2, 35), t, font=f, fill=GOLD)
f = serifB(34); t = "Wednesday 25 November 2026"
d.text(((W - tw(t, f)) / 2, 48), t, font=f, fill=WHITE)
f = ital(12); t = "700,000 Russian dead, war analysis finds  ·  Gaza toll reaches 74,746  ·  CIA and spy chief's office breached"
t = fit(t, f, W - 30)
d.text(((W - tw(t, f)) / 2, 93), t, font=f, fill=RED_LT)

# ============ 2. DAY IN NUMBERS (110-158) ============
d.text((10, 112), "THE DAY IN NUMBERS", font=sansB(9), fill=RED)
stats = [("700,000+", "Russian soldiers killed — war analysis"),
         ("74,746", "dead in Gaza — WAFA toll"),
         ("266M", "face acute hunger — WFP"),
         ("204", "runs off 53 balls — Sooryavanshi, 15"),
         ("31", "ancient quasars — Euclid"),
         ("₹32,266 CR", "Tata Steel bid for APL Apollo")]
sw = (W - 20) / 6
for i, (v, lab) in enumerate(stats):
    x = 10 + i * sw
    if i: d.line([x - 4, 124, x - 4, 152], fill=LGREY)
    d.text((x, 122), v, font=serifB(15), fill=NAVY)
    for j, ln in enumerate(wrap(lab, sans(7.5), sw - 18, 2)):
        d.text((x, 139 + j * 8), ln, font=sans(7.5), fill=GREY)

# ============ STORY DATA ============
# n, place, region, field, chip, headline, summary, source, lon, lat, scene
S = [
 (1,"KYIV, UKRAINE","EUROPE","WAR","REPORTED","700,000+ Russian soldiers killed, analysis finds","A new analysis puts Russian military deaths in the nearly five-year war above 700,000 — a staggering toll on both sides.","RFE/RL",30.5,50.4,"field"),
 (2,"GAZA CITY","MIDDLE EAST","WAR","REPORTED","Gaza death toll reaches 74,746","The toll climbs as strikes continue; Oxfam finds pollution risks across more than 99% of the Strip, its survey says.","WAFA · Oxfam",34.5,31.5,"rubble"),
 (3,"WASHINGTON, USA","NORTH AMERICA","SECURITY","REPORTED","CIA and spy chief's office hit by breach","The CIA and the Office of the Director of National Intelligence suffer a breach of unclassified systems, sources say.","CNN · Reuters",-77.0,38.9,"agency"),
 (4,"ADEN, YEMEN","MIDDLE EAST","CONFLICT","CLAIM","Houthis press toward Aden; army says city will hold","Yemen's Houthis push to within 60 km of the temporary capital, vowing to attack; government forces say: it will not happen.","Reuters",45.0,12.8,"coast"),
 (5,"STRAIT OF HORMUZ","MIDDLE EAST","ENERGY","CLAIM","Iran claims three tankers hit by naval mines","Iran's Revolutionary Guard Navy says three oil tankers were hit by mines in the strait, raising shipping fears.","Reuters",56.5,26.5,"strait"),
 (6,"WASHINGTON, USA","NORTH AMERICA","SECURITY","REPORTED","Trump team debates strikes on Iran's leaders","The administration debates targeted strikes on Iran's leadership, NBC reports, as Tehran sets conditions for talks.","NBC",-77.0,38.9,"sitroom"),
 (7,"WARSAW, POLAND","EUROPE","DEFENCE","REPORTED","NATO plans early-warning jets for Poland","The alliance plans to deploy early-warning aircraft after missiles landed in Poland during an attack on Ukraine.","Reuters",21.0,52.2,"awacs"),
 (8,"ITURI, DR CONGO","AFRICA","HEALTH","OFFICIAL","WHO evacuates Ebola hospital staff after siege","Health workers leave the Akwe hospital after sheltering there for three days amid fierce fighting, the WHO says.","WHO · Tedros",29.5,1.5,"hospital"),
 (9,"MUMBAI, INDIA","SOUTH ASIA","BUSINESS","CONFIRMED","Tata Steel bids ₹32,266 crore for APL Apollo","Tata Steel proposes buying a 52.38% stake in APL Apollo Tubes, the morning's biggest Indian deal by value.","Hindu BusinessLine",72.8,19.1,"steel"),
 (10,"SINGAPORE","EAST ASIA","TECH","OFFICIAL","US blacklists Megaspeed over Nvidia chip diversion","Washington restricts the Singapore firm, saying it sits at the centre of AI-chip smuggling to China.","Reuters",103.8,1.35,"port"),
 (11,"DARMSTADT, GERMANY","EUROPE","SCIENCE","CONFIRMED","Euclid telescope finds 31 ancient quasars","ESA's Euclid spots 31 quasars from the early universe, the oldest pair dating to 670 million years after the Big Bang.","ESA · Sci.News",8.65,49.87,"space"),
 (12,"RAJKOT, INDIA","SOUTH ASIA","SPORT","CONFIRMED","15-year-old smashes 204 off 53 balls","Vaibhav Sooryavanshi hits the fastest List A double hundred ever, clearing the ropes 15 times in a record-shattering innings.","The Hindu · BBC",70.8,22.3,"stadium"),
 (13,"CAPE CANAVERAL, USA","NORTH AMERICA","SPACE","CONFIRMED","Cygnus XL cargo ship readied for space station","NASA and Northrop Grumman target 29 November for the CRS-25 cargo launch, carrying about 4,990 kg to the ISS.","NASA",-80.6,28.4,"launchpad"),
]

# ============ SCENES ============
def clip_box(x, y, w_, h_):
    return (x, y, x + w_, y + h_)
def scene_field(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_ * 0.45], fill=(168, 178, 186))
    d.rectangle([x, y + h_ * 0.45, x + w_, y + h_], fill=(122, 128, 84))
    hz = y + h_ * 0.45
    pts = []
    for i in range(9):
        px = x + 8 + i * (w_ - 16) / 8
        pts.append((px, hz + 8 if i % 2 else hz + 16))
    d.line(pts, fill=(70, 60, 40), width=2)
    for r in range(3):
        yy = hz + 14 + r * (h_ * 0.16); n = 6 + r * 3
        for i in range(n):
            px = x + 12 + i * (w_ - 24) / max(n - 1, 1) + r * 4; s = 2 + r
            d.line([px, yy, px, yy + 3 + r], fill=(230, 228, 220), width=1)
            d.line([px - s, yy + 1, px + s, yy + 1], fill=(230, 228, 220), width=1)
    for sx in (x + w_ * 0.25, x + w_ * 0.72):
        for k in range(4):
            d.ellipse([sx - 3 - k * 2, y + 4 + k * 5, sx + 5 + k * 3, y + 12 + k * 5], fill=(105, 105, 105))
    f = serifB(26); t = "700,000+"
    d.rectangle([x + w_ - tw(t, f) - 16, y + h_ - 36, x + w_ - 6, y + h_ - 6], fill=NAVY)
    d.text((x + w_ - tw(t, f) - 11, y + h_ - 33), t, font=f, fill=WHITE)
def scene_rubble(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(216, 200, 178))
    d.ellipse([x + w_ * 0.78, y + 5, x + w_ * 0.78 + 16, y + 21], fill=(240, 214, 150))
    d.rectangle([x + 8, y + h_ * 0.3, x + 34, y + h_ * 0.85], fill=(140, 132, 120))
    d.polygon([(x + 40, y + h_ * 0.35), (x + 66, y + h_ * 0.42), (x + 60, y + h_ * 0.88), (x + 38, y + h_ * 0.88)], fill=(120, 112, 100))
    d.rectangle([x + 74, y + h_ * 0.45, x + 96, y + h_ * 0.85], fill=(150, 142, 128))
    for bx, by, bw in ((12, 0.42, 18), (46, 0.55, 14), (78, 0.58, 14)):
        d.rectangle([x + bx, y + h_ * by, x + bx + bw, y + h_ * by + 5], fill=(90, 84, 74))
    for i in range(7):
        px = x + 10 + i * (w_ - 30) / 6
        d.polygon([(px, y + h_), (px + 8, y + h_ * 0.82), (px + 16, y + h_)], fill=(105, 98, 88))
    for sx in (x + 20, x + 55):
        for k in range(3):
            d.ellipse([sx - k * 2, y + 2 + k * 6, sx + 8 + k * 3, y + 9 + k * 6], fill=(130, 128, 124))
def scene_agency(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=SKY)
    d.rectangle([x, y + h_ - 8, x + w_, y + h_], fill=(110, 130, 100))
    bx, bw = x + w_ * 0.28, w_ * 0.44
    d.rectangle([bx, y + h_ * 0.38, bx + bw, y + h_ - 8], fill=(226, 222, 210))
    d.polygon([(bx - 4, y + h_ * 0.38), (bx + bw + 4, y + h_ * 0.38), (bx + bw / 2, y + h_ * 0.2)], fill=NAVY)
    d.arc([bx + bw / 2 - 9, y + h_ * 0.08, bx + bw / 2 + 9, y + h_ * 0.26], 180, 360, fill=NAVY, width=3)
    for i in range(4):
        cx = bx + 5 + i * (bw - 10) / 3
        d.rectangle([cx - 2, y + h_ * 0.42, cx + 2, y + h_ - 10], fill=(180, 176, 164))
    sx, sy = x + w_ * 0.85, y + h_ * 0.52
    d.polygon([(sx, sy - 13), (sx + 11, sy - 8), (sx + 11, sy + 5), (sx, sy + 14), (sx - 11, sy + 5), (sx - 11, sy - 8)], fill=GOLD, outline=INK)
    d.ellipse([sx - 3.5, sy - 6, sx + 3.5, sy + 1], outline=INK, width=2)
    d.line([sx, sy + 1, sx, sy + 7], fill=INK, width=2)
    d.line([x + w_ * 0.8, y + 6, x + w_ * 0.92, y + 14, x + w_ * 0.97, y + 26], fill=RED, width=2)
    for px, py in ((0.84, 10), (0.93, 18), (0.9, 30)):
        d.ellipse([x + w_ * px - 2, y + py - 2, x + w_ * px + 2, y + py + 2], fill=RED)
def scene_coast(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_ * 0.62], fill=SKY)
    d.rectangle([x, y + h_ * 0.62, x + w_, y + h_], fill=(70, 120, 165))
    for i in range(5):
        d.line([x + 6 + i * 20, y + h_ * 0.72, x + 18 + i * 20, y + h_ * 0.72], fill=(150, 195, 220), width=1)
    d.polygon([(x, y + h_ * 0.62), (x + w_ * 0.4, y + h_ * 0.4), (x + w_, y + h_ * 0.5), (x + w_, y + h_ * 0.62)], fill=(196, 178, 138))
    for i, bh in enumerate((10, 14, 8, 12)):
        bx = x + w_ * 0.55 + i * 13
        d.rectangle([bx, y + h_ * 0.62 - bh, bx + 9, y + h_ * 0.62], fill=(90, 88, 84))
    for cx_ in (x + w_ * 0.48, x + w_ * 0.86):
        d.line([cx_, y + h_ * 0.62, cx_, y + h_ * 0.3], fill=(60, 60, 60), width=2)
        d.line([cx_, y + h_ * 0.3, cx_ + 14, y + h_ * 0.3], fill=(60, 60, 60), width=2)
        d.line([cx_ + 12, y + h_ * 0.3, cx_ + 12, y + h_ * 0.42], fill=(60, 60, 60), width=1)
    fx, fy = x + w_ * 0.2, y + h_ * 0.34
    d.line([fx, fy, fx, fy + 16], fill=INK, width=2)
    d.polygon([(fx, fy), (fx + 13, fy + 3), (fx, fy + 7)], fill=RED)
    for t_ in (0.25, 0.5, 0.75):
        px = x + w_ * 0.22 + (w_ * 0.3) * t_; py = y + h_ * 0.5 - 6 * math.sin(t_ * math.pi)
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.polygon([(x + w_ * 0.55, y + h_ * 0.44), (x + w_ * 0.5, y + h_ * 0.5), (x + w_ * 0.6, y + h_ * 0.5)], fill=RED)
def scene_strait(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(80, 135, 180))
    d.polygon([(x, y), (x + w_ * 0.22, y), (x + w_ * 0.1, y + h_ * 0.55), (x, y + h_ * 0.7)], fill=(150, 128, 92))
    d.polygon([(x + w_, y), (x + w_ * 0.8, y), (x + w_ * 0.92, y + h_ * 0.5), (x + w_, y + h_ * 0.65)], fill=(150, 128, 92))
    def tanker(tx, ty, s):
        d.polygon([(tx, ty), (tx + 70 * s, ty), (tx + 62 * s, ty + 9 * s), (tx + 8 * s, ty + 9 * s)], fill=(60, 60, 66))
        d.rectangle([tx + 8 * s, ty - 6 * s, tx + 50 * s, ty], fill=(150, 60, 45))
        for i in range(3):
            d.ellipse([tx + (12 + i * 13) * s, ty - 7 * s, tx + (21 + i * 13) * s, ty - 2 * s], fill=(110, 45, 35))
        d.rectangle([tx + 54 * s, ty - 13 * s, tx + 64 * s, ty], fill=(225, 222, 214))
    tanker(x + w_ * 0.2, y + h_ * 0.5, 1.0)
    tanker(x + w_ * 0.55, y + h_ * 0.26, 0.55)
    for mx, my in ((0.35, 0.78), (0.55, 0.85), (0.72, 0.75)):
        cx, cy = x + w_ * mx, y + h_ * my
        d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(35, 35, 40))
        for a in range(0, 360, 45):
            d.line([cx, cy, cx + 8 * math.cos(math.radians(a)), cy + 8 * math.sin(math.radians(a))], fill=(35, 35, 40), width=1)
def scene_sitroom(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(52, 48, 60))
    d.rectangle([x + w_ * 0.3, y + 4, x + w_ * 0.72, y + h_ * 0.52], fill=(30, 70, 90))
    d.ellipse([x + w_ * 0.45, y + h_ * 0.16, x + w_ * 0.58, y + h_ * 0.34], outline=RED_LT, width=2)
    d.ellipse([x + w_ * 0.48, y + h_ * 0.2, x + w_ * 0.55, y + h_ * 0.3], outline=RED_LT, width=1)
    d.line([x + w_ * 0.34, y + h_ * 0.4, x + w_ * 0.68, y + h_ * 0.12], fill=(120, 180, 200), width=1)
    d.polygon([(x + w_ * 0.2, y + h_), (x + w_ * 0.34, y + h_ * 0.62), (x + w_ * 0.68, y + h_ * 0.62), (x + w_ * 0.86, y + h_)], fill=(110, 80, 50))
    for t_ in (0.15, 0.4, 0.62, 0.85):
        px = x + w_ * (0.24 + 0.55 * t_)
        d.ellipse([px - 3, y + h_ * 0.66 - 3, px + 3, y + h_ * 0.66 + 3], fill=(230, 200, 170))
    for fx, col in ((x + 8, (60, 90, 170)), (x + w_ - 16, RED)):
        d.rectangle([fx, y + 8, fx + 9, y + 20], fill=col)
        d.line([fx, y + 8, fx, y + 30], fill=(200, 200, 200), width=1)
def scene_awacs(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=SKY)
    d.rectangle([x, y + h_ - 7, x + w_, y + h_], fill=(70, 100, 60))
    for i in range(8):
        px = x + 6 + i * (w_ - 12) / 7
        d.polygon([(px, y + h_ - 6), (px + 3, y + h_ - 16), (px + 6, y + h_ - 6)], fill=(45, 80, 45))
    cx, cy = x + w_ * 0.48, y + h_ * 0.44
    d.ellipse([cx - 34, cy - 6, cx + 34, cy + 7], fill=(228, 230, 234), outline=(120, 124, 130))
    d.polygon([(cx - 30, cy - 2), (cx - 44, cy - 13), (cx - 40, cy + 2), (cx - 28, cy + 3)], fill=(200, 204, 210))
    d.polygon([(cx + 28, cy - 3), (cx + 40, cy - 14), (cx + 42, cy - 2), (cx + 32, cy + 3)], fill=(200, 204, 210))
    d.ellipse([cx - 13, cy - 17, cx + 13, cy - 8], fill=(240, 240, 244), outline=(120, 124, 130))
    d.line([cx - 3, cy - 8, cx - 3, cy - 3], fill=(120, 124, 130), width=2)
    d.line([cx + 3, cy - 8, cx + 3, cy - 3], fill=(120, 124, 130), width=2)
    for r in (18, 27, 36):
        d.arc([cx - r, cy - 14 - r * 0.55, cx + r, cy - 14 + r * 0.55], 200, 340, fill=(60, 110, 190), width=1)
    jx, jy = x + w_ * 0.85, y + h_ * 0.2
    d.polygon([(jx - 9, jy), (jx + 9, jy - 2), (jx + 4, jy + 3), (jx - 6, jy + 3)], fill=(170, 176, 184))
def scene_hospital(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(205, 226, 205))
    d.rectangle([x, y + h_ - 8, x + w_, y + h_], fill=(120, 140, 95))
    bx = x + w_ * 0.1
    d.rectangle([bx, y + h_ * 0.25, bx + w_ * 0.42, y + h_ - 8], fill=(240, 238, 232))
    d.rectangle([bx, y + h_ * 0.25, bx + w_ * 0.42, y + h_ * 0.36], fill=(210, 208, 200))
    ccx, ccy = bx + w_ * 0.21, y + h_ * 0.52
    d.rectangle([ccx - 3, ccy - 9, ccx + 3, ccy + 9], fill=RED)
    d.rectangle([ccx - 9, ccy - 3, ccx + 9, ccy + 3], fill=RED)
    for i in range(3):
        d.rectangle([bx + 6 + i * 16, y + h_ * 0.68, bx + 14 + i * 16, y + h_ * 0.8], fill=(150, 170, 185))
    ax, ay = x + w_ * 0.6, y + h_ * 0.68
    d.rectangle([ax, ay, ax + 34, ay + 13], fill=WHITE, outline=(150, 150, 150))
    d.rectangle([ax + 24, ay + 2, ax + 34, ay + 9], fill=(160, 190, 210))
    d.rectangle([ax + 13, ay + 3, ax + 19, ay + 10], fill=RED)
    d.rectangle([ax + 15, ay + 1.5, ax + 17, ay + 11.5], fill=RED)
    for wx in (ax + 7, ax + 27):
        d.ellipse([wx - 3.5, ay + 11, wx + 3.5, ay + 18], fill=(40, 40, 40))
    hx, hy = x + w_ * 0.72, y + h_ * 0.2
    d.ellipse([hx - 11, hy - 4, hx + 11, hy + 5], fill=(225, 160, 40))
    d.line([hx - 18, hy - 8, hx + 18, hy - 8], fill=INK, width=2)
    d.line([hx + 11, hy, hx + 19, hy - 3], fill=INK, width=2)
    for tx_ in (x + w_ * 0.92,):
        d.polygon([(tx_ - 6, y + h_ - 8), (tx_, y + h_ * 0.4), (tx_ + 6, y + h_ - 8)], fill=(50, 95, 50))
def scene_steel(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(225, 205, 185))
    d.rectangle([x, y + h_ - 9, x + w_, y + h_], fill=(90, 82, 76))
    fx = x + w_ * 0.16
    d.polygon([(fx, y + h_ - 9), (fx + 8, y + h_ * 0.3), (fx + 22, y + h_ * 0.3), (fx + 30, y + h_ - 9)], fill=(105, 100, 98))
    d.rectangle([fx + 9, y + h_ * 0.22, fx + 21, y + h_ * 0.32], fill=(70, 66, 64))
    for i, cx_ in enumerate((x + w_ * 0.52, x + w_ * 0.66)):
        d.rectangle([cx_ - 4, y + h_ * 0.18, cx_ + 4, y + h_ - 9], fill=(120, 114, 108))
        for k in range(3):
            d.ellipse([cx_ - 4 - k * 2, y + 2 + k * 5, cx_ + 6 + k * 3, y + 9 + k * 5], fill=(150, 148, 144))
    d.polygon([(fx + 30, y + h_ * 0.62), (x + w_ * 0.44, y + h_ * 0.78), (x + w_ * 0.44, y + h_ * 0.86), (fx + 28, y + h_ * 0.74)], fill=(255, 130, 30))
    for i in range(6):
        sx = x + w_ * 0.4 + rng.random() * 8; sy = y + h_ * 0.6 + rng.random() * 10
        d.ellipse([sx, sy, sx + 1.6, sy + 1.6], fill=(255, 190, 60))
    for i, gx in enumerate((x + w_ * 0.6, x + w_ * 0.74, x + w_ * 0.87)):
        gy = y + h_ - 20
        d.ellipse([gx, gy, gx + 17, gy + 17], fill=GOLD, outline=(150, 105, 25), width=1)
        f = sansB(11); d.text((gx + 4.5, gy + 2.5), "₹", font=f, fill=(90, 60, 10))
def scene_port(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_ * 0.7], fill=SKY)
    d.rectangle([x, y + h_ * 0.7, x + w_, y + h_], fill=(95, 110, 120))
    cols = [(200, 70, 50), (50, 110, 180), (60, 160, 90), (230, 160, 40)]
    for r in range(2):
        for i in range(4):
            bx = x + 6 + i * 24; by = y + h_ * 0.7 - 12 - r * 11
            d.rectangle([bx, by, bx + 21, by + 10], fill=cols[(i + r) % 4], outline=(60, 60, 60))
    for cx_ in (x + w_ * 0.35, x + w_ * 0.7):
        d.line([cx_, y + h_ * 0.7, cx_, y + 5], fill=(50, 55, 60), width=2)
        d.line([cx_, y + 5, cx_ + 22, y + 5], fill=(50, 55, 60), width=2)
        d.line([cx_ + 18, y + 5, cx_ + 18, y + h_ * 0.3], fill=(50, 55, 60), width=1)
    mx, my = x + w_ * 0.55, y + h_ * 0.34
    d.rectangle([mx, my, mx + 22, my + 15], fill=(40, 44, 52), outline=GOLD, width=1)
    for i in range(3):
        d.line([mx - 3, my + 3 + i * 5, mx, my + 3 + i * 5], fill=GOLD, width=1)
        d.line([mx + 22, my + 3 + i * 5, mx + 25, my + 3 + i * 5], fill=GOLD, width=1)
    d.rectangle([mx + 6, my + 4, mx + 16, my + 11], fill=(90, 200, 120))
    d.polygon([(x + w_ * 0.78, y + h_), (x + w_ * 0.8, y + h_ * 0.8), (x + w_, y + h_ * 0.8), (x + w_, y + h_)], fill=(55, 60, 66))
def scene_space(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=(10, 12, 34))
    for i in range(40):
        sx = x + rng.random() * w_; sy = y + rng.random() * h_
        d.ellipse([sx, sy, sx + 1.4, sy + 1.4], fill=(220, 225, 255))
    d.arc([x - w_ * 0.3, y + h_ * 0.62, x + w_ * 0.45, y + h_ * 1.5], 200, 320, fill=(90, 150, 220), width=6)
    tx, ty = x + w_ * 0.3, y + h_ * 0.42
    d.rectangle([tx, ty - 5, tx + 26, ty + 5], fill=(200, 204, 212))
    d.ellipse([tx + 26, ty - 8, tx + 38, ty + 8], fill=(225, 228, 234), outline=(140, 144, 150))
    d.polygon([(tx - 16, ty - 9), (tx, ty - 3), (tx, ty + 3), (tx - 16, ty + 9)], fill=(60, 90, 180))
    for qx, qy, qr, col in ((0.68, 0.22, 8, (255, 190, 90)), (0.85, 0.5, 6, (170, 200, 255)), (0.6, 0.72, 5, (255, 150, 170))):
        cx, cy = x + w_ * qx, y + h_ * qy
        for r in range(qr, 1, -3):
            d.arc([cx - r, cy - r * 0.55, cx + r, cy + r * 0.55], 20, 300, fill=col, width=1)
        d.ellipse([cx - 1.8, cy - 1.8, cx + 1.8, cy + 1.8], fill=WHITE)
def scene_stadium(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_ * 0.55], fill=(40, 45, 70))
    d.rectangle([x, y + h_ * 0.55, x + w_, y + h_], fill=(60, 140, 70))
    for r in range(3):
        for i in range(16):
            px = x + 4 + i * (w_ - 8) / 15; py = y + 4 + r * 6
            d.ellipse([px, py, px + 2.4, py + 2.4], fill=[(230, 120, 110), (240, 220, 160), (150, 190, 240)][(i + r) % 3])
    for px in (x + 8, x + w_ - 12):
        d.line([px + 2, y + h_ * 0.55, px + 2, y + 8], fill=(200, 200, 205), width=2)
        for k in range(3):
            d.ellipse([px + k * 3 - 1, y + 5, px + k * 3 + 2, y + 8], fill=(255, 250, 200))
    bx, by = x + w_ * 0.42, y + h_ * 0.68
    d.line([bx, by + 12, bx + 3, by + 2], fill=INK, width=3)
    d.line([bx + 3, by + 2, bx + 13, by - 4], fill=INK, width=3)
    d.line([bx + 3, by + 2, bx - 2, by + 12], fill=INK, width=3)
    d.ellipse([bx + 1, by - 8, bx + 7, by - 2], fill=(235, 195, 160))
    d.line([bx + 12, by - 4, bx + 20, by - 12], fill=(150, 110, 60), width=2)
    for sx in (bx - 12, bx - 8):
        d.rectangle([sx, by + 8, sx + 2, by + 16], fill=(240, 220, 120))
    pts = [(bx + 22 + i * 3, by - 13 - int(7 * math.sin(i / 5))) for i in range(7)]
    d.line(pts, fill=WHITE, width=1)
    ex, ey = pts[-1]; d.ellipse([ex - 2.4, ey - 2.4, ex + 2.4, ey + 2.4], fill=(235, 235, 235), outline=RED)
    d.rectangle([x + w_ - 40, y + h_ * 0.6, x + w_ - 6, y + h_ * 0.6 + 17], fill=NAVY)
    f = serifB(12); d.text((x + w_ - 34, y + h_ * 0.6 + 2), "204", font=f, fill=WHITE)
def scene_launchpad(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_ * 0.8], fill=SKY)
    d.rectangle([x, y + h_ * 0.8, x + w_, y + h_], fill=(80, 140, 180))
    d.rectangle([x, y + h_ * 0.74, x + w_ * 0.72, y + h_ * 0.82], fill=(150, 148, 140))
    rx = x + w_ * 0.42
    d.rectangle([rx, y + h_ * 0.18, rx + 13, y + h_ * 0.74], fill=(235, 236, 240), outline=(150, 152, 158))
    d.polygon([(rx, y + h_ * 0.18), (rx + 6.5, y + 2), (rx + 13, y + h_ * 0.18)], fill=(235, 236, 240), outline=(150, 152, 158))
    d.rectangle([rx + 2, y + h_ * 0.4, rx + 11, y + h_ * 0.52], fill=(60, 65, 75))
    d.text((rx + 3.2, y + h_ * 0.24), "XL", font=sansB(7), fill=NAVY)
    gx = rx + 18
    d.rectangle([gx, y + h_ * 0.1, gx + 6, y + h_ * 0.74], fill=(120, 90, 70))
    for k in range(4):
        d.line([gx, y + h_ * (0.16 + k * 0.15), gx + 6, y + h_ * (0.24 + k * 0.15)], fill=(120, 90, 70), width=1)
    d.line([gx, y + h_ * 0.3, rx + 13, y + h_ * 0.32], fill=(90, 70, 55), width=2)
    d.line([gx, y + h_ * 0.55, rx + 13, y + h_ * 0.56], fill=(90, 70, 55), width=2)
    d.polygon([(rx + 1, y + h_ * 0.74), (rx + 6.5, y + h_ * 0.92), (rx + 12, y + h_ * 0.74)], fill=(255, 150, 40))
    for i in range(6):
        sx = rx - 8 + i * 6; sy = y + h_ * 0.78 + (i % 2) * 3
        d.ellipse([sx, sy, sx + 10, sy + 6], fill=(235, 235, 238))
SCENES = {"field": scene_field, "rubble": scene_rubble, "agency": scene_agency,
          "coast": scene_coast, "strait": scene_strait, "sitroom": scene_sitroom,
          "awacs": scene_awacs, "hospital": scene_hospital, "steel": scene_steel,
          "port": scene_port, "space": scene_space, "stadium": scene_stadium,
          "launchpad": scene_launchpad}

def card_frame(x, y, w_, h_):
    d.rectangle([x, y, x + w_, y + h_], fill=CARD, outline=LGREY)

# ============ 3. LEAD CARD (162-258) ============
LY, LH = 162, 96
card_frame(10, LY, W - 20, LH)
SCENES["field"](12, LY + 2, 328, LH - 4)
tx = 356
s = S[0]
disc(tx + 11, LY + 14, 11, 1, fsz=12)
d.text((tx + 28, LY + 6), s[1], font=sansB(12), fill=NAVY)
chip(tx + 28 + tw(s[1], sansB(12)) + 10, LY + 5, s[4], 8)
d.text((tx + 28, LY + 22), f"{s[2]} · {s[3]}", font=sansB(8.5), fill=GOLD)
yy = LY + 33
for ln in wrap(s[5], serifB(18), W - 20 - tx - 12, 2):
    d.text((tx, yy), ln, font=serifB(18), fill=INK); yy += 22
for ln in wrap(s[6], sans(10), W - 20 - tx - 12, 2):
    d.text((tx, yy + 1), ln, font=sans(10), fill=(50, 48, 44)); yy += 13
d.text((tx, LY + LH - 14), f"Source: {s[7]}", font=ital(10), fill=GREY)

# ============ 4. GRID CARDS 2-13 (262-695) ============
GY, RH, GAP = 262, 106, 3
CW = (W - 20 - 2 * GAP) / 3
for idx, s in enumerate(S[1:]):
    r, c = divmod(idx, 3)
    x = 10 + c * (CW + GAP); y = GY + r * (RH + GAP)
    card_frame(x, y, CW, RH)
    SCENES[s[10]](x + 1, y + 1, CW - 2, 44)
    disc(x + 12, y + 53, 9, s[0], fsz=10)
    d.text((x + 25, y + 47), fit(s[1], sansB(9.5), CW - 110), font=sansB(9.5), fill=NAVY)
    chip(x + CW - 74, y + 46, s[4], 7.5)
    d.text((x + 25, y + 59), f"{s[2]} · {s[3]}", font=sansB(7), fill=GOLD)
    hl = wrap(s[5], serifB(10.5), CW - 14, 2)
    yy = y + 68
    for ln in hl:
        d.text((x + 7, yy), ln, font=serifB(10.5), fill=INK); yy += 11
    sm = wrap(s[6], sans(7.5), CW - 14, 1)
    if sm: d.text((x + 7, y + 91), fit(sm[0], sans(7.5), CW - 14), font=sans(7.5), fill=(60, 58, 54))
    d.text((x + 7, y + RH - 9), f"Source: {s[7]}", font=ital(7.5), fill=GREY)

# ============ 5. MAP + TIMELINE (699-855) ============
MY, MH = 699, 156
MX, MW = 10, 596
d.rectangle([MX, MY, MX + MW, MY + MH], fill=(238, 242, 246), outline=LGREY)
d.text((MX + 8, MY + 5), "WHERE IT HAPPENED — STORIES 1–13", font=sansB(10), fill=NAVY)
LAND = [
 [(-165,60),(-150,70),(-130,71),(-115,69),(-100,73),(-90,70),(-85,66),(-80,62),(-76,58),(-70,50),(-65,45),(-70,42),(-74,40),(-76,35),(-80,32),(-81,26),(-84,30),(-89,30),(-94,29),(-97,26),(-97,22),(-94,18),(-90,15),(-83,9),(-78,8),(-80,15),(-87,13),(-92,15),(-97,16),(-105,20),(-110,23),(-114,29),(-117,33),(-122,37),(-124,46),(-130,55),(-150,60)],
 [(-78,8),(-70,11),(-62,10),(-55,6),(-50,0),(-44,-3),(-35,-8),(-40,-15),(-48,-25),(-55,-33),(-62,-39),(-65,-45),(-68,-52),(-72,-54),(-74,-48),(-73,-40),(-72,-30),(-70,-20),(-75,-15),(-79,-8),(-81,-4),(-80,1),(-77,4)],
 [(-10,37),(-9,44),(-1,44),(-4,48),(1,50),(5,53),(8,57),(12,56),(18,56),(23,54),(24,58),(21,60),(25,66),(32,70),(45,68),(48,62),(42,56),(36,50),(30,46),(28,42),(23,40),(19,40),(15,44),(12,46),(8,44),(3,43),(0,39),(-2,37)],
 [(-6,35),(0,36),(10,37),(20,32),(30,31),(34,28),(38,20),(43,12),(48,11),(51,12),(45,5),(40,-5),(40,-15),(36,-22),(32,-28),(25,-34),(19,-35),(17,-30),(15,-22),(13,-12),(12,-6),(9,-1),(9,4),(4,6),(-3,5),(-8,5),(-13,8),(-17,15),(-16,20),(-14,25),(-10,30)],
 [(28,41),(36,46),(44,50),(55,52),(66,55),(78,55),(90,52),(102,51),(114,52),(126,53),(138,55),(150,60),(162,66),(175,65),(178,64),(168,60),(158,54),(148,48),(141,44),(139,36),(131,33),(124,31),(121,27),(112,21),(109,16),(106,8),(103,2),(100,8),(98,15),(94,18),(90,22),(86,20),(81,14),(77,8),(75,13),(72,20),(68,23),(62,25),(56,26),(51,29),(48,30),(52,24),(55,24),(58,22),(59,20),(55,17),(52,15),(50,12),(44,12),(40,20),(36,28),(33,32),(30,36)],
 [(113,-22),(115,-32),(120,-34),(128,-32),(134,-33),(137,-35),(140,-38),(146,-39),(150,-37),(153,-31),(153,-25),(149,-20),(143,-12),(142,-16),(139,-18),(136,-14),(132,-11),(128,-13),(124,-16),(119,-19)],
 [(130,31),(133,34),(137,35),(140,37),(141,40),(141,44),(140,45),(138,40),(135,34),(132,33)],
 [(100,6),(103,2),(105,-3),(108,-6),(112,-7),(115,-6),(112,-3),(107,0),(103,3)],
]
def inpoly(px, py, poly):
    inside = False; n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > py) != (y2 > py):
            if px < (x2 - x1) * (py - y1) / (y2 - y1) + x1: inside = not inside
    return inside
def proj(lon, lat, bx, by, bw, bh, lon0=-170, lon1=185, lat0=-58, lat1=82):
    return (bx + (lon - lon0) / (lon1 - lon0) * bw, by + (lat1 - lat) / (lat1 - lat0) * bh)
mapbox = (MX + 6, MY + 22, MW - 12, MH - 28)
lon = -168.0
while lon < 182:
    lat = -55.0
    while lat < 80:
        if any(inpoly(lon, lat, p) for p in LAND):
            px, py = proj(lon, lat, *mapbox)
            d.ellipse([px - 1.3, py - 1.3, px + 1.3, py + 1.3], fill=(168, 178, 150))
        lat += 3.2
    lon += 3.2
pin_off = {3: (-13, -8), 6: (13, 9), 9: (-11, 10), 12: (11, -11), 2: (-9, 6), 5: (10, -6)}
for s in S:
    px, py = proj(s[8], s[9], *mapbox)
    ox, oy = pin_off.get(s[0], (0, 0)); px += ox; py += oy
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=WHITE, width=2)
    f = sansB(10); t = str(s[0])
    d.text((px - tw(t, f) / 2, py - 6.5), t, font=f, fill=WHITE)
# Europe zoom inset
ZX, ZY, ZW, ZH = MX + 8, MY + MH - 108, 188, 100
d.rectangle([ZX, ZY, ZX + ZW, ZY + ZH], fill=(226, 234, 242), outline=NAVY, width=2)
d.text((ZX + 5, ZY + 3), "EUROPE — ZOOM", font=sansB(8.5), fill=NAVY)
lon = -11.0
while lon < 46:
    lat = 36.0
    while lat < 68:
        if any(inpoly(lon, lat, p) for p in LAND):
            px, py = proj(lon, lat, ZX + 4, ZY + 16, ZW - 8, ZH - 20, -12, 46, 35, 68)
            d.ellipse([px - 1.4, py - 1.4, px + 1.4, py + 1.4], fill=(150, 165, 135))
        lat += 2.2
    lon += 2.2
for s in (S[0], S[6], S[10]):
    px, py = proj(s[8], s[9], ZX + 4, ZY + 16, ZW - 8, ZH - 20, -12, 46, 35, 68)
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=RED, outline=WHITE, width=2)
    f = sansB(10); t = str(s[0])
    d.text((px - tw(t, f) / 2, py - 6.5), t, font=f, fill=WHITE)
d.text((ZX + 5, ZY + ZH - 13), "1 Kyiv · 7 Warsaw · 11 Darmstadt", font=sans(7.5), fill=NAVY)

# Right column: timeline + tally
RX, RW = MX + MW + 10, W - 10 - (MX + MW + 10)
d.rectangle([RX, MY, RX + RW, MY + 96], fill=CARD, outline=LGREY)
tl_title = wrap("WHEN MIDDAY FELL — STORIES 1–13 ON THE UTC CLOCK (LOCAL NOON, IN UTC)", sansB(8.5), RW - 14, 2)
yy = MY + 5
for ln in tl_title:
    d.text((RX + 7, yy), ln, font=sansB(8.5), fill=NAVY); yy += 11
ax0, ax1, ay = RX + 16, RX + RW - 10, MY + 60
d.line([ax0, ay, ax1, ay], fill=INK, width=1)
for hr in range(25):
    hx = ax0 + (ax1 - ax0) * hr / 24
    d.line([hx, ay - 3, hx, ay + 3], fill=INK)
    if hr % 3 == 0:
        f = sans(7); t = f"{hr:02d}"
        d.text((hx - tw(t, f) / 2, ay + 5), t, font=f, fill=GREY)
noon_utc = {1: 10, 2: 10, 3: 17, 4: 9, 5: 8.5, 6: 17, 7: 11, 8: 10, 9: 6.5, 10: 4, 11: 11, 12: 6.5, 13: 17}
seen = {}
for n_, hr in noon_utc.items():
    row = seen.get(hr, 0); seen[hr] = row + 1
    hx = ax0 + (ax1 - ax0) * hr / 24
    if row < 2:
        hy, rr, fsz = ay - 12 - row * 13, 7, 8
    else:
        hy, rr, fsz = ay + 22, 6.5, 7.5
    d.ellipse([hx - rr, hy - rr, hx + rr, hy + rr], fill=NAVY, outline=WHITE, width=1)
    f = sansB(fsz); t = str(n_)
    d.text((hx - tw(t, f) / 2, hy - fsz * 0.62), t, font=f, fill=WHITE)
# tally
TY = MY + 102
d.rectangle([RX, TY, RX + RW, MY + MH], fill=NAVY)
d.text((RX + 8, TY + 4), "REGION TALLY — ALL 34 STORIES", font=sansB(9), fill=GOLD)
tally = ["SOUTH ASIA 7", "EUROPE 6", "MIDDLE EAST 8", "N. AMERICA 9", "EAST ASIA 1", "AFRICA 1", "OCEANIA 1", "GLOBAL 1"]
yy = TY + 15
for i in range(0, 8, 2):
    for j in range(2):
        d.text((RX + 10 + j * (RW / 2), yy), tally[i + j], font=sansB(9), fill=WHITE)
    yy += 9.5

# ============ 6. RAIL 14-34 (859-949) ============
RY = 859
d.line([10, RY - 4, W - 10, RY - 4], fill=NAVY, width=2)
d.text((10, RY), "ALSO ON WEDNESDAY 25 NOVEMBER — STORIES 14–34", font=sansB(11), fill=NAVY)
RAIL = [
 (14,"Gukesh holds Sindarov in World Chess Game 1","SPORT","The Hindu"),
 (15,"England level T20 series, beat Australia by 8 wickets","SPORT","BBC"),
 (16,"Ben Stokes registers for the IPL 2027 auction","SPORT","Cricbuzz"),
 (17,"BJP and Akali Dal reunite for 2027 Punjab polls","INDIA","TOI"),
 (18,"Nvidia's Huang said he violated code of conduct","TECH","Reuters"),
 (19,"Jio scraps daily data cap on select plans","TELECOM","BusinessLine"),
 (20,"Google Cloud India denies layoffs, confirms 30 cuts","TECH","BusinessLine"),
 (21,"WFP: 266 million face acute food insecurity","AID","WFP"),
 (22,"EU announces fresh sanctions on Russia","EUROPE","Reuters"),
 (23,"Russia, Ukraine trade accusations at the UN","DIPLOMACY","UN"),
 (24,"US and Qatar discuss strategic cooperation","DIPLOMACY","Reuters"),
 (25,"RFE/RL returns to shortwave for Afghan girls","MEDIA","RFE/RL"),
 (26,"Iran braces for winter gas shortages","ENERGY","RFE/RL"),
 (27,"Baghdad to run Kurdish oilfields; Kurds reject move","IRAQ","Reuters"),
 (28,"Putin: retaliation 'inevitable' after oil-plant hits","RUSSIA","Kremlin"),
 (29,"Israeli strike kills senior Hamas security official","GAZA","Hamas sources"),
 (30,"Iran flogs singer and her team, website reports","IRAN","Iranian media"),
 (31,"Marvel drops final 'Avengers: Doomsday' trailer","FILM","Marvel"),
 (32,"Super Bowl LXI to screen live in Imax theatres","SPORT","NFL"),
 (33,"Dell lifts forecasts on record AI server quarter","TECH","Dell"),
 (34,"HBO Max halves price in Black Friday deal","MEDIA","Mashable"),
]
colw = (W - 20) / 3
for idx, (n_, head, fld, src) in enumerate(RAIL):
    r, c = idx % 7, idx // 7
    x = 10 + c * colw; y = RY + 18 + r * 10.5
    f = sansB(8.5)
    d.text((x, y), f"{n_}", font=f, fill=RED)
    nx = x + tw(f"{n_}", f) + 4
    hf = sans(8)
    hw = tw(head, hf)
    if nx + hw > x + colw - 6:
        head = fit(head, hf, colw - (nx - x) - 6); hw = tw(head, hf)
        d.text((nx, y), head, font=hf, fill=INK)
    else:
        d.text((nx, y), head, font=hf, fill=INK)
        suf = f" · {fld} — {src}"
        d.text((nx + hw, y + 0.5), fit(suf, sans(7.5), x + colw - 4 - (nx + hw)), font=sans(7.5), fill=GREY)

# ============ 7. DATE CHECK FOOTER (953-1020) ============
FY = 953
d.rectangle([10, FY, W - 10, H - 4], fill=(238, 234, 224), outline=NAVY)
d.text((18, FY + 3), "DATE CHECK — every story above happened or was first reported on Wednesday 25 November 2026 (any time zone).", font=sansB(8.5), fill=NAVY)
d.text((18, FY + 14), "LEFT OUT — other days' news, deliberately excluded:", font=sansB(8.5), fill=RED)
leftout = ["COP31 ends with no climate deal · 22 Nov", "Houthi strike on Riyadh tower, 11 hurt · 24 Nov",
           "US jury convicts Huawei on 10 counts · 24 Nov", "Zelenskyy confirms Sparta II ship strike · 24 Nov",
           "Nvidia reinstates Huang as chief executive · 23 Nov", "Turkish military helicopter crash, 5 killed · 24 Nov"]
for i, t in enumerate(leftout):
    c, r = i % 2, i // 2
    d.text((18 + c * ((W - 36) / 2), FY + 24 + r * 9), "• " + t, font=sans(8), fill=(60, 58, 54))
d.text((18, FY + 51), "CONFIRMED = 2+ outlets · OFFICIAL = authority on record · REPORTED = one outlet · CLAIM = one side's account", font=sansB(7.5), fill=NAVY)
d.text((18, FY + 60), "Sources: RFE/RL · WAFA · Oxfam · CNN · Reuters · NBC · WHO · Hindu BusinessLine · The Hindu · BBC · ESA · NASA · WFP · UN and others named above.", font=ital(7.5), fill=GREY)

img.save("/home/hatch/workspace/makefun/work/wave3/entries/news-image-20261125-v2/entry.png", optimize=True)
print("saved")
