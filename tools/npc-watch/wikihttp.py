"""Blue Archive Wiki への HTTP アクセス（check.py と draft.py で共用）。

失敗したときは、原因を調べられるように応答のヘッダーと本文の先頭をログに出す。
"""
import sys
import urllib.error
import urllib.request

UA = "ba-student-kuji-npc-watch/1.1 (+https://github.com/T0bbuT/ba-student-kuji)"


def fetch(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except urllib.error.HTTPError as e:
        try:
            body = e.read()[:600]
        except Exception:
            body = b""
        hdrs = dict(e.headers.items()) if e.headers else {}
        print(f"[wikihttp] HTTP {e.code} {url[:150]}\n  headers={hdrs}\n  body={body!r}", file=sys.stderr)
        raise
