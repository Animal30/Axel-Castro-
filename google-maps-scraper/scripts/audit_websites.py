#!/usr/bin/env python3
"""Audit each lead's website and rank the leads whose site is missing, broken or outdated.

Reads a lead CSV from scrape.py (needs a `website` column), visits every site once and adds:
  web_estado   ok | sin web | solo redes | caída | error | en construcción
  web_puntaje  0-100, higher = worse site = better prospect for selling a new one
  web_motivos  the problems found, in Spanish, ready to use on a sales call
  web_https, web_mobile, web_copyright, web_segundos

Usage:   python3 scripts/audit_websites.py results-<id>.csv [--out prospectos.csv] [--min-score 30]
Plain HTTP and regex only: no LLM tokens, no dependencies.
"""
import argparse, csv, datetime, re, ssl, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
THIS_YEAR = datetime.date.today().year
SOCIAL_HOSTS = ("facebook.com", "instagram.com", "wa.me", "whatsapp.com", "linktr.ee", "tiktok.com",
                "linkedin.com", "twitter.com", "x.com", "youtube.com", "mercadolibre.com", "mercadoshops.com")
FREE_BUILDERS = (".wixsite.com", ".blogspot.", ".wordpress.com", ".webnode.", ".jimdosite.com",
                 ".jimdo.com", ".site123.me", ".negocio.site", ".business.site", ".godaddysites.com",
                 ".weebly.com", ".mitiendanube.com")
PARKED = re.compile(r"en construcci[oó]n|under construction|coming soon|pr[oó]ximamente|"
                    r"domain (is )?for sale|dominio (est[aá] )?en venta|buy this domain|"
                    r"this domain (has expired|is parked)|parked (free|domain)|sitio en mantenimiento", re.I)
COPYRIGHT = re.compile(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*[-–]\s*)?((?:19|20)\d{2})", re.I)
VIEWPORT = re.compile(r"<meta[^>]+name=[\"']viewport[\"']", re.I)
OLD_JQUERY = re.compile(r"jquery[.-]?(1\.\d+|2\.\d+)(?:\.\d+)?(?:\.min)?\.js", re.I)
TAG_TEXT = re.compile(r"<script.*?</script>|<style.*?</style>|<[^>]+>", re.S | re.I)


def norm(url):
    url = (url or "").strip()
    if url and not url.startswith(("http://", "https://")):
        url = "http://" + url
    return url


