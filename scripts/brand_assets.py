"""Build every brand file the site serves from the robin logo's SVGs (~/projects/qz-brand/robin, traced from the
chosen concept). Dev-time only: needs inkscape and playwright; the outputs are committed.
  app/static/img/brand/{wordmark,wordmark-dark,robin,robin-dark,icon}.svg
  app/static/img/{logo,favicon-32,apple-touch-icon,icon-192,icon-512,icon-maskable-192,icon-maskable-512}.png
  app/static/{icon-192,icon-512}.png
  app/static/img/shot-question.webp, shot-my-day.webp: the old Q in their header swapped for the robin
  app/static/img/og-preview.png (1200x630 link preview)
Usage: python3 scripts/brand_assets.py"""
import os, shutil, subprocess, tempfile
import numpy as np
from PIL import Image

SRC = os.path.expanduser("~/projects/qz-brand/robin")
APP = os.path.join(os.path.dirname(__file__), "..", "app", "static")
IMG, BRAND = f"{APP}/img", f"{APP}/img/brand"
INDIGO, INDIGO_DARK = "#4F46E5", "#A5B4FC"          # the dark-theme link colour (style.css) for letters on #0B1020
os.makedirs(BRAND, exist_ok=True)
tmp = tempfile.mkdtemp()


def svg_png(svg, out, w=None, h=None):
    args = ["inkscape", svg, "--export-type=png", f"--export-filename={out}"]
    args += [f"--export-width={w}"] if w else [f"--export-height={h}"]
    subprocess.run(args, check=True, capture_output=True)
    return Image.open(out).convert("RGBA")


# 1. SVGs, with a dark-theme variant whose indigo is lighter
for name, src in (("wordmark", "robin-wordmark.svg"), ("robin", "robin-q.svg"), ("icon", "robin-icon.svg")):
    s = open(f"{SRC}/{src}").read()
    open(f"{BRAND}/{name}.svg", "w").write(s)
    if name != "icon":
        open(f"{BRAND}/{name}-dark.svg", "w").write(s.replace(f'fill="{INDIGO}"', f'fill="{INDIGO_DARK}"'))

# 2. PNGs
def square(im, size, pad, bg=None):
    """im centred in a size x size square, fitting inside (1 - 2*pad) of it."""
    room = int(size * (1 - 2 * pad))
    k = room / max(im.size); im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    out = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    out.alpha_composite(im, ((size - im.width) // 2, (size - im.height) // 2))
    return out

bird = svg_png(f"{BRAND}/robin.svg", f"{tmp}/bird.png", h=1024)
square(bird, 512, 0.04).save(f"{IMG}/logo.png")
icon = svg_png(f"{BRAND}/icon.svg", f"{tmp}/icon.png", w=1024)
for n, size in (("favicon-32", 32), ("icon-192", 192), ("icon-512", 512)):
    icon.resize((size, size), Image.LANCZOS).save(f"{IMG}/{n}.png")
for size in (192, 512):
    shutil.copy(f"{IMG}/icon-{size}.png", f"{APP}/icon-{size}.png")
# full-bleed squares: iOS rounds the corners itself; maskable icons keep the bird inside the 80% safe circle
white_bird = svg_png(f"{SRC}/robin-icon-square.svg", f"{tmp}/sq.png", w=1024)
inner = white_bird.crop((int(1024 * .2), int(1024 * .12), int(1024 * .86), int(1024 * .9)))
inner = inner.crop(Image.fromarray((np.array(inner)[..., 1] > 120).astype(np.uint8) * 255).getbbox())   # the bird only
for n, size, pad in (("apple-touch-icon", 180, 0.17), ("icon-maskable-192", 192, 0.24), ("icon-maskable-512", 512, 0.24)):
    square(inner, size, pad, bg=INDIGO).convert("RGB").save(f"{IMG}/{n}.png")

# 3. the landing screenshots: swap the old Q in the header for the robin
def patch_shot(path):
    im = Image.open(path).convert("RGB"); a = np.array(im).astype(float)
    reg = a[:72, :90]                                  # the header's left corner only
    sat = reg.max(2) - reg.min(2)
    m = sat > 90                                      # the old Q is the only saturated thing there
    ys, xs = np.where(m)
    y0, y1, x0, x1 = ys.min() - 3, ys.max() + 4, xs.min() - 3, xs.max() + 4
    left = np.median(a[y0:y1, max(0, x0 - 8):x0 - 2], axis=1); right = np.median(a[y0:y1, x1 + 2:x1 + 10], axis=1)
    t = np.linspace(0, 1, x1 - x0)[None, :, None]
    a[y0:y1, x0:x1] = left[:, None] * (1 - t) + right[:, None] * t
    h = round((y1 - y0) * 1.12); b = bird.resize((round(bird.width * h / bird.height), h), Image.LANCZOS)
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).convert("RGBA")
    out.alpha_composite(b, ((x0 + x1 - b.width) // 2, (y0 + y1 - h) // 2 + 1))
    out.convert("RGB").save(path, quality=90)
    print("patched", os.path.basename(path), (x0, y0, x1, y1))

for s in ("shot-question.webp", "shot-my-day.webp"):
    p = f"{IMG}/{s}"
    orig = os.path.expanduser(f"~/projects/qz-brand/shots-orig/{s}")    # the untouched capture, outside static/
    if not os.path.exists(orig):
        shutil.copy(p, orig)
    shutil.copy(orig, p); patch_shot(p)

# 4. the link preview
from playwright.sync_api import sync_playwright
F = os.path.abspath(f"{APP}/fonts")
html = f"""<html><head><meta charset="utf-8"><style>
@font-face{{font-family:J;font-weight:800;src:url(file://{F}/plus-jakarta-sans-latin-800-normal.woff2)}}
@font-face{{font-family:I;font-weight:500;src:url(file://{F}/inter-latin-500-normal.woff2)}}
html,body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#F7F8FC}}
.bg{{position:absolute;right:-210px;top:-150px;width:760px;height:930px;border-radius:50%;background:#E8E9FB}}
.l{{position:absolute;left:72px;top:72px;width:600px}}
.l img{{height:96px}}
h1{{font-family:J;font-weight:800;font-size:46px;line-height:1.2;letter-spacing:-.02em;color:#111827;margin:52px 0 0}}
p{{font-family:I;font-weight:500;font-size:29px;line-height:1.45;color:#5B6475;margin:22px 0 0}}
.b{{position:absolute;left:72px;bottom:56px;font-family:I;font-weight:500;font-size:29px;color:#4F46E5}}
.ph{{position:absolute;left:788px;top:26px;width:322px;height:578px;border-radius:40px;background:#111827;padding:11px;box-sizing:border-box;
 box-shadow:0 24px 60px rgba(17,24,39,.25)}}
.ph div{{width:100%;height:100%;border-radius:30px;overflow:hidden;background:url(file://{os.path.abspath(IMG)}/shot-question.webp) top/100% auto no-repeat}}
</style></head><body><div class="bg"></div><div class="l"><img src="file://{os.path.abspath(BRAND)}/wordmark.svg">
<h1>Daily practice your<br>children will actually do</h1><p>Maths, times tables, spelling, grammar<br>and science for Years 1 to 9 in England</p></div>
<div class="b">Founding families: free in the beta + 12 months after launch</div><div class="ph"><div></div></div></body></html>"""
open(f"{tmp}/og.html", "w").write(html)
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto(f"file://{tmp}/og.html"); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(300)
    pg.screenshot(path=f"{IMG}/og-preview.png"); b.close()
shutil.rmtree(tmp)
print("done")
