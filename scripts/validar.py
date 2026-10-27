#!/usr/bin/env python3
"""Valida os streams de canais.json e escreve estado.json (corre no GitHub Actions, fora de PT).
Os streams PT fazem geo-block: 403/451 fora de Portugal = canal provavelmente VIVO em PT.
Só 404/erros de ligação = morto a sério."""
import gzip
import json
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta

LISBOA = timezone(timedelta(hours=1))  # WET/WINTER
UA_BASE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
GEO_CODES = {403, 451}

def testar(canal):
    """Devolve 'ok', 'geo' ou 'morto'."""
    req = urllib.request.Request(canal["url"])
    req.add_header("User-Agent", canal.get("ua", UA_BASE))
    if canal.get("referer"):
        req.add_header("Referer", canal["referer"])
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            cru = r.read(200)
        if cru[:2] == b"\x1f\x8b":  # resposta gzip
            cru = gzip.decompress(cru)
        bloco = cru.decode("utf-8", "ignore")
        return "ok" if bloco.lstrip().startswith("#EXTM3U") else "morto"
    except urllib.error.HTTPError as e:
        return "geo" if e.code in GEO_CODES else "morto"
    except Exception:
        return "morto"

def main():
    with open("canais.json", encoding="utf-8") as f:
        canais = json.load(f)
    ok, geo, mortos = [], [], []
    for c in canais:
        r = testar(c)
        {"ok": ok, "geo": geo, "morto": mortos}[r].append(c["nome"])
        print(f"{r.upper():5}  {c['nome']}")
    estado = {
        "validado_em": datetime.now(LISBOA).isoformat(timespec="seconds"),
        "validado_de": "GitHub Actions (fora de PT)",
        "total": len(canais),
        "ok": ok,
        "geo_bloqueados_vivos_em_pt": geo,
        "mortos": mortos,
    }
    with open("estado.json", "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=1)
    vivos = len(ok) + len(geo)
    print(f"\n{vivos}/{len(canais)} canais vivos em PT ({len(ok)} confirmados, {len(geo)} geo-bloqueados ao teste)")

if __name__ == "__main__":
    main()