def fetch(url, verify=True, timeout=12):
    ctx = ssl.create_default_context() if verify else ssl._create_unverified_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,*/*",
                                               "Accept-Language": "es-AR,es;q=0.9,en;q=0.8"})
    t = time.time()
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as r:
        html = r.read(600_000).decode(r.headers.get_content_charset() or "utf-8", "replace")
        return r.status, r.geturl(), html, time.time() - t


def audit(row):
    url = norm(row.get("website"))
    out = {"web_estado": "", "web_puntaje": 0, "web_motivos": "", "web_https": "", "web_mobile": "",
           "web_copyright": "", "web_segundos": ""}
    reasons, score = [], 0

    def done(estado):
        out.update(web_estado=estado, web_puntaje=min(score, 100), web_motivos="; ".join(reasons))
        return out

    if not url:
        reasons.append("no tiene sitio web")
        score = 100
        return done("sin web")
    host = (urllib.parse.urlparse(url).hostname or "").lower()
    if any(host == h or host.endswith("." + h) for h in SOCIAL_HOSTS):
        reasons.append("en Google figura una red social o un link, no una web propia")
        score = 90
        return done("solo redes")

    cert_ok = True
    try:
        status, final, html, secs = fetch(url)
    except Exception as e:
        err = getattr(e, "reason", e)
        if isinstance(err, ssl.SSLError) or "CERTIFICATE" in str(err).upper():
            cert_ok = False
            try:
                status, final, html, secs = fetch(url, verify=False)
            except Exception as e2:
                reasons.append(f"la web no carga ({short(e2)})")
                score = 95
                return done("caída")
        elif isinstance(e, urllib.error.HTTPError):
            reasons.append(f"la web devuelve error {e.code}")
            score = 90 if e.code >= 500 or e.code == 404 else 70
            return done("error")
        else:
            reasons.append(f"la web no carga ({short(e)})")
            score = 95
            return done("caída")

    final_host = (urllib.parse.urlparse(final).hostname or "").lower()
    if any(final_host == h or final_host.endswith("." + h) for h in SOCIAL_HOSTS):
        reasons.append("la web redirige a una red social")
        score = 85
        return done("solo redes")

    text = re.sub(r"\s+", " ", TAG_TEXT.sub(" ", html)).strip()
    if PARKED.search(text[:5000]) or len(text) < 150:
        reasons.append("la web está en construcción, vacía o el dominio está estacionado")
        score = 90
        return done("en construcción")

    https = final.startswith("https://") and cert_ok
    out["web_https"] = "sí" if https else "no"
    if not cert_ok:
        reasons.append("certificado de seguridad inválido (el navegador muestra 'no seguro')"); score += 30
    elif not final.startswith("https://"):
        reasons.append("sin HTTPS (el navegador la marca como 'no segura')"); score += 25

    mobile = bool(VIEWPORT.search(html))
    out["web_mobile"] = "sí" if mobile else "no"
    if not mobile:
        reasons.append("no está adaptada a celulares"); score += 30

    years = [int(y) for y in COPYRIGHT.findall(html) if int(y) <= THIS_YEAR]
    if years:
        y = max(years)
        out["web_copyright"] = y
        if THIS_YEAR - y >= 3:
            reasons.append(f"el pie dice © {y}, parece abandonada"); score += 20 if THIS_YEAR - y < 6 else 30

    m = OLD_JQUERY.search(html)
    if m:
        reasons.append(f"usa tecnología vieja (jQuery {m.group(1)})"); score += 10
    if re.search(r"\.swf\b|<frameset|<marquee|<font\s", html, re.I):
        reasons.append("usa código de los 2000 (Flash, frames o <font>)"); score += 20
    if not re.search(r"<title>\s*\S", html, re.I):
        reasons.append("no tiene título (mal para Google)"); score += 5
    if not re.search(r"<meta[^>]+name=[\"']description[\"']", html, re.I):
        reasons.append("sin descripción para Google"); score += 5
    if any(b in final_host for b in FREE_BUILDERS):
        reasons.append("hecha con un constructor gratis y sin dominio propio"); score += 20
    if not re.search(r"wa\.me/|api\.whatsapp\.com|whatsapp", html, re.I):
        reasons.append("no tiene botón de WhatsApp"); score += 5

    out["web_segundos"] = round(secs, 1)
    if secs > 6:
        reasons.append(f"tarda {secs:.0f} s en cargar"); score += 15
    elif secs > 3:
        reasons.append(f"carga lenta ({secs:.0f} s)"); score += 5

    if status >= 400:
        reasons.append(f"la web devuelve error {status}"); score += 40
    return done("ok")


def short(e):
    s = str(getattr(e, "reason", e))
    if "timed out" in s or "timeout" in s.lower():
        return "no responde"
    if "Name or service not known" in s or "getaddrinfo" in s or "nodename" in s:
        return "el dominio no existe o venció"
    if "refused" in s.lower():
        return "conexión rechazada"
    return s[:60]


def main():
    ap = argparse.ArgumentParser(description="Rank leads by how bad their website is.")
    ap.add_argument("csv", help="lead CSV from scrape.py (needs a 'website' column)")
    ap.add_argument("--out", help="output CSV (default: <input>-auditado.csv)")
    ap.add_argument("--min-score", type=int, default=0,
                    help="keep only leads with web_puntaje >= this (e.g. 30 = only bad sites)")
    ap.add_argument("--workers", type=int, default=8)
    a = ap.parse_args()

    with open(a.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if rows and "website" not in rows[0]:
        sys.exit("✗ The CSV has no 'website' column.")
    print(f"▶ Auditing {len(rows)} websites…")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        for i, (r, res) in enumerate(zip(rows, ex.map(audit, rows)), 1):
            r.update(res)
            print(f"\r  {i}/{len(rows)}", end="", flush=True)
    print()

    rows.sort(key=lambda r: -r["web_puntaje"])
    kept = [r for r in rows if r["web_puntaje"] >= a.min_score]
    out = a.out or re.sub(r"\.csv$", "", a.csv) + "-auditado.csv"
    cols = list(rows[0].keys()) if rows else ["website"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(kept)

    counts = {}
    for r in rows:
        counts[r["web_estado"]] = counts.get(r["web_estado"], 0) + 1
    print("✓ " + ", ".join(f"{k}: {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1])))
    print(f"  {len(kept)} leads saved → {out} (worst sites first)")
    for r in kept[:8]:
        print(f"  • [{r['web_puntaje']:>3}] {r.get('title','')} | {r.get('phone','')} | {r['web_motivos'][:90]}")


if __name__ == "__main__":
    main()
