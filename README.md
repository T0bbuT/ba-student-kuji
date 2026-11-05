# 生徒くじ

ブルーアーカイブの生徒をランダムに何人か表示する、非公式のファンツールです。二次創作のネタ出し用に作りました。

**▶ アプリを開く：https://t0bbut.github.io/ba-student-kuji/**

## 使い方

`index.html` をブラウザで開くだけで使えます（ビルド不要）。

- 「引く」またはスペースキーで、生徒をランダムに表示（1〜16人）
- 日本版で未実装の生徒も「未実装」バッジ付きで表示（含む／未実装だけ／含まない を切り替え可）
- 📌 で固定した生徒は、引き直しても残る
- カードを押すとプロフィールを表示
- 学園での絞り込み、衣装違いの表示切り替え
- ストーリーにだけ登場する未実装キャラ（ニヤニヤ教授、マルクトなど約60人）も画像付きで出る（画像がないキャラは名前カード）
- ほかのキャラも自分で追加して混ぜられる（ブラウザ内に保存）

## データについて

実装済み・実装予定の生徒のデータと画像は [SchaleDB](https://schaledb.com/) から、開いたときにブラウザで直接読み込んでいます（このリポジトリには含みません）。
SchaleDB 本体から読めない場合は、GitHub 上の SchaleDB の古いミラーを使います（新しい生徒や未実装の生徒が含まれません）。

ブルーアーカイブに関する権利は NEXON Games / Yostar に帰属します。本ツールは公式とは関係ありません。

## 未実装キャラの画像

`images/npc/` に `キャラ名.webp`（`.png` `.jpg` も可）を置くと、名前カードの代わりに画像が表示されます。対応するファイル名の一覧は [images/npc/README.md](images/npc/README.md) にあります。

## 画像の出典

`images/npc/` にある未実装キャラの画像（カード用・詳細用）は、[Blue Archive Wiki](https://bluearchive.wiki/) に掲載されている立ち絵をトリミング・縮小したものです。
詳細画面の「画像：Blue Archive Wiki」から、それぞれの元画像のページを開けます。元画像のURLとSHA256は [images/npc/sources.csv](images/npc/sources.csv) にまとめています。
画像の権利は NEXON Games / Yostar に帰属します。問題がある場合は Issue でお知らせください。すぐに削除します。

<details><summary>キャラごとの元画像（58枚）</summary>

| キャラ | 元画像 | 備考 |
|---|---|---|
| ユメ | [Yume_01.png](https://bluearchive.wiki/wiki/File:Yume_01.png) |  |
| コユキ（バニーガール） | [Koyuki_(Bunnysuit)_01.png](https://bluearchive.wiki/wiki/File:Koyuki_%28Bunnysuit%29_01.png) |  |
| チヒロ（キャンプ） | [Chihiro_(Camping)_01.png](https://bluearchive.wiki/wiki/File:Chihiro_%28Camping%29_01.png) |  |
| トキ（制服） | [Toki_(School_Uniform)_01.png](https://bluearchive.wiki/wiki/File:Toki_%28School_Uniform%29_01.png) |  |
| ミライ | [Mirai_01.png](https://bluearchive.wiki/wiki/File:Mirai_01.png) |  |
| ツバサ | [Tsubasa_01.png](https://bluearchive.wiki/wiki/File:Tsubasa_01.png) |  |
| マコト（ドレス） | [Makoto_(Dress)_01.png](https://bluearchive.wiki/wiki/File:Makoto_%28Dress%29_01.png) |  |
| イブキ（ドレス） | [Ibuki_(Dress)_01.png](https://bluearchive.wiki/wiki/File:Ibuki_%28Dress%29_01.png) |  |
| マユミ | [Mayumi_01.png](https://bluearchive.wiki/wiki/File:Mayumi_01.png) |  |
| カレン | [Karen_01.png](https://bluearchive.wiki/wiki/File:Karen_01.png) |  |
| ショウコ | [Shouko_01.png](https://bluearchive.wiki/wiki/File:Shouko_01.png) |  |
| クズノハ | [Kuzunoha_01.png](https://bluearchive.wiki/wiki/File:Kuzunoha_01.png) |  |
| アラタ | [Arata_01.png](https://bluearchive.wiki/wiki/File:Arata_01.png) |  |
| アヤメ | [Ayame_01.png](https://bluearchive.wiki/wiki/File:Ayame_01.png) |  |
| シュロ | [Shuro_01.png](https://bluearchive.wiki/wiki/File:Shuro_01.png) |  |
| コクリコ | [Kokuriko_01.png](https://bluearchive.wiki/wiki/File:Kokuriko_01.png) |  |
| アザミ | [Azami_01.png](https://bluearchive.wiki/wiki/File:Azami_01.png) |  |
| カグヤ | [Kaguya_01.png](https://bluearchive.wiki/wiki/File:Kaguya_01.png) |  |
| メル（温泉） | [Meru_(Hot_Spring)_diorama_01.png](https://bluearchive.wiki/wiki/File:Meru_%28Hot_Spring%29_diorama_01.png) | 小物・台座付きのdiorama画像。独立した直立ポーズではありません。 |
| ミスズ | [Misuzu_01.png](https://bluearchive.wiki/wiki/File:Misuzu_01.png) |  |
| ユキノ | [Yukino_01.png](https://bluearchive.wiki/wiki/File:Yukino_01.png) |  |
| マイア | [Maia_01.png](https://bluearchive.wiki/wiki/File:Maia_01.png) |  |
| スオウ | [Suou_01.png](https://bluearchive.wiki/wiki/File:Suou_01.png) |  |
| ミリア | [Akira_(Miria)_01.png](https://bluearchive.wiki/wiki/File:Akira_%28Miria%29_01.png) | 寮監隊姿。ユーザー指定のFandom掲載画像と同じ立ち絵。参照ページ：https://bluearchive.fandom.com/wiki/Kiyosumi_Akira |
| ヒロミ | [Hiromi_01.png](https://bluearchive.wiki/wiki/File:Hiromi_01.png) |  |
| ツムギ | [Tsumugi_01.png](https://bluearchive.wiki/wiki/File:Tsumugi_01.png) |  |
| スミカ | [Sumika_01.png](https://bluearchive.wiki/wiki/File:Sumika_01.png) |  |
| サユリ | [Sayuri_01.png](https://bluearchive.wiki/wiki/File:Sayuri_01.png) |  |
| マキナ | [Makina_01.png](https://bluearchive.wiki/wiki/File:Makina_01.png) |  |
| ミナト | [Minato_01.png](https://bluearchive.wiki/wiki/File:Minato_01.png) |  |
| アミ | [Ami_01.png](https://bluearchive.wiki/wiki/File:Ami_01.png) |  |
| ナナミ | [Nanami_01.png](https://bluearchive.wiki/wiki/File:Nanami_01.png) |  |
| ミツキ | [Mitsuki_01.png](https://bluearchive.wiki/wiki/File:Mitsuki_01.png) |  |
| サナエ | [Sanae_01.png](https://bluearchive.wiki/wiki/File:Sanae_01.png) |  |
| 連邦生徒会長 | [Student_Council_President_01.png](https://bluearchive.wiki/wiki/File:Student_Council_President_01.png) |  |
| リン | [Rin_01.png](https://bluearchive.wiki/wiki/File:Rin_01.png) |  |
| モモカ | [Momoka_01.png](https://bluearchive.wiki/wiki/File:Momoka_01.png) |  |
| カヤ | [Kaya_01.png](https://bluearchive.wiki/wiki/File:Kaya_01.png) |  |
| アユム | [Ayumu_01.png](https://bluearchive.wiki/wiki/File:Ayumu_01.png) |  |
| スモモ | [Sumomo_01.png](https://bluearchive.wiki/wiki/File:Sumomo_01.png) |  |
| アオイ | [Aoi_01.png](https://bluearchive.wiki/wiki/File:Aoi_01.png) |  |
| ハイネ | [Haine_01.png](https://bluearchive.wiki/wiki/File:Haine_01.png) |  |
| シノン | [Shinon_01.png](https://bluearchive.wiki/wiki/File:Shinon_01.png) |  |
| マイ | [Mai_01.png](https://bluearchive.wiki/wiki/File:Mai_01.png) |  |
| アキラ | [Akira_01.png](https://bluearchive.wiki/wiki/File:Akira_01.png) |  |
| カイ | [Kai_01.png](https://bluearchive.wiki/wiki/File:Kai_01.png) |  |
| アケミ | [Akemi_01.png](https://bluearchive.wiki/wiki/File:Akemi_01.png) |  |
| ニヤニヤ教授 | [Professor_Smug_01.png](https://bluearchive.wiki/wiki/File:Professor_Smug_01.png) |  |
| アイン | [Ein_01.png](https://bluearchive.wiki/wiki/File:Ein_01.png) |  |
| ソフ | [Sof_01.png](https://bluearchive.wiki/wiki/File:Sof_01.png) |  |
| オウル | [Ohr_01.png](https://bluearchive.wiki/wiki/File:Ohr_01.png) |  |
| マルクト | [Malkuth_01.png](https://bluearchive.wiki/wiki/File:Malkuth_01.png) |  |
| ジェネラル | [Kaiser_PMC_General_00.png](https://bluearchive.wiki/wiki/File:Kaiser_PMC_General_00.png) |  |
| デカルト | [Descartes_01.png](https://bluearchive.wiki/wiki/File:Descartes_01.png) |  |
| ソラ | [Sora_01.png](https://bluearchive.wiki/wiki/File:Sora_01.png) |  |
| アロナ | [Arona_01.png](https://bluearchive.wiki/wiki/File:Arona_01.png) |  |
| プラナ | [Plana_01.png](https://bluearchive.wiki/wiki/File:Plana_01.png) |  |
| 黒服 | [Black_Suit_00.png](https://bluearchive.wiki/wiki/File:Black_Suit_00.png) |  |

</details>
