#!/usr/bin/env python3
"""
檢查某一題「全部測資」（明測 + 暗測合起來）對 solution.py 造成的
Statement Coverage（一般俗稱的 Instruction Coverage）與 Branch Coverage
各自能跑到多少。

【為什麼不能直接用 pytest-cov？】
本專案的測試框架（tests/test_problems.py）是用 subprocess 開一個全新的
Python 行程去執行 solution.py（見那支檔案裡的說明：這樣才能不管解答內部
用 input() 還是 sys.stdin.read() 都能測，且行程互相隔離）。
pytest-cov／coverage.py 預設只會追蹤「自己這個 process 內」執行到的程式碼，
子行程裡發生的事，母行程裡的 pytest --cov 是看不到的
（實測過：用 `pytest --cov=solution.py` 直接測，會出現
"Module was never imported" / "No data was collected"）。

【怎麼解？】
pytest-cov 本身也只是包了一層 coverage.py，所以這裡不透過 pytest 這層，
直接呼叫 coverage.py 本人：把「執行 solution.py」這個動作換成
`python -m coverage run --branch --append solution.py`，每一筆測資都這樣跑一次，
覆蓋率資料就會一直累加進同一份 .coverage 資料檔，最後統一產生報表。
這跟 pytest-cov 底層用的是同一顆引擎，只是換一種方式驅動它。

用法：
    ./scripts/check_coverage.py 1
    ./scripts/check_coverage.py 001_buy_books
    ./scripts/check_coverage.py problems/001_buy_books

    # 自訂及格門檻（百分比），預設兩者都要 100
    ./scripts/check_coverage.py 1 --fail-under-stmt 90 --fail-under-branch 80

    # 額外產生 HTML 報表，方便瀏覽器打開逐行檢視哪裡沒被測到
    ./scripts/check_coverage.py 1 --html

需要先安裝 coverage（在 requirements-dev.txt 裡）：
    pip install -r requirements-dev.txt
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _lib  # noqa: E402

COVERAGERC = _lib.PROJECT_ROOT / ".coveragerc"


def parse_args():
    parser = argparse.ArgumentParser(
        description="檢查某一題全部測資合起來對 solution.py 的 Statement / Branch Coverage"
    )
    parser.add_argument("target", help="題號、資料夾名稱，或 problems/xxx 路徑")
    parser.add_argument(
        "--fail-under-stmt",
        type=float,
        default=100.0,
        help="Statement (Instruction) coverage 及格門檻，百分比，預設 100",
    )
    parser.add_argument(
        "--fail-under-branch",
        type=float,
        default=100.0,
        help="Branch coverage 及格門檻，百分比，預設 100",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="額外產生 HTML 報表 htmlcov_<題目資料夾名稱>/index.html",
    )
    return parser.parse_args()


def run_one_case(solution_path: Path, in_file: Path, data_file: Path) -> subprocess.CompletedProcess:
    """用 coverage run 包裝一次 solution.py 的執行，覆蓋率資料 append 進 data_file。"""
    return subprocess.run(
        [
            sys.executable, "-m", "coverage", "run",
            f"--rcfile={COVERAGERC}",
            "--branch",
            "--append",
            f"--data-file={data_file}",
            str(solution_path),
        ],
        input=in_file.read_text(encoding="utf-8"),
        capture_output=True,
        text=True,
        timeout=_lib.TIMEOUT_SECONDS,
    )


def find_file_entry(report: dict, solution_path: Path) -> dict:
    """coverage.py 的 JSON 報表用『執行當下傳入的路徑字串』當 key，
    這裡做一次容錯：先直接比對絕對路徑，比不到的話、如果報表裡就只有
    這一個檔案，就直接拿那一筆，避免因為路徑字串格式差異而找不到。
    """
    files = report["files"]
    abs_str = str(solution_path.resolve())
    for key, entry in files.items():
        if str(Path(key).resolve()) == abs_str:
            return entry
    if len(files) == 1:
        return next(iter(files.values()))
    _lib.die(f"在 coverage 報表裡找不到 {solution_path}，報表內的檔案：{list(files.keys())}")


def main() -> None:
    args = parse_args()
    problem_dir = _lib.resolve_problem_dir(args.target)
    solution_path = problem_dir / "solution.py"
    if not solution_path.exists():
        _lib.die(f"找不到 {solution_path}")

    if shutil.which("coverage") is None:
        try:
            subprocess.run(
                [sys.executable, "-m", "coverage", "--version"],
                check=True, capture_output=True,
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            _lib.die(
                "找不到 coverage 套件，請先安裝："
                "pip install -r requirements-dev.txt（或 pip install coverage）"
            )

    cases = _lib.discover_cases(problem_dir)
    if not cases:
        _lib.die(f"{problem_dir} 底下 testdata/ 沒有找到任何成對的 .in/.out")

    rel_solution = solution_path.relative_to(_lib.PROJECT_ROOT)
    print(f"對象：{rel_solution}")
    print(f"共 {len(cases)} 組測資（sample + hidden 合計）\n")

    with tempfile.TemporaryDirectory() as tmp:
        data_file = Path(tmp) / ".coverage"
        failed_cases = []

        for case_name, in_file, out_file in cases:
            result = run_one_case(solution_path, in_file, data_file)
            expected = out_file.read_text(encoding="utf-8").strip()
            actual = result.stdout.strip()
            if result.returncode != 0:
                failed_cases.append(
                    (case_name, f"程式異常結束 (exit {result.returncode})：{result.stderr.strip()[-300:]}")
                )
            elif actual != expected:
                failed_cases.append((case_name, f"輸出不符：預期 {expected!r}，實際 {actual!r}"))

        if failed_cases:
            print("⚠ 以下測資沒有通過正確性驗證，覆蓋率數字可能因此失真"
                  "（程式提早出錯、沒機會跑到後面的程式碼）：")
            for name, msg in failed_cases:
                print(f"  - {name}: {msg}")
            print("  建議先用 unittest/pytest 確認 solution.py 全部測資都正確，再回頭看覆蓋率。\n")

        json_path = Path(tmp) / "coverage.json"
        subprocess.run(
            [
                sys.executable, "-m", "coverage", "json",
                f"--rcfile={COVERAGERC}",
                f"--data-file={data_file}",
                "-o", str(json_path),
            ],
            check=True, capture_output=True, text=True,
        )
        report = json.loads(json_path.read_text(encoding="utf-8"))
        file_entry = find_file_entry(report, solution_path)
        summary = file_entry["summary"]

        # 不直接讀 summary["percent_statements_covered"] / ["percent_branches_covered"]：
        # 這兩個欄位是比較新版的 coverage.py 才有（舊版 JSON 報表裡沒有這兩個 key，
        # 只有 percent_covered 這個把 statement 跟 branch 混在一起算的綜合指標）。
        # 改成自己用 covered_lines/num_statements、covered_branches/num_branches
        # 這幾個從舊版就存在的基本欄位計算，不管裝的是哪個版本的 coverage 都能跑。
        num_statements = summary["num_statements"]
        covered_lines = summary["covered_lines"]
        stmt_pct = (covered_lines / num_statements * 100) if num_statements else 100.0

        num_branches = summary["num_branches"]
        covered_branches = summary["covered_branches"]
        branch_pct = (covered_branches / num_branches * 100) if num_branches else 100.0

        print(f"Statement (Instruction) Coverage: {stmt_pct:.1f}%  "
              f"({covered_lines}/{num_statements} 行)")
        print(f"Branch Coverage:                  {branch_pct:.1f}%  "
              f"({covered_branches}/{num_branches} 分支)")

        source_lines = solution_path.read_text(encoding="utf-8").splitlines()

        if file_entry["missing_lines"]:
            print("\n沒有任何一組測資執行到的行：")
            for ln in file_entry["missing_lines"]:
                text = source_lines[ln - 1].strip() if 0 < ln <= len(source_lines) else ""
                print(f"  line {ln}: {text}")

        if file_entry["missing_branches"]:
            print("\n沒有任何一組測資走到的分支（來源行 -> 目的行，-1 代表函式/程式在該處結束）：")
            for src, dst in file_entry["missing_branches"]:
                text = source_lines[src - 1].strip() if 0 < src <= len(source_lines) else ""
                print(f"  {src} -> {dst}   (line {src}: {text})")

        if args.html:
            html_dir = _lib.PROJECT_ROOT / f"htmlcov_{problem_dir.name}"
            subprocess.run(
                [
                    sys.executable, "-m", "coverage", "html",
                    f"--rcfile={COVERAGERC}",
                    f"--data-file={data_file}",
                    "-d", str(html_dir),
                ],
                check=True, capture_output=True, text=True,
            )
            print(f"\nHTML 報表：{html_dir}/index.html")

    print()
    ok = stmt_pct >= args.fail_under_stmt and branch_pct >= args.fail_under_branch
    if not ok:
        print(f"未達門檻（statement >= {args.fail_under_stmt}%, branch >= {args.fail_under_branch}%）")
        sys.exit(1)
    print("達到門檻 ✔")


if __name__ == "__main__":
    main()