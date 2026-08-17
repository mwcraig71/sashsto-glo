#!/usr/bin/env python3
"""
Repoint the whole site at a new URL and regenerate both QR codes.

    python3 set-url.py https://sashto-glow.onrender.com

Rewrites the canonical link, Open Graph tags, the visible URL on the page,
and the calendar file, then rebuilds qr_screen.png and qr_print.png.
Run it again any time the hostname changes; nothing else needs touching.
"""
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).parent
URL_RE = re.compile(r"https://(?:glow\.strinteg\.com|[a-z0-9-]+\.onrender\.com|strinteg\.com/glow)")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    url = sys.argv[1].rstrip("/")
    if not url.startswith("https://"):
        sys.exit("URL must start with https://")
    bare = url.replace("https://", "")

    for name in ("index.html", "glow-party.ics"):
        p = HERE / name
        if not p.exists():
            continue
        t = p.read_text()
        n = len(URL_RE.findall(t))
        t = URL_RE.sub(url, t)
        # the human-readable URL shown in the Share It block
        t = re.sub(r"<strong>[a-z0-9.\-/]+\.(?:com|app)[a-z0-9/\-]*</strong>",
                   f"<strong>{bare}</strong>", t)
        p.write_text(t)
        print(f"{name}: {n} URL references updated")

    try:
        import qrcode
        from qrcode.constants import ERROR_CORRECT_Q
    except ImportError:
        sys.exit("QR codes not regenerated - run: pip install qrcode")

    for name, box in (("qr_screen.png", 12), ("qr_print.png", 40)):
        q = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, box_size=box, border=4)
        q.add_data(url)
        q.make(fit=True)
        q.make_image(fill_color="#000000", back_color="#FFFFFF").convert("RGB").save(HERE / name)
        print(f"{name}: version {q.version}, {q.modules_count} modules")

    print(f"\nAll assets now point at {url}")
    if q.version > 4:
        print("WARNING: symbol is dense for a dark venue. Consider a shorter hostname.")


if __name__ == "__main__":
    main()
