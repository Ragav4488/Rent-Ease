"""Capture RentEase screenshots with Playwright driving the installed Chrome.

The system Chrome needs --single-process under this sandbox (its GPU helper
aborts otherwise), which is why raw CDP was unreliable; Playwright's launcher
handles that fine.

Run the PHP server first:
    php -S 127.0.0.1:8088 -t RentEase
Then:
    python RentEase/scripts/shoot.py
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "screenshots"
BASE = "http://127.0.0.1:8088"
WIDTH = 1280

PUBLIC = [
    ("01-home",              "/index.php",                                          1.2),
    ("02-properties",        "/properties.php",                                     1.0),
    ("03-properties-filter", "/properties.php?city=Coimbatore&bhk=2&max_rent=20000", 1.0),
    ("04-property-detail",   "/property.php?id=1",                                  1.0),
    ("05-register",          "/register.php",                                       0.9),
    ("06-login",             "/login.php",                                          0.9),
]

TENANT = [
    ("07-tenant-dashboard", "/tenant_dashboard.php", 1.3),
    ("08-pay-rent",         "/pay_rent.php",         1.0),
    ("09-complaints",       "/complaints.php",       1.0),
]

OWNER = [
    ("10-owner-dashboard",  "/owner_dashboard.php", 1.5),
    ("11-add-property",     "/add_property.php",    1.0),
]


def shoot(page, name, path, wait):
    page.goto(f"{BASE}{path}", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(int(wait * 1000))
    target = OUT / f"{name}.png"
    page.screenshot(path=str(target), full_page=True)
    print(f"  {target.name:26s} {page.viewport_size['width']}x"
          f"{target.stat().st_size // 1024} KB")
    return target


def login(page, email, password):
    page.goto(f"{BASE}/login.php", wait_until="networkidle", timeout=30000)
    page.fill("#email", email)
    page.fill("#password", password)
    page.click("form[method=post] button[type=submit]")
    page.wait_for_load_state("networkidle", timeout=30000)
    page.wait_for_timeout(600)


def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("*.png"):
        f.unlink()

    with sync_playwright() as pw:
        browser = pw.chromium.launch(
            channel="chrome", headless=True,
            args=["--single-process", "--disable-gpu", "--disable-crashpad",
                  "--hide-scrollbars", "--force-device-scale-factor=1"],
        )
        ctx = browser.new_context(viewport={"width": WIDTH, "height": 900},
                                  device_scale_factor=1, locale="en-IN")
        page = ctx.new_page()

        print("public pages")
        for name, path, wait in PUBLIC:
            shoot(page, name, path, wait)

        print("tenant session")
        login(page, "arjun.tenant@rentease.in", "rent@1234")
        for name, path, wait in TENANT:
            shoot(page, name, path, wait)

        print("owner session")
        page.goto(f"{BASE}/logout.php", wait_until="networkidle", timeout=30000)
        login(page, "ragav.owner@rentease.in", "rent@1234")
        for name, path, wait in OWNER:
            shoot(page, name, path, wait)

        browser.close()
    print(f"done — {len(list(OUT.glob('*.png')))} screenshots in {OUT}")


if __name__ == "__main__":
    main()
