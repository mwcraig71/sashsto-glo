# SASHTO 2026 Glow Party

Live at the Render URL. `glow.strinteg.com` is optional and can be added later
without invalidating anything already printed — Render keeps the `onrender.com`
hostname active after a custom domain is attached.

Static site. No build step. `index.html` is at the repo root.

## Deploy on Render

1. Push this folder to a new GitHub repo (Render static sites deploy from Git only —
   there is no ZIP or drag-and-drop upload).
2. Render Dashboard → **New** → **Static Site** → connect the repo.
3. Settings:
   - Build Command: *(leave blank)*
   - Publish Directory: `.`
4. Deploy. Note the assigned `*.onrender.com` URL.

## Changing the URL

    python3 set-url.py https://<whatever>.onrender.com

Rewrites the canonical link, Open Graph tags, the visible URL on the page, and the
calendar file, then regenerates both QR codes. Run it once right after you learn
the hostname Render assigns.

## Custom domain (optional, later)

1. Render → the site → **Settings** → **Custom Domains** → **Add Custom Domain** →
   `glow.strinteg.com`.
2. In Bluehost DNS for strinteg.com, add:

   | Type  | Host | Points to                  | TTL |
   |-------|------|----------------------------|-----|
   | CNAME | glow | `<yoursite>.onrender.com`  | 300 |

   Do not add an AAAA record — Render is IPv4 only and an AAAA will break
   certificate issuance. This record does not touch the WordPress site on the
   apex domain.
3. Back in Render, click **Verify**. TLS is provisioned automatically and HTTP
   redirects to HTTPS.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The page. Self-contained; only external dependency is Google Fonts. |
| `map.webp` / `map.jpg` / `map-sm.webp` | Dual-route map. `<picture>` serves the small one on phones. |
| `map.png` | Full-resolution master for print and slide use. |
| `qr_screen.png` | 444 px QR for the conference app push and on-screen use. |
| `qr_print.png` | 1480 px QR, good to ~5 in at 300 dpi, for signage and cards. |
| `glow-party.ics` | Calendar file with a 90-minute reminder. |

QR encodes whatever URL `set-url.py` was last run with at error correction level Q. Keep it black
on white — recoloring costs contrast, and it will be scanned in a dark venue.


## If you cannot reach Bluehost

The custom domain is a convenience, not a dependency. Deploy on the Render
hostname, run `set-url.py` against it, and print that QR. Everything works.
Add `glow.strinteg.com` whenever DNS access turns up; the printed code keeps
resolving because Render does not retire the `onrender.com` hostname.

Whoever administers Microsoft 365 for strinteg.com is the likely holder of the
Bluehost credentials — the domain's mail is on Outlook behind Barracuda, and
the same person or vendor usually set both up.

**If someone else edits Bluehost DNS, tell them to add only a CNAME on the
`glow` host.** Do not let anyone touch the existing A record (50.87.227.237),
the MX records, or the SPF TXT record. Breaking those takes down the website
or company email.
