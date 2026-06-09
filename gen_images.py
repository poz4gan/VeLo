"""Generate soccer-themed vector artwork for the VELOCITY demo site."""
import math, os, random

random.seed(7)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
os.makedirs(OUT, exist_ok=True)

DEFS = '''<defs>
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#1a1a1a"/><stop offset="1" stop-color="#0a0a0a"/>
</linearGradient>
<radialGradient id="halo"><stop offset="0" stop-color="#E53935" stop-opacity=".30"/><stop offset="1" stop-color="#E53935" stop-opacity="0"/></radialGradient>
<radialGradient id="ballG" cx=".35" cy=".3" r="1"><stop offset="0" stop-color="#ff8a80"/><stop offset=".55" stop-color="#e53935"/><stop offset="1" stop-color="#8f1414"/></radialGradient>
<linearGradient id="redV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff5f52"/><stop offset="1" stop-color="#b71c1c"/></linearGradient>
<radialGradient id="vig"><stop offset=".6" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></radialGradient>
<filter id="glow" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="10" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">{DEFS}'
            f'<rect width="{w}" height="{h}" fill="url(#bg)"/>{body}'
            f'<rect width="{w}" height="{h}" fill="url(#vig)"/></svg>')


def wordmark(w, h):
    return (f'<text x="{w-26}" y="{h-20}" font-family="Arial, sans-serif" font-size="15" '
            f'letter-spacing="6" fill="#fff" opacity=".16" text-anchor="end">VELOCITY</text>')


def ground(cx=350, y=470, w=700):
    return (f'<line x1="40" y1="{y}" x2="{w-40}" y2="{y}" stroke="#fff" stroke-opacity=".09" stroke-width="2"/>'
            f'<ellipse cx="{cx}" cy="{y}" rx="190" ry="26" fill="none" stroke="#fff" stroke-opacity=".06" stroke-width="2"/>')


def halo(cx, cy, r):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#halo)"/>'


def pent(cx, cy, r, rot=-90):
    pts = []
    for i in range(5):
        a = math.radians(rot + i * 72)
        pts.append(f"{cx + r * math.cos(a):.1f},{cy + r * math.sin(a):.1f}")
    return " ".join(pts)


def ball(cx, cy, r):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r*1.9:.0f}" fill="url(#halo)"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#ballG)"/>'
    s += f'<polygon points="{pent(cx, cy, r*.42)}" fill="#140000" opacity=".85"/>'
    for i in range(5):
        a = math.radians(-90 + i * 72)
        x1, y1 = cx + r * .42 * math.cos(a), cy + r * .42 * math.sin(a)
        x2, y2 = cx + r * .86 * math.cos(a), cy + r * .86 * math.sin(a)
        s += (f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" '
              f'stroke="#140000" stroke-width="{max(2, r*.07):.0f}" opacity=".8"/>')
    return s


def head(x, y, r=28, c="#f5f5f5"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>'


def seg(pts, w=24, c="#f5f5f5"):
    p = " ".join(f"{a},{b}" for a, b in pts)
    return (f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="{w}" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def shadow(cx, y, rx=90):
    return f'<ellipse cx="{cx}" cy="{y}" rx="{rx}" ry="13" fill="#000" opacity=".5"/>'


def cone(x, y, h=54, c="#E53935"):
    w = h * .8
    return (f'<polygon points="{x},{y-h} {x-w/2:.0f},{y} {x+w/2:.0f},{y}" fill="{c}"/>'
            f'<rect x="{x-w*.32:.0f}" y="{y-h*.48:.0f}" width="{w*.64:.0f}" height="{h*.15:.0f}" fill="#fff" opacity=".85"/>')


SCENES = {}

# ---- STRIKE: player shooting, ball flying with motion arcs ----
SCENES["strike"] = svg(700, 560,
    halo(420, 300, 280) + ground() + shadow(340, 470) +
    seg([(352, 192), (330, 300)], 46) +                       # torso
    seg([(330, 300), (300, 380), (288, 462)]) +               # standing leg
    seg([(334, 300), (420, 348), (498, 330)]) +               # kicking leg
    seg([(348, 206), (272, 264)]) +                           # back arm
    seg([(352, 204), (432, 196), (472, 148)]) +               # front arm up
    head(352, 152) +
    '<path d="M 470 330 A 150 150 0 0 1 600 250" fill="none" stroke="#E53935" stroke-width="4" opacity=".35" stroke-linecap="round"/>'
    '<path d="M 480 360 A 180 180 0 0 1 640 290" fill="none" stroke="#E53935" stroke-width="3" opacity=".2" stroke-linecap="round"/>' +
    ball(575, 300, 34) + wordmark(700, 560))

# ---- DRIBBLE: leaning run with ball at foot, cones behind ----
SCENES["dribble"] = svg(700, 560,
    halo(360, 320, 270) + ground() +
    cone(130, 472) + cone(210, 466, 44) + shadow(350, 472) +
    seg([(312, 182), (352, 292)], 46) +
    seg([(352, 292), (424, 352), (436, 446)]) +
    seg([(352, 292), (298, 380), (252, 434)]) +
    seg([(318, 200), (394, 244)]) +
    seg([(316, 202), (240, 256)]) +
    head(302, 142) +
    ball(478, 452, 30) + wordmark(700, 560))

# ---- KEEPER: diving save, goal frame, ball at top corner ----
SCENES["keeper"] = svg(700, 560,
    '<g stroke="#fff" stroke-opacity=".5" stroke-width="7" fill="none">'
    '<polyline points="90,470 90,120 610,120 610,470"/></g>'
    '<g stroke="#fff" stroke-opacity=".08" stroke-width="2">' +
    "".join(f'<line x1="{x}" y1="124" x2="{x}" y2="468"/>' for x in range(130, 610, 42)) +
    "".join(f'<line x1="92" y1="{y}" x2="608" y2="{y}"/>' for y in range(160, 470, 42)) +
    '</g>' + halo(480, 240, 260) +
    seg([(282, 312), (392, 278)], 46) +                       # torso horizontal
    seg([(392, 282), (470, 238), (542, 206)]) +               # top arm to ball
    seg([(386, 294), (458, 268)]) +                           # second arm
    seg([(284, 312), (212, 360), (152, 402)]) +               # leg
    seg([(288, 316), (228, 330), (178, 308)]) +               # leg 2
    head(252, 300) +
    ball(580, 178, 30) + ground() + wordmark(700, 560))

# ---- HEADER: jumping header, ball above ----
SCENES["header"] = svg(700, 560,
    halo(350, 220, 260) + ground() + shadow(350, 470, 70) +
    ball(350, 96, 28) +
    head(350, 178) +
    seg([(350, 214), (346, 318)], 46) +
    seg([(348, 228), (270, 180)]) +
    seg([(352, 228), (430, 180)]) +
    seg([(346, 318), (308, 388), (330, 446)]) +
    seg([(350, 318), (400, 380), (378, 446)]) +
    wordmark(700, 560))

# ---- SPRINT: deep lean with speed streaks ----
streaks = "".join(
    f'<rect x="{60+i*18}" y="{150+i*38}" width="{240-i*22}" height="8" rx="4" fill="#E53935" opacity="{.3-i*.04:.2f}"/>'
    for i in range(6))
SCENES["sprint"] = svg(700, 560,
    streaks + halo(420, 280, 260) + ground() + shadow(420, 470) +
    seg([(438, 196), (384, 300)], 46) +
    seg([(384, 300), (472, 358), (520, 450)]) +
    seg([(384, 300), (302, 338), (232, 300)]) +
    seg([(430, 212), (504, 252)]) +
    seg([(426, 214), (352, 252), (372, 302)]) +
    head(434, 154) + wordmark(700, 560))

# ---- CELEBRATE: arms up V, confetti ----
confetti = "".join(
    f'<rect x="{random.randint(60,640)}" y="{random.randint(60,300)}" width="7" height="11" rx="2" '
    f'fill="{random.choice(["#E53935","#fff","#FFD700"])}" opacity="{random.uniform(.25,.7):.2f}" '
    f'transform="rotate({random.randint(-50,50)} {random.randint(60,640)} {random.randint(60,300)})"/>'
    for _ in range(26))
SCENES["celebrate"] = svg(700, 560,
    confetti + halo(350, 260, 280) + ground() + shadow(350, 470) +
    seg([(350, 196), (350, 312)], 46) +
    seg([(348, 212), (282, 128)]) +
    seg([(352, 212), (418, 128)]) +
    seg([(350, 312), (302, 396), (296, 466)]) +
    seg([(350, 312), (398, 396), (404, 466)]) +
    head(350, 156) +
    ball(560, 452, 28) + wordmark(700, 560))

# ---- TEAM: row of five linked figures ----
team = halo(350, 300, 300) + ground()
xs = [190, 270, 350, 430, 510]
for x in xs:
    team += shadow(x, 470, 46)
for x in xs:
    team += seg([(x, 232), (x, 330)], 40)
    team += seg([(x, 330), (x - 22, 400), (x - 20, 462)], 20)
    team += seg([(x, 330), (x + 22, 400), (x + 20, 462)], 20)
for a, b in zip(xs, xs[1:]):
    team += seg([(a + 8, 246), (b - 8, 246)], 18)            # arms over shoulders
team += seg([(190, 246), (140, 310)], 18) + seg([(510, 246), (560, 310)], 18)
for x in xs:
    team += head(x, 192, 26)
team += ball(350, 452, 26)
SCENES["team"] = svg(700, 560, team + wordmark(700, 560))

# ---- STADIUM: floodlights and pitch ----
def tower(x):
    lights = "".join(
        f'<circle cx="{x-33+c*22}" cy="{66+r*20}" r="8" fill="#fff" filter="url(#glow)"/>'
        for r in range(2) for c in range(4))
    return (f'<polygon points="{x-6},90 {x+6},90 {x+16},330 {x-16},330" fill="#1f1f1f"/>'
            f'<rect x="{x-44}" y="52" width="88" height="52" rx="6" fill="#101010" stroke="#333"/>' + lights +
            f'<polygon points="{x-40},104 {x+40},104 {x+150},470 {x-150},470" fill="#fff" opacity=".05"/>')

pitchlines = "".join(
    f'<line x1="{120-i*12}" y1="{358+i*28}" x2="{580+i*12}" y2="{358+i*28}" stroke="#fff" stroke-opacity=".1" stroke-width="2"/>'
    for i in range(5))
SCENES["stadium"] = svg(700, 560,
    '<rect x="0" y="300" width="700" height="40" fill="#E53935" opacity=".06"/>' +
    '<ellipse cx="350" cy="310" rx="330" ry="60" fill="url(#halo)"/>' +
    tower(160) + tower(540) + pitchlines +
    '<ellipse cx="350" cy="420" rx="120" ry="34" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="3"/>'
    '<line x1="80" y1="420" x2="620" y2="420" stroke="#fff" stroke-opacity=".18" stroke-width="3"/>' +
    ball(350, 420, 22) + wordmark(700, 560))

# ---- DRILLS: top-down ladder + slalom cones ----
ladder = '<g stroke="#fff" stroke-opacity=".55" stroke-width="6">'
ladder += '<line x1="200" y1="90" x2="200" y2="480"/><line x1="290" y1="90" x2="290" y2="480"/>'
ladder += "".join(f'<line x1="200" y1="{y}" x2="290" y2="{y}"/>' for y in range(90, 481, 48))
ladder += '</g>'
cones_z = "".join(cone(430 + (i % 2) * 120, 150 + i * 80, 46) for i in range(5))
SCENES["drills"] = svg(700, 560,
    halo(350, 280, 300) + ladder + cones_z +
    '<path d="M 430 110 Q 560 190 442 230 Q 320 270 560 310 Q 680 350 460 400" fill="none" '
    'stroke="#E53935" stroke-width="4" stroke-dasharray="12 10" opacity=".7"/>' +
    ball(470, 452, 26) + wordmark(700, 560))

# ---- TACTICS: chalkboard pitch with X / O and arrows ----
tact = ('<rect x="100" y="80" width="500" height="400" rx="8" fill="none" stroke="#fff" stroke-opacity=".4" stroke-width="3"/>'
        '<line x1="100" y1="280" x2="600" y2="280" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>'
        '<circle cx="350" cy="280" r="58" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>'
        '<rect x="240" y="80" width="220" height="70" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>'
        '<rect x="240" y="410" width="220" height="70" fill="none" stroke="#fff" stroke-opacity=".3" stroke-width="2"/>')
def X(x, y):
    return (f'<line x1="{x-14}" y1="{y-14}" x2="{x+14}" y2="{y+14}" stroke="#E53935" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="{x+14}" y1="{y-14}" x2="{x-14}" y2="{y+14}" stroke="#E53935" stroke-width="7" stroke-linecap="round"/>')
def O(x, y):
    return f'<circle cx="{x}" cy="{y}" r="15" fill="none" stroke="#f5f5f5" stroke-width="6"/>'
tact += X(200, 360) + X(350, 330) + X(480, 380) + X(300, 430)
tact += O(250, 180) + O(420, 160) + O(350, 230) + O(180, 240)
tact += ('<path d="M 350 330 Q 390 250 420 180" fill="none" stroke="#E53935" stroke-width="4" stroke-dasharray="10 8"/>'
         '<polygon points="424,156 408,184 436,180" fill="#E53935"/>'
         '<path d="M 200 360 Q 210 290 250 200" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="3" stroke-dasharray="8 8"/>')
SCENES["tactics"] = svg(700, 560, halo(350, 280, 300) + tact + wordmark(700, 560))

# ---- BALLGLOW: dramatic hero ball ----
orbit = ('<ellipse cx="350" cy="266" rx="210" ry="64" fill="none" stroke="#E53935" stroke-opacity=".4" stroke-width="2" transform="rotate(-16 350 266)"/>'
         '<ellipse cx="350" cy="266" rx="250" ry="84" fill="none" stroke="#E53935" stroke-opacity=".18" stroke-width="2" transform="rotate(12 350 266)"/>')
dots = "".join(
    f'<circle cx="{random.randint(60,640)}" cy="{random.randint(60,460)}" r="{random.choice([2,2,3])}" fill="#E53935" opacity="{random.uniform(.2,.7):.2f}"/>'
    for _ in range(30))
SCENES["ballglow"] = svg(700, 560,
    dots + halo(350, 266, 320) + ball(350, 266, 110) + orbit +
    '<ellipse cx="350" cy="488" rx="150" ry="20" fill="#E53935" opacity=".08"/>' +
    wordmark(700, 560))

# ---- PASS: two figures, dashed pass line ----
SCENES["pass"] = svg(700, 560,
    halo(350, 320, 300) + ground() + shadow(170, 470, 60) + shadow(540, 470, 60) +
    # passer (left, follow-through)
    seg([(166, 222), (178, 318)], 40) +
    seg([(178, 318), (150, 392), (142, 458)], 21) +
    seg([(180, 318), (244, 360), (272, 420)], 21) +
    seg([(170, 236), (120, 290)], 21) + seg([(172, 234), (228, 262)], 21) +
    head(162, 184, 26) +
    # receiver (right, ready)
    seg([(544, 230), (536, 326)], 40) +
    seg([(536, 326), (502, 398), (498, 460)], 21) +
    seg([(538, 326), (582, 396), (590, 458)], 21) +
    seg([(540, 244), (590, 290)], 21) + seg([(538, 244), (488, 286)], 21) +
    head(548, 192, 26) +
    '<path d="M 290 430 Q 400 330 480 432" fill="none" stroke="#E53935" stroke-width="4" stroke-dasharray="12 10" opacity=".75"/>' +
    ball(470, 448, 26) + wordmark(700, 560))

for name, code in SCENES.items():
    with open(os.path.join(OUT, f"{name}.svg"), "w") as f:
        f.write(code)

# ---- PLAYER CARDS ----
PLAYERS = [("09", "STRIKER"), ("07", "WINGER"), ("10", "PLAYMAKER"), ("04", "DEFENDER"),
           ("01", "KEEPER"), ("11", "FORWARD"), ("08", "MIDFIELD"), ("03", "FULLBACK")]
hexes = "".join(
    f'<polygon points="{pent(random.randint(60,500), random.randint(120,640), random.randint(26,60), rot=random.randint(0,72))}" '
    f'fill="none" stroke="#fff" stroke-opacity=".05" stroke-width="2"/>'
    for _ in range(8))
for num, pos in PLAYERS:
    body = (hexes +
        '<polygon points="0,500 560,320 560,408 0,588" fill="#E53935" opacity=".12"/>'
        '<rect x="16" y="16" width="528" height="728" fill="none" stroke="#E53935" stroke-opacity=".45" stroke-width="2"/>'
        '<text x="280" y="76" font-family="Arial, sans-serif" font-size="22" letter-spacing="10" fill="#fff" opacity=".8" text-anchor="middle">VELOCITY</text>'
        '<text x="280" y="106" font-family="Arial, sans-serif" font-size="13" letter-spacing="6" fill="#E53935" text-anchor="middle">ELITE ROSTER</text>'
        f'<text x="286" y="494" font-family="Impact, \'Arial Black\', sans-serif" font-size="330" fill="#000" opacity=".55" text-anchor="middle">{num}</text>'
        f'<text x="280" y="488" font-family="Impact, \'Arial Black\', sans-serif" font-size="330" fill="url(#redV)" text-anchor="middle">{num}</text>'
        f'<text x="280" y="630" font-family="Impact, \'Arial Black\', sans-serif" font-size="52" letter-spacing="8" fill="#f5f5f5" text-anchor="middle">{pos}</text>'
        '<rect x="220" y="654" width="120" height="4" fill="#E53935"/>'
        '<text x="280" y="700" font-family="Arial, sans-serif" font-size="15" letter-spacing="4" fill="#888" text-anchor="middle">TRAIN FAST · PLAY FASTER</text>')
    with open(os.path.join(OUT, f"player-{num}.svg"), "w") as f:
        f.write(svg(560, 760, body))

# ---- ABOUT: coach pictogram ----
about = ('<text x="400" y="700" font-family="Impact, \'Arial Black\', sans-serif" font-size="660" '
         'fill="none" stroke="#E53935" stroke-opacity=".09" stroke-width="3" text-anchor="middle">V</text>' +
    halo(380, 480, 360) +
    f'<line x1="60" y1="800" x2="740" y2="800" stroke="#fff" stroke-opacity=".1" stroke-width="2"/>' +
    shadow(320, 800, 110) +
    seg([(322, 348), (320, 520)], 52) +
    seg([(320, 520), (282, 656), (276, 786)], 27) +
    seg([(320, 520), (364, 656), (370, 786)], 27) +
    seg([(318, 372), (452, 330), (562, 302)], 27) +          # pointing arm
    seg([(322, 376), (242, 452)], 27) +                      # arm to clipboard
    '<g transform="rotate(-12 218 500)"><rect x="172" y="438" width="96" height="126" rx="8" fill="#161616" stroke="#f5f5f5" stroke-width="5"/>'
    '<line x1="190" y1="472" x2="250" y2="472" stroke="#E53935" stroke-width="5"/>'
    '<line x1="190" y1="498" x2="250" y2="498" stroke="#555" stroke-width="5"/>'
    '<line x1="190" y1="524" x2="236" y2="524" stroke="#555" stroke-width="5"/></g>' +
    head(324, 296, 32) +
    cone(620, 790, 64) + ball(520, 756, 40) +
    '<text x="400" y="900" font-family="Arial, sans-serif" font-size="17" letter-spacing="8" fill="#fff" opacity=".35" text-anchor="middle">PRO-ACADEMY METHODOLOGY</text>')
with open(os.path.join(OUT, "about.svg"), "w") as f:
    f.write(svg(800, 1000, about))

# ---- SCRIMMAGE POSTER ----
hazard = "".join(
    f'<rect x="{-40+i*44}" y="-20" width="20" height="80" fill="#E53935" transform="rotate(45 {i*44} 20)" opacity=".5"/>'
    for i in range(8))
poster = (f'<g>{hazard}</g><g transform="translate(800,1000) rotate(180)">{hazard}</g>' +
    '<rect x="22" y="22" width="756" height="956" fill="none" stroke="#E53935" stroke-opacity=".6" stroke-width="3"/>'
    '<text x="400" y="150" font-family="Arial, sans-serif" font-size="24" letter-spacing="12" fill="#bbb" text-anchor="middle">VELOCITY PRESENTS</text>'
    '<text x="400" y="290" font-family="Impact, \'Arial Black\', sans-serif" font-size="128" letter-spacing="4" fill="#f5f5f5" text-anchor="middle">WEEKEND</text>'
    '<text x="400" y="408" font-family="Impact, \'Arial Black\', sans-serif" font-size="100" letter-spacing="3" fill="url(#redV)" text-anchor="middle">SCRIMMAGES</text>'
    '<rect x="300" y="438" width="200" height="5" fill="#E53935"/>'
    '<text x="400" y="510" font-family="Arial, sans-serif" font-size="26" letter-spacing="4" fill="#ddd" text-anchor="middle">INVITE ONLY &#183; EXCLUSIVE ACCESS</text>'
    '<text x="400" y="556" font-family="Arial, sans-serif" font-size="26" letter-spacing="4" fill="#ddd" text-anchor="middle">HIGHLY COMPETITIVE &#183; ELITE ENVIRONMENT</text>'
    '<text x="400" y="602" font-family="Arial, sans-serif" font-size="26" letter-spacing="4" fill="#ddd" text-anchor="middle">MIXED AGE GROUPS &#183; 2 HOURS PER SESSION</text>' +
    halo(400, 760, 280) +
    '<text x="404" y="822" font-family="Impact, \'Arial Black\', sans-serif" font-size="220" fill="#000" opacity=".5" text-anchor="middle">10</text>'
    '<text x="400" y="818" font-family="Impact, \'Arial Black\', sans-serif" font-size="220" fill="url(#redV)" text-anchor="middle">10</text>'
    '<text x="400" y="868" font-family="Arial, sans-serif" font-size="30" letter-spacing="10" fill="#f5f5f5" text-anchor="middle">LIMITED SPOTS</text>'
    '<text x="400" y="930" font-family="Arial, sans-serif" font-size="22" letter-spacing="4" fill="#999" text-anchor="middle">$100 / 4 SESSIONS &#183; SUNDAYS</text>')
with open(os.path.join(OUT, "scrimmage.svg"), "w") as f:
    f.write(svg(800, 1000, poster))

print("Generated:", sorted(os.listdir(OUT)))
