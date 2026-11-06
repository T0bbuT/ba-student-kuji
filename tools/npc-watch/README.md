# 新しいNPCの確認（PCで手動実行）

Blue Archive Wiki の [Category:NPC](https://bluearchive.wiki/wiki/Category:NPC) を見て、まだ知らないページがあれば `NPCS` の下書き・画像・出典を入れた PR を作ります。マージは手動です。

GitHub Actions では動きません。Wiki（Miraheze）の Cloudflare のボット対策が、GitHub のサーバーからのアクセスに確認画面を返すためです（2026-11 時点）。なので、普通に Wiki が見られる PC から手動で実行します。

## 最初の準備（1回だけ）

1. [Python 3](https://www.python.org/downloads/)、[Git](https://git-scm.com/)、[GitHub CLI](https://cli.github.com/) を入れる。
2. ターミナル（PowerShell など）で:
   ```
   pip install pillow "opencv-python-headless<5"
   gh auth login
   git clone https://github.com/T0bbuT/ba-student-kuji.git
   ```

## 実行するとき

```
cd ba-student-kuji
python tools/npc-watch/run_local.py
```

- 新着が無ければ「新しいNPCはありませんでした。」で終わります。
- 新着があれば、`known.txt` を main に記録してから、下書きのブランチを push して PR を作ります。
- 確認だけしたいときは `python tools/npc-watch/run_local.py --dry-run`（何も変えません）。

## 中でやっていること

1. `check.py` が Wiki の API でカテゴリのページ一覧を取り、`known.txt`（もう見たページ）と比べる。
2. `draft.py` が新しいページごとに:
   - ページの `{{NPC}}` 欄から日本語名・名字・ふりがな・学園を読む。乗り物（`DevName` が `TSS_` で始まるもの）と、もう `NPCS` にある名前は外す。
   - 全身の立ち絵（`<ページ名>_01.png`、無ければ `_00.png`）を取得し、詳細用（高さ1400pxまで縮小）と、カード用（400×452、顔検出 lbpcascade_animeface で顔を中央に）の webp を作る。立ち絵が無ければ名前カード。
   - `index.html` の `NPCS` の末尾に行を足し（行末に「自動追加」と書く）、`images/npc/sources.csv` に出典を足す。
3. PR の説明には、キャラごとの画像と確認すべき点（初登場が空欄、衣装名が英語、顔が見つからなかった、など）が載る。

## 確認してマージするとき

- 初登場（`debut`）は Wiki に無いので必ず空欄。PR の画面（Files changed → index.html の「…」→ Edit file）で書き足す。
- 衣装違いの名前は「スズミ（Casual）」のように英語で入るので日本語にする。
- カード画像の顔の位置がずれていたら、画像を差し替えるか、`img` と `src` を消して名前カードにする。
- 要らないキャラは、その行と画像を消す。全部要らなければ PR を閉じるだけでよい（`known.txt` は記録済みなので次回は出ない）。
