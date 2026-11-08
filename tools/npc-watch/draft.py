#!/usr/bin/env python3
"""check.py が見つけた新着NPC（new.json）から、NPCS の下書き・画像・出典を作る。

  python3 tools/npc-watch/draft.py [--branch ブランチ名]

- Wiki のページの {{NPC}} 欄から日本語名・名字・ふりがな・学園を読む
- 立ち絵（<ページ名>_01.png → _00.png の順に探す）を取ってきて、
  カード用（400×452、顔検出で顔を中心に）と詳細用（高さ1400pxまで縮小）の webp を作る
- index.html の NPCS の末尾に1行ずつ足し、images/npc/sources.csv に出典を足す
- PR の説明文を pr_body.md に書き出す
画像の処理には Pillow と opencv-python-headless(<5) が要る。
"""
import csv
import hashlib
import io
import json
import os
import re
import sys
import urllib.parse
from datetime import date

import cv2
import numpy as np
from PIL import Image

from wikihttp import fetch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
INDEX = os.path.join(ROOT, "index.html")
NPC_DIR = os.path.join(ROOT, "images", "npc")
SOURCES = os.path.join(NPC_DIR, "sources.csv")
NEW = os.path.join(HERE, "new.json")
BODY = os.path.join(HERE, "pr_body.md")
CASCADE = os.path.join(HERE, "lbpcascade_animeface.xml")
CASCADE_URL = "https://raw.githubusercontent.com/nagadomi/lbpcascade_animeface/master/lbpcascade_animeface.xml"
API = "https://bluearchive.wiki/w/api.php"

CARD_W, CARD_H = 400, 452     # カード用（200:226）
PORTRAIT_MAX_H = 1400         # 詳細用（全身・トリミングしない）
# 既存58枚のカードから測った値：切り抜き幅＝顔の幅×2.05、上端＝顔の上端−顔の幅×0.57、顔の中心が左右中央
FACE_TO_CROP = 2.05
FACE_TOP_MARGIN = 0.57

SCHOOL_ALIAS = {"redwinter": "RedWinter", "wildhunt": "Wildhunt", "gsc": "Federal",
                "generalstudentcouncil": "Federal", "federalstudentcouncil": "Federal"}


def get(url, binary=False):
    data = fetch(url)
    return data if binary else json.loads(data)


def api(**params):
    return get(API + "?" + urllib.parse.urlencode({"format": "json", **params}))


def school_keys():
    m = re.search(r"const SCHOOL_JA = \{(.*?)\};", open(INDEX, encoding="utf-8").read())
    return re.findall(r"(\w+):", m.group(1)) if m else []


def to_school(wiki_value, keys):
    k = re.sub(r"[^a-z]", "", (wiki_value or "").lower())
    if not k:
        return "ETC"
    if k in SCHOOL_ALIAS:
        return SCHOOL_ALIAS[k]
    for key in keys:
        if key.lower() == k:
            return key
    return "ETC"


def npc_fields(wikitext):
    m = re.search(r"\{\{NPC\s*\n(.*?)\n\}\}", wikitext, re.S)
    if not m:
        return None
    fields = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"\s*\|\s*(\w+)\s*=(.*)", line)
        if mm:
            fields[mm.group(1)] = mm.group(2).strip()
    return fields


def file_slug(title):
    s = title.lower().replace("(", " ").replace(")", " ")
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "npc"


def find_sprite(title):
    base = title.replace(" ", "_")
    for name in (f"{base}_01.png", f"{base}_00.png"):
        j = api(action="query", prop="imageinfo", iiprop="url|size", titles="File:" + name)
        page = next(iter(j["query"]["pages"].values()))
        if page.get("imageinfo"):
            return name, page["imageinfo"][0]
    return None, None


