#!/usr/bin/env python3
"""
幫「已經存在」的題目追加明測 (sample) 或暗測 (hidden) 測資組。

跟 new_problem.py 的差異：這支腳本的 --samples / --hidden 是「追加幾組」，
不是「總共要幾組」。會自動偵測目前 testdata/ 底下該類型最大的編號，
接著往後新增，完全不會動到既有的檔案，也不需要你自己去算現在有幾組。

用法：
    # 用題號找（不論資料夾是 010 還是 010_buy_snacks 都找得到）
    ./scripts/add_testdata.py 10 --samples 2
    ./scripts/add_testdata.py 10 --hidden 1

    # 也可以直接給資料夾路徑
    ./scripts/add_testdata.py problems/010_buy_snacks --samples 2 --hidden 1

範例：題目 010 目前有 sample_01~03、hidden_01~03，
執行 `./scripts/add_testdata.py 10 --samples 2 --hidden 1` 後，
會新增 sample_04、sample_05、hidden_04，01~03 完全不受影響。
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _lib  # noqa: E402


def parse_args():
    parser = argparse.ArgumentParser(
        description="幫既有題目追加明測/暗測測資組（追加語意，不是總數語意）"
    )
    parser.add_argument(
        "target",
        help="題號（例如 10）或題目資料夾路徑（例如 problems/010_buy_snacks）",
    )
    parser.add_argument("--samples", type=int, default=0, help="要追加幾組明測，預設 0")
    parser.add_argument("--hidden", type=int, default=0, help="要追加幾組暗測，預設 0")
    return parser.parse_args()


# def resolve_problem_dir(target: str) -> Path:
#     # 先試著當成題號解析；不是整數的話就當成路徑處理
#     try:
#         number = int(target)
#     except ValueError:
#         path = Path(target)
#         if not path.is_absolute():
#             path = _lib.PROJECT_ROOT / path
#         if not path.exists():
#             _lib.die(f"找不到題目資料夾：{path}")
#         return path

#     problem_dir = _lib.find_problem_dir(number)
#     if problem_dir is None:
#         _lib.die(
#             f"找不到題號 {number:03d} 對應的資料夾，"
#             f"請確認 problems/ 底下是否有 {number:03d} 或 {number:03d}_xxx，"
#             f"或先用 new_problem.py 建立這一題。"
#         )
#     return problem_dir


def main() -> None:
    args = parse_args()
    if args.samples < 0 or args.hidden < 0:
        _lib.die("--samples / --hidden 必須是不小於 0 的整數")
    if args.samples == 0 and args.hidden == 0:
        _lib.die("請至少指定 --samples 或 --hidden 其中一個要大於 0，否則沒有東西可以追加")

    # problem_dir = resolve_problem_dir(args.target)
    problem_dir = _lib.resolve_problem_dir(args.target)
    print(f"追加測資：{problem_dir.relative_to(_lib.PROJECT_ROOT)}/testdata/")

    if args.samples:
        _lib.add_cases(problem_dir, "sample", args.samples)
    if args.hidden:
        _lib.add_cases(problem_dir, "hidden", args.hidden)

    print("完成。")


if __name__ == "__main__":
    main()