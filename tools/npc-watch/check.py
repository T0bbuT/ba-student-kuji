#!/usr/bin/env python3
"""Blue Archive Wiki の Category:NPC を読み、known.txt に無いページを新着として報告する。

使い方:
  python3 tools/npc-watch/check.py            # 新着を表示し、known.txt を更新
  python3 tools/npc-watch/check.py --dry-run  # known.txt を更新しない

新着があれば new.json（タイトルと追加日時）を書き出し、GitHub Actions の出力 new_count を設定する。
"""
import json
import os
import sys
import urllib.parse

from wikihttp import fetch

API = "https://bluearchive.wiki/w/api.php"
CATEGORY = "Category:NPC"
HERE = os.path.dirname(os.path.abspath(__file__))
KNOWN = os.path.join(HERE, "known.txt")
NEW = os.path.join(HERE, "new.json")


def fetch_members():
    members, cont = [], {}
    while True:
        params = {
            "action": "query", "format": "json", "list": "categorymembers",
            "cmtitle": CATEGORY, "cmlimit": "500", "cmprop": "title|timestamp",
            "cmnamespace": "0", **cont,
        }
        data = json.loads(fetch(API + "?" + urllib.parse.urlencode(params), timeout=30))
        members += data["query"]["categorymembers"]
        if "continue" not in data:
            return members
        cont = {"cmcontinue": data["continue"]["cmcontinue"]}


def page_url(title):
    return "https://bluearchive.wiki/wiki/" + urllib.parse.quote(title.replace(" ", "_"))


def main():
    dry = "--dry-run" in sys.argv
    members = fetch_members()
    if not members:
        sys.exit("Category:NPC が空でした。Wiki 側の変更かもしれないので確認してください。")
    with open(KNOWN, encoding="utf-8") as f:
        known = {line.strip() for line in f if line.strip()}
    new = sorted((m for m in members if m["title"] not in known), key=lambda m: m["timestamp"])

    print(f"Category:NPC {len(members)} 件 / 既知 {len(known)} 件 / 新着 {len(new)} 件")
    for m in new:
        print(f"  + {m['title']}  ({m['timestamp'][:10]})")

    if new:
        with open(NEW, "w", encoding="utf-8") as f:
            json.dump(new, f, ensure_ascii=False, indent=1)
        if not dry:
            with open(KNOWN, "w", encoding="utf-8") as f:
                f.write("\n".join(sorted(known | {m["title"] for m in new})) + "\n")

    out = os.environ.get("GITHUB_OUTPUT")
    if out:
        with open(out, "a", encoding="utf-8") as f:
            f.write(f"new_count={len(new)}\n")


if __name__ == "__main__":
    main()