def detect_face(rgba):
    if not os.path.exists(CASCADE):
        with open(CASCADE, "wb") as f:
            f.write(get(CASCADE_URL, binary=True))
    casc = cv2.CascadeClassifier(CASCADE)
    bg = Image.new("RGBA", rgba.size, (255, 255, 255, 255))
    bg.alpha_composite(rgba)
    gray = cv2.equalizeHist(cv2.cvtColor(np.array(bg.convert("RGB")), cv2.COLOR_RGB2GRAY))
    top = gray[: int(gray.shape[0] * 0.45)]  # 顔は上の方にあるはず
    faces = casc.detectMultiScale(top, 1.05, 3, minSize=(max(24, rgba.width // 20),) * 2)
    if len(faces) == 0:
        return None
    return max(faces, key=lambda r: r[2])


def make_images(png_bytes, slug):
    im = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    if im.height > PORTRAIT_MAX_H:
        im = im.resize((round(im.width * PORTRAIT_MAX_H / im.height), PORTRAIT_MAX_H), Image.LANCZOS)
    face = detect_face(im)
    if face is not None:
        fx, fy, fw, _ = face
        cw = fw * FACE_TO_CROP
        cx, top = fx + fw / 2, fy - fw * FACE_TOP_MARGIN
    else:
        # 顔が見つからないとき：不透明部分の上端・左右中央から、平均的な顔の大きさ（高さの13%）で切る
        l, t, r, _ = im.getchannel("A").getbbox() or (0, 0, im.width, im.height)
        cw = im.height * 0.13 * FACE_TO_CROP
        head = im.getchannel("A").crop((l, t, r, t + int(cw * 0.6))).getbbox()
        cx = l + ((head[0] + head[2]) / 2 if head else (r - l) / 2)
        top = t
    ch = cw * CARD_H / CARD_W
    box = tuple(round(v) for v in (cx - cw / 2, top, cx + cw / 2, top + ch))
    card = Image.new("RGBA", (box[2] - box[0], box[3] - box[1]), (0, 0, 0, 0))
    card.paste(im.crop((max(0, box[0]), max(0, box[1]), min(im.width, box[2]), min(im.height, box[3]))),
               (max(0, -box[0]), max(0, -box[1])))
    card = card.resize((CARD_W, CARD_H), Image.LANCZOS)
    card.save(os.path.join(NPC_DIR, "card", slug + ".webp"), "WEBP", quality=88, method=6)
    im.save(os.path.join(NPC_DIR, "portrait", slug + ".webp"), "WEBP", quality=88, method=6)
    return face is not None


def js(s):
    return json.dumps(s, ensure_ascii=False)


def main():
    branch = sys.argv[sys.argv.index("--branch") + 1] if "--branch" in sys.argv else ""
    with open(NEW, encoding="utf-8") as f:
        new = json.load(f)
    keys = school_keys()
    index = open(INDEX, encoding="utf-8").read()
    existing = set(re.findall(r'\{ name:"([^"]+)"', index))
    today = date.today().isoformat()
    added, skipped, lines, rows = [], [], [], []

    for m in new:
        title = m["title"]
        url = "https://bluearchive.wiki/wiki/" + urllib.parse.quote(title.replace(" ", "_"))
        try:
            wt = api(action="parse", page=title, prop="wikitext")["parse"]["wikitext"]["*"]
        except Exception as e:
            skipped.append((title, url, f"ページを読めませんでした（{e}）"))
            continue
        f = npc_fields(wt) or {}
        if re.search(r"\{\{\s*Unused content", wt, re.I) or re.search(r"\(unused", title, re.I):
            skipped.append((title, url, "未使用コンテンツ（ゲームに出ていない流出・没データ）なので外しました"))
            continue
        if f.get("DevName", "").startswith("TSS_"):
            skipped.append((title, url, "乗り物（戦術支援）のページなので外しました"))
            continue

        notes = []
        jp = f.get("PersonalNameJp", "").strip()
        outfit = re.search(r"\((.+)\)$", title)
        if not f:
            notes.append("Wiki に {{NPC}} 欄が無いので、名前・学園は仮です")
        if not jp:
            jp = re.sub(r"\s*\(.*\)$", "", title)
            notes.append(f"日本語名が Wiki に無いので英語名「{jp}」のままです")
        name = jp
        if outfit:
            name += f"（{outfit.group(1)}）"
            notes.append(f"衣装名「{outfit.group(1)}」を日本語にしてください")
        if name in existing:
            skipped.append((title, url, f"「{name}」はもう NPCS にあります"))
            continue

        entry = {"name": name}
        if f.get("FamilyNameJp"):
            entry["family"] = f["FamilyNameJp"]
        if f.get("FamilyNameRubyJp"):
            entry["ruby"] = f["FamilyNameRubyJp"]
        entry["school"] = to_school(f.get("School"), keys)
        if entry["school"] == "ETC" and f.get("School"):
            notes.append(f"学園「{f['School']}」に当てはまるキーが無いので ETC にしました")
        entry["debut"] = ""
        notes.append("初登場（debut）を書いてください")

        sprite, info, face = None, None, None
        try:
            sprite, info = find_sprite(title)
            if sprite:
                png = get(info["url"], binary=True)
                slug = file_slug(title)
                face = make_images(png, slug)
                entry["img"], entry["src"] = slug, sprite
                rows.append([name, slug + ".webp", sprite, info["width"], info["height"],
                             "https://bluearchive.wiki/wiki/File:" + urllib.parse.quote(sprite, safe="()"), info["url"],
                             hashlib.sha256(png).hexdigest(), f"自動追加 {today}"])
                if not face:
                    notes.append("顔が見つからなかったので、カード画像の位置を確認してください")
            else:
                notes.append("全身の立ち絵（_01.png / _00.png）が無いので名前カードになります")
        except Exception as e:
            notes.append(f"画像を取れませんでした（{e}）。名前カードになります")
            entry.pop("img", None)
            entry.pop("src", None)

        body = ", ".join(f"{k}:{js(v)}" for k, v in entry.items())
        lines.append(f"  {{ {body} }}, // 自動追加 {today}（{title}）")
        existing.add(name)
        added.append((title, url, entry, notes, face))

    if lines:
        start = index.index("const NPCS = [")
        end = index.index("\n];", start)
        index = index[:end] + "\n" + "\n".join(lines) + index[end:]
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(index)
    if rows:
        with open(SOURCES, "a", encoding="utf-8", newline="") as f:
            csv.writer(f, quoting=csv.QUOTE_ALL, lineterminator="\n").writerows(rows)

    raw = f"https://github.com/T0bbuT/ba-student-kuji/blob/{branch}/images/npc/card/" if branch else ""
    out = ["Blue Archive Wiki の [Category:NPC](https://bluearchive.wiki/wiki/Category:NPC) に新しいページが見つかったので、`NPCS` の下書きを自動で作りました。", ""]
    if added:
        out += ["## 追加したキャラ", "", "| 画像 | 名前 | 学園 | 確認すること |", "|---|---|---|---|"]
        for title, url, e, notes, face in added:
            img = f'<img src="{raw}{e["img"]}.webp?raw=true" width="100">' if raw and e.get("img") else "（名前カード）"
            out.append(f"| {img} | [{e['name']}]({url}) | {e['school']} | {'<br>'.join(notes)} |")
        out += ["", "初登場（`debut`）は Wiki に無いので空欄です。`index.html` の該当行（末尾に「自動追加」と書いた行）を直してからマージしてください。",
                "要らないキャラは、その行と画像を消すか、PR ごと閉じてください。閉じても次回からは通知されません。"]
    if skipped:
        out += ["", "## 入れなかったページ", ""] + [f"- [{t}]({u})：{why}" for t, u, why in skipped]
    with open(BODY, "w", encoding="utf-8") as f:
        f.write("\n".join(out) + "\n")
    print(f"追加 {len(added)} 件 / 見送り {len(skipped)} 件")
    gh = os.environ.get("GITHUB_OUTPUT")
    if gh:
        with open(gh, "a", encoding="utf-8") as f:
            f.write(f"added_count={len(added)}\n")


if __name__ == "__main__":
    main()
