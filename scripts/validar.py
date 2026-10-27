#!/usr/bin/env python3
"""Valida os streams de canais.json e escreve estado.json (corre no GitHub Actions, sem PC/VPS)."""
import json
import urllib.request
from datetime import datetime, timezone, timedelta

LISBOA = timezone(timedelta(hours=1))  # WET/WINTER
UA_BASE = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

def testar(canal):
    req = urllib.request.Request(canal["url"])
    req.add_header("User-Agent", canal.get("ua", UA_BASE))
    if canal.get("referer"):
        req.add_header("Referer", canal["referer"])
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            bloco = r.read(200).decode("utf-8", "ignore")
        return bloco.lstrip().startswith("#EXTM3U")
    except Exception:
        return False

def main():
    with open("canais.json", encoding="utf-8") as f:
        canais = json.load(f)
    ok, mortos = [], []
    for c in canais:
        (ok if testar(c) else mortos).append(c["nome"])
        print(("OK      " if c["nome"] in ok else "MORTO   ") + c["nome"])
    estado = {
        "validado_em": datetime.now(LISBOA).isoformat(timespec="seconds"),
        "total": len(canais),
        "ok": ok,
        "mortos": mortos,
    }
    with open("estado.json", "w", encoding="utf-8") as f:
        json.dump(estado, f, ensure_ascii=False, indent=1)
    print(f"\n{len(ok)}/{len(canais)} canais vivos")

if __name__ == "__main__":
    main()
