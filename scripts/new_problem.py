#!/usr/bin/env python3
"""
建立新題目的鷹架 (scaffold)。

用法：
    ./scripts/new_problem.py 10
    ./scripts/new_problem.py 10 buy_books
    python3 scripts/new_problem.py 10 --samples 3 --hidden 3

會在 problems/ 底下建立：

    problems/<編號>[_名稱]/
        problem.md              (空白，之後手動填題目敘述)
        solution.py              (空白，之後手動填參考解答)
        testdata/
            sample_01.in / .out  ┐
            sample_02.in / .out  ├─ 明測，共 --samples 組 (預設 3)
            sample_03.in / .out  ┘
            hidden_01.in / .out  ┐
            hidden_02.in / .out  ├─ 暗測，共 --hidden 組 (預設 3)
            hidden_03.in / .out  ┘

所有檔案內容都是空白，之後自行填入即可。

這支腳本只負責「從無到有」建立一題的骨架；日後想幫已經存在的題目
再多加幾組明測/暗測，請改用 add_testdata.py（語意是「追加」而不是「總數」）。

安全性：
    - 已存在的檔案「不會被覆蓋」。
    - 若同一個題號已經用別的名稱建立過資料夾，會直接中止並提示，避免同一題號重複建立。
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _lib  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(
        description="建立新題目的鷹架（資料夾、空白 problem.md / solution.py、空白測資檔）"
    )
    parser.add_argument("number", type=int, help="題號，例如 10")
    parser.add_argument(
        "name",
        nargs="?",
        default=None,
        help="選填，題目的英文/拼音名稱，例如 buy_books；"
        "不給的話資料夾只會用補零後的題號命名",
    )
    parser.add_argument(
        "--samples", type=int, default=3, help="明測 (sample) 組數，預設 3"
    )
    parser.add_argument(
        "--hidden", type=int, default=3, help="暗測 (hidden) 組數，預設 3"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.number < 0:
        _lib.die("題號必須是不小於 0 的整數")
    if args.samples < 0 or args.hidden < 0:
        _lib.die("--samples / --hidden 必須是不小於 0 的整數")

    padded = f"{args.number:03d}"
    folder_name = f"{padded}_{args.name}" if args.name else padded

    existing = _lib.find_problem_dir(args.number)
    if existing is not None and existing.name != folder_name:
        _lib.die(
            f"題號 {padded} 已經存在 problems/{existing.name}/ 了，"
            f"若這是不同題目請換一個題號；若是同一題，"
            f"請直接用既有資料夾名稱再跑一次這支腳本，"
            f"或改用 add_testdata.py 追加測資。"
        )

    problem_dir = _lib.PROBLEMS_DIR / folder_name
    print(f"建立題目鷹架：problems/{folder_name}/")

    _lib.touch(problem_dir / "problem.md")
    _lib.touch(problem_dir / "solution.py")

    # 全新資料夾，testdata 底下還沒有任何檔案，
    # 所以 add_cases 會直接從 01 開始建立，效果等同於原本「建立 N 組」的行為。
    _lib.add_cases(problem_dir, "sample", args.samples)
    _lib.add_cases(problem_dir, "hidden", args.hidden)

    print("完成。")


if __name__ == "__main__":
    main()