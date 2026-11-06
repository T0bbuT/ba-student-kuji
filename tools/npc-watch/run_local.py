#!/usr/bin/env python3
"""PC で新しいNPCを確認し、あれば下書きPRを作る（手動で実行する用）。

  python tools/npc-watch/run_local.py            # 確認して、新着があれば PR を作る
  python tools/npc-watch/run_local.py --dry-run  # 新着の確認だけ（何も変えない）

必要なもの: Python 3、Git、GitHub CLI（gh、`gh auth login` 済み）、
           `pip install pillow "opencv-python-headless<5"`
リポジトリのフォルダの中ならどこから実行してもよい。
"""
import json
import os
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
PY = sys.executable


def run(*cmd, check=True, capture=False):
    print("$", " ".join(cmd))
    r = subprocess.run(cmd, cwd=ROOT, check=check, text=True, encoding="utf-8",
                       stdout=subprocess.PIPE if capture else None)
    return r.stdout.strip() if capture else r.returncode


def main():
    dry = "--dry-run" in sys.argv
    if dry:
        run(PY, os.path.join(HERE, "check.py"), "--dry-run")
        return

    if run("git", "status", "--porcelain", capture=True):
        sys.exit("まだコミットしていない変更があります。先にコミットするか退避してから実行してください。")
    run("git", "switch", "main")
    run("git", "pull", "--ff-only", "origin", "main")

    new_json = os.path.join(HERE, "new.json")
    if os.path.exists(new_json):
        os.remove(new_json)
    run(PY, os.path.join(HERE, "check.py"))
    if not os.path.exists(new_json):
        print("新しいNPCはありませんでした。")
        return
    with open(new_json, encoding="utf-8") as f:
        count = len(json.load(f))

    # 既知リストは main に直接記録する（PR を閉じても次回から通知しないため）
    run("git", "add", "tools/npc-watch/known.txt")
    run("git", "commit", "-m", "NPC既知リストを更新")
    run("git", "push", "origin", "main")

    branch = "npc-watch/" + datetime.now().strftime("%Y%m%d-%H%M")
    run("git", "switch", "-c", branch)
    run(PY, os.path.join(HERE, "draft.py"), "--branch", branch)
    if not run("git", "status", "--porcelain", "--", "index.html", "images/npc", capture=True):
        print(f"新しいページは {count} 件ありましたが、追加するキャラはありませんでした（乗り物や既存キャラなど）。")
        print("内容は tools/npc-watch/pr_body.md を見てください。")
        run("git", "switch", "main")
        run("git", "branch", "-D", branch)
        return
    run("git", "add", "index.html", "images/npc")
    run("git", "commit", "-m", "新しいNPCの下書きを追加")
    run("git", "push", "-u", "origin", branch)
    run("gh", "pr", "create", "--base", "main", "--head", branch,
        "--title", f"新しいNPCの下書き（{datetime.now():%Y-%m-%d}）",
        "--body-file", os.path.join(HERE, "pr_body.md"))
    run("git", "switch", "main")
    print("PR を作りました。GitHub で画像と名前を確認してからマージしてください。")


if __name__ == "__main__":
    main()
