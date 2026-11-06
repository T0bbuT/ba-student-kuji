# 新しいNPCの自動確認

GitHub Actions（`.github/workflows/npc-watch.yml`）が毎週月曜 9:00 に動き、新しいNPCが見つかったら下書きPRを作ります。マージは手動です。

## 流れ

1. `check.py` が Blue Archive Wiki の API で [Category:NPC](https://bluearchive.wiki/wiki/Category:NPC) のページ一覧を取得し、`known.txt`（もう見たページ）と比べる。
2. 新しいページがあれば、`known.txt` に足して main にコミットする。PR を閉じても、次回から同じページは通知されない。
3. `draft.py` が新しいページごとに:
   - ページの `{{NPC}}` 欄から日本語名・名字・ふりがな・学園を読む。乗り物（`DevName` が `TSS_` で始まるもの）と、もう `NPCS` にある名前は外す。
   - 全身の立ち絵（`<ページ名>_01.png`、無ければ `_00.png`）を取得し、詳細用（高さ1400pxまで縮小）と、カード用（400×452、顔検出 lbpcascade_animeface で顔を中央に）の webp を作る。立ち絵が無ければ名前カード。
   - `index.html` の `NPCS` の末尾に行を足し（行末に「自動追加」と書く）、`images/npc/sources.csv` に出典を足す。
4. PR を作る。説明には、キャラごとの画像と確認すべき点（初登場が空欄、衣装名が英語、顔が見つからなかった、など）が載る。

## 確認してマージするとき

- 初登場（`debut`）は Wiki に無いので必ず空欄。PR の画面（Files changed → index.html の「…」→ Edit file）で書き足す。
- 衣装違いの名前は「スズミ（Casual）」のように英語で入るので日本語にする。
- カード画像の顔の位置がずれていたら、画像を差し替えるか、`img` と `src` を消して名前カードにする。
- 要らないキャラは、その行と画像を消す。全部要らなければ PR を閉じるだけでよい。

## 手動で動かす

Actions タブ →「新しいNPCの確認」→ Run workflow。

ローカルなら `python3 tools/npc-watch/check.py --dry-run` で新着の確認だけできます（`known.txt` は更新しない）。

## 初回に必要な設定

Actions が PR を作れるように、リポジトリの Settings → Actions → General → Workflow permissions で
「Allow GitHub Actions to create and approve pull requests」にチェックを入れてください。
