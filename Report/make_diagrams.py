"""Draw the RentEase three-tier architecture and ER diagrams as PNGs.

Both are pure PIL so no Graphviz / matplotlib dependency is needed.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

INK = (18, 32, 46)
SOFT = (75, 96, 118)
LINE = (176, 192, 208)
BRAND = (15, 118, 110)
BRAND_DK = (11, 92, 86)
TINT = (230, 244, 242)
AMBER = (180, 83, 9)
AMBER_T = (254, 243, 199)
BLUE = (3, 105, 161)
BLUE_T = (224, 242, 254)
WHITE = (255, 255, 255)


def font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold
        else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()


def center(d, box, text, f, fill):
    """Draw text centred in box; multi-line strings are stacked."""
    x0, y0, x1, y1 = box
    lines = str(text).split("\n")
    lh = f.size + 4
    total = lh * len(lines)
    cy = y0 + (y1 - y0 - total) / 2
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f)
        d.text((x0 + (x1 - x0 - tw) / 2, cy + i * lh), ln, font=f, fill=fill)


def rbox(d, box, fill, outline, radius=10, width=2):
    d.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def tier(d, y0, y1, label, sub, body):
    d.rounded_rectangle([40, y0, 1280, y1], radius=14, fill=WHITE,
                        outline=LINE, width=2)
    d.rounded_rectangle([40, y0, 250, y1], radius=14, fill=TINT, outline=LINE, width=2)
    d.rectangle([240, y0 + 2, 252, y1 - 2], fill=TINT)
    center(d, (52, y0 + 18, 240, y0 + 52), label, font(19, True), BRAND_DK)
    center(d, (52, y0 + 54, 240, y1 - 18), sub, font(13), SOFT)
    body(d)


def arrow(d, p0, p1, color=SOFT, width=3):
    d.line([p0, p1], fill=color, width=width)
    (x0, y0), (x1, y1) = p0, p1
    if abs(x1 - x0) > abs(y1 - y0):
        s = 1 if x1 > x0 else -1
        d.polygon([(x1, y1), (x1 - 11 * s, y1 - 6), (x1 - 11 * s, y1 + 6)], fill=color)
    else:
        s = 1 if y1 > y0 else -1
        d.polygon([(x1, y1), (x1 - 6, y1 - 11 * s), (x1 + 6, y1 - 11 * s)], fill=color)


def architecture():
    W, H = 1320, 900
    img = Image.new("RGB", (W, H), (245, 247, 251))
    d = ImageDraw.Draw(img)

    d.text((40, 24), "RentEase — Three-Tier Architecture", font=font(30, True), fill=INK)
    d.text((40, 62), "Presentation (browser) → Application (PHP) → Data (MySQL)",
           font=font(15), fill=SOFT)

    # ---------- tier 1 : client ----------
    def body1(d):
        items = [("index.php", "Landing"), ("properties.php", "Search & filter"),
                 ("property.php", "Detail + apply")]
        for i, (f, s) in enumerate(items):
            x = 280 + i * 245
            rbox(d, [x, 116, x + 225, 172], BLUE_T, BLUE)
            center(d, (x, 118, x + 225, 144), f, font(14, True), BLUE)
            center(d, (x, 144, x + 225, 170), s, font(12), SOFT)

        items2 = [("style.css", "Cascade + grid"), ("main.js", "Validation / filters")]
        for i, (f, s) in enumerate(items2):
            x = 280 + i * 245
            rbox(d, [x, 184, x + 225, 236], WHITE, LINE)
            center(d, (x, 186, x + 225, 210), f, font(14, True), INK)
            center(d, (x, 210, x + 225, 234), s, font(12), SOFT)

    tier(d, 100, 250, "PRESENTATION", "HTML · CSS · JavaScript", body1)

    # ---------- tier 2 : application ----------
    def body2(d):
        groups = [
            ("Authentication", ["login.php", "register.php", "logout.php"]),
            ("Tenant flows", ["tenant_dashboard.php", "pay_rent.php", "complaints.php"]),
            ("Owner flows", ["owner_dashboard.php", "add_property.php", "application_action.php"]),
        ]
        for i, (title, files) in enumerate(groups):
            x = 280 + i * 245
            rbox(d, [x, 290, x + 225, 430], WHITE, BRAND)
            center(d, (x, 292, x + 225, 318), title, font(14, True), BRAND_DK)
            for j, f in enumerate(files):
                yy = 324 + j * 32
                d.text((x + 16, yy), "• " + f, font=font(12), fill=SOFT)

        # shared includes strip
        rbox(d, [280, 444, 1215, 492], TINT, BRAND)
        center(d, (290, 446, 1210, 470),
               "includes/functions.php  ·  includes/header.php  ·  includes/footer.php",
               font(13, True), BRAND_DK)
        center(d, (290, 470, 1210, 490),
               "session guard · CSRF token · PDO helpers · htmlspecialchars output",
               font(12), SOFT)

    tier(d, 274, 508, "APPLICATION", "PHP 8.4 · PDO", body2)

    # ---------- tier 3 : data ----------
    def body3(d):
        tables = ["users", "properties", "property_images",
                  "applications", "payments", "complaints"]
        for i, t in enumerate(tables):
            col, row = i % 3, i // 3
            x = 280 + col * 245
            y = 546 + row * 62
            rbox(d, [x, y, x + 225, y + 50], AMBER_T, AMBER)
            center(d, (x, y + 2, x + 225, y + 24), t, font(14, True), AMBER)
            center(d, (x, y + 24, x + 225, y + 48),
                   "InnoDB · foreign keys", font(11), SOFT)

        rbox(d, [1020, 546, 1215, 668], WHITE, LINE)
        center(d, (1024, 550, 1211, 574), "config/db.php", font(13, True), INK)
        center(d, (1024, 578, 1211, 640),
               "one PDO handle\ncharset utf8mb4\nexceptions on", font(11), SOFT)

    tier(d, 532, 690, "DATA", "MySQL 9", body3)

    # ---------- arrows ----------
    arrow(d, (1000, 250), (1000, 274))
    arrow(d, (1000, 508), (1000, 532))
    d.text((862, 254), "HTTP GET / POST", font=font(11), fill=SOFT)
    d.text((880, 512), "SQL over PDO", font=font(11), fill=SOFT)

    # ---------- request flow ----------
    d.text((40, 716), "Request flow for “record a rent payment”", font=font(17, True), fill=INK)
    steps = ["Browser posts\nthe form", "verify_csrf()\nchecks token",
             "require_role(\n'tenant')", "PDO prepared\nINSERT", "UNIQUE key\nblocks dupes",
             "Redirect +\nflash message"]
    for i, s in enumerate(steps):
        x = 40 + i * 205
        rbox(d, [x, 750, x + 185, 822], WHITE, BRAND, radius=10)
        center(d, (x, 754, x + 185, 818), s, font(12), INK)
        if i < len(steps) - 1:
            arrow(d, (x + 187, 786), (x + 203, 786), BRAND, 2)

    img.save(OUT / "architecture.png", quality=95)
    return OUT / "architecture.png"


def er_diagram():
    """Six-table ER diagram on an explicit grid.

    Gutters are kept empty so every relationship line runs in blank space:
      gutter A|B  x = 320..355     gutter B|C  x = 700..735
      row gutter  y = 445..545     right margin x = 1085..1320
    """
    W, H = 1360, 860
    img = Image.new("RGB", (W, H), (250, 251, 253))
    d = ImageDraw.Draw(img)
    d.text((36, 20), "RentEase - Entity Relationship Diagram", font=font(27, True), fill=INK)
    d.text((36, 55), "Six InnoDB tables; a single users table serves both owners and tenants",
           font=font(13), fill=SOFT)

    def entity(x, y, w, name, cols):
        h = 34 + 19 * len(cols) + 8
        rbox(d, [x, y, x + w, y + h], WHITE, BRAND, radius=8)
        d.rounded_rectangle([x, y, x + w, y + 30], radius=8, fill=TINT,
                            outline=BRAND, width=2)
        d.rectangle([x + 2, y + 20, x + w - 2, y + 30], fill=TINT)
        center(d, (x, y, x + w, y + 29), name, font(14, True), BRAND_DK)
        for i, c in enumerate(cols):
            key = c[:2] in ("PK", "FK", "UQ")
            d.text((x + 10, y + 36 + i * 19), c, font=font(11, key),
                   fill=INK if key else SOFT)
        return dict(x=x, y=y, w=w, h=h,
                    cx=x + w / 2, cy=y + h / 2,
                    left=x, right=x + w, top=y, bottom=y + h)

    # ---------- entities ----------
    users = entity(40, 110, 250, "users",
                   ["PK user_id", "   full_name", "UQ email", "   phone",
                    "   password_hash", "   role"])
    props = entity(400, 100, 290, "properties",
                   ["PK property_id", "FK owner_id -> users", "   title, description",
                    "   property_type, bhk", "   city, locality, address",
                    "   rent_amount, deposit", "   area_sqft, furnishing",
                    "   available_from, status", "   cover_image"])
    pays = entity(800, 110, 285, "payments",
                  ["PK payment_id", "FK property_id", "FK tenant_id -> users",
                   "UQ (property_id,", "     tenant_id, pay_month)",
                   "   amount, method", "   txn_ref, paid_on"])

    imgs = entity(40, 590, 250, "property_images",
                  ["PK image_id", "FK property_id", "   image_path", "   caption"])
    apps = entity(400, 575, 290, "applications",
                  ["PK application_id", "FK property_id", "FK tenant_id -> users",
                   "UQ (property_id, tenant_id)", "   occupation, family_size",
                   "   status"])
    cmps = entity(800, 575, 285, "complaints",
                  ["PK complaint_id", "FK property_id", "FK tenant_id -> users",
                   "   category, subject", "   description, priority",
                   "   status, owner_note", "   resolved_on"])

    def route(points, label=None, at=None):
        d.line(points, fill=SOFT, width=2, joint="curve")
        # dot at the "many" end
        ex, ey = points[-1]
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=BRAND)
        if label and at:
            d.text(at, label, font=font(10), fill=SOFT)

    # 1. users 1:M properties  (same row, straight across)
    route([(users["right"], 175), (props["left"], 175)])
    d.text((306, 156), "1:M", font=font(10), fill=SOFT)

    # 2. users 1:M applications  (gutter x=320 down, then right)
    route([(users["right"], 250), (320, 250), (320, 640), (apps["left"], 640)])
    d.text((250, 430), "1:M", font=font(10), fill=SOFT)

    # 3. users 1:M payments  (lane y=470, right margin x=1210 up)
    route([(users["right"], 300), (300, 300), (300, 470), (1210, 470),
           (1210, pays["bottom"] - 20), (pays["right"], pays["bottom"] - 20)])
    d.text((930, 452), "1:M", font=font(10), fill=SOFT)

    # 4. users 1:M complaints  (lane y=515)
    route([(users["right"], 330), (285, 330), (285, 515), (1250, 515),
           (1250, cmps["top"] + 30), (cmps["right"], cmps["top"] + 30)])
    d.text((930, 497), "1:M", font=font(10), fill=SOFT)

    # 5. properties 1:M property_images  (gutter x=355 down, into left column)
    route([(props["left"], 330), (355, 330), (355, 700), (imgs["right"], 700)])
    d.text((358, 700), "1:M", font=font(10), fill=SOFT)

    # 6. properties 1:M applications  (straight down)
    route([(props["cx"], props["bottom"]), (props["cx"], apps["top"])])
    d.text((props["cx"] + 8, 545), "1:M", font=font(10), fill=SOFT)

    # 7. properties 1:M payments  (same row, straight across)
    route([(props["right"], 175), (pays["left"], 175)])
    d.text((705, 156), "1:M", font=font(10), fill=SOFT)

    # 8. properties 1:M complaints  (gutter x=735 down, then right)
    route([(props["right"], 290), (735, 290), (735, 620), (cmps["left"], 620)])
    d.text((752, 596), "1:M", font=font(10), fill=SOFT)

    # legend
    d.rectangle([40, 790, 300, 815], fill=WHITE, outline=LINE)
    d.line([(52, 802), (86, 802)], fill=SOFT, width=2)
    d.ellipse([86, 799, 92, 805], fill=BRAND)
    d.text((100, 795), "one-to-many relationship", font=font(11), fill=SOFT)
    d.text((320, 795), "PK primary key    FK foreign key    UQ unique constraint",
           font=font(11), fill=SOFT)

    img.save(OUT / "er_diagram.png", quality=95)
    return OUT / "er_diagram.png"


if __name__ == "__main__":
    print("wrote", architecture())
    print("wrote", er_diagram())
