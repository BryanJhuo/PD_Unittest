"""
共用邏輯，給 new_problem.py、add_testdata.py、check_coverage.py，
以及 tests/test_problems.py 一起 import 使用。
這支檔案本身不是拿來直接執行的腳本。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
PROBLEMS_DIR = PROJECT_ROOT / "problems"

TIMEOUT_SECONDS = 5  # 單一測資執行逾時秒數，避免無窮迴圈卡住整個測試/覆蓋率量測

_CASE_RE_TEMPLATE = r"^{prefix}_(\d+)\.in$"


def touch(path: Path) -> bool:
    """建立空白檔案；若已存在則略過，絕不覆蓋既有內容。回傳是否為新建立。"""
    if path.exists():
        print(f"  略過（已存在） {path.relative_to(PROJECT_ROOT)}")
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()
    print(f"  建立         {path.relative_to(PROJECT_ROOT)}")
    return True


def find_problem_dir(number: int) -> Path | None:
    """依題號找出對應的題目資料夾（不論有沒有加後綴名稱）。找不到回傳 None。"""
    padded = f"{number:03d}"
    if not PROBLEMS_DIR.exists():
        return None
    for d in PROBLEMS_DIR.iterdir():
        if d.is_dir() and (d.name == padded or d.name.startswith(f"{padded}_")):
            return d
    return None


def resolve_problem_dir(target: str) -> Path:
    """把使用者輸入的題號（"10"）、資料夾名稱（"010_buy_snacks"）或路徑
    （"problems/010_buy_snacks"）統一解析成題目資料夾的絕對路徑。

    找不到的話會直接印出錯誤訊息並結束程式（呼叫 die()），
    讓每支腳本都不用各自重複寫這段解析與報錯邏輯。
    """
    try:
        number = int(target)
    except ValueError:
        path = Path(target)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        if not path.exists():
            die(f"找不到題目資料夾：{path}")
        return path

    problem_dir = find_problem_dir(number)
    if problem_dir is None:
        die(
            f"找不到題號 {number:03d} 對應的資料夾，"
            f"請確認 problems/ 底下是否有 {number:03d} 或 {number:03d}_xxx，"
            f"或先用 new_problem.py 建立這一題。"
        )
    return problem_dir


def discover_cases(problem_dir: Path) -> list[tuple[str, Path, Path]]:
    """回傳該題目底下 (case 名稱, .in 路徑, .out 路徑) 的排序列表。

    給 tests/test_problems.py（跑正確性測試）與 check_coverage.py
    （量覆蓋率）共用，確保兩邊看到的測資集合永遠一致。
    """
    testdata_dir = problem_dir / "testdata"
    cases = []
    if not testdata_dir.exists():
        return cases
    for in_file in sorted(testdata_dir.glob("*.in")):
        out_file = in_file.with_suffix(".out")
        if out_file.exists():
            cases.append((in_file.stem, in_file, out_file))
    return cases


def next_index(testdata_dir: Path, prefix: str) -> int:
    """回傳該 prefix（sample / hidden）目前最大編號的下一號，資料夾不存在或還沒有任何檔案就回傳 1。"""
    if not testdata_dir.exists():
        return 1
    pattern = re.compile(_CASE_RE_TEMPLATE.format(prefix=prefix))
    max_idx = 0
    for f in testdata_dir.iterdir():
        m = pattern.match(f.name)
        if m:
            max_idx = max(max_idx, int(m.group(1)))
    return max_idx + 1


def add_cases(problem_dir: Path, prefix: str, count: int) -> list[Path]:
    """在 problem_dir/testdata 底下，接續現有編號之後，新增 count 組空白的 <prefix>_NN.in/.out。

    這是「追加」語意：已經有 sample_01~03 時呼叫 add_cases(..., "sample", 2)
    會建立 sample_04、sample_05，不會動到 01~03，也不會要求你先知道目前有幾組。
    """
    testdata_dir = problem_dir / "testdata"
    start = next_index(testdata_dir, prefix)
    created = []
    for i in range(start, start + count):
        idx = f"{i:02d}"
        for ext in (".in", ".out"):
            p = testdata_dir / f"{prefix}_{idx}{ext}"
            if touch(p):
                created.append(p)
    return created


def die(message: str) -> None:
    sys.exit(message)