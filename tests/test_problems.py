"""
通用測試框架
============
這個檔案「不需要為每一題修改」。它會自動掃描 problems/ 底下的每一個子資料夾，
只要該資料夾內有 solution.py 與 testdata/*.in + *.out，就會自動產生對應的
unittest TestCase，並在執行時把 .in 檔內容當作 stdin 餵給 solution.py，
再比對 stdout 是否與 .out 檔一致。

新增題目時，你只需要：
  1. 在 problems/ 底下新增一個資料夾，例如 problems/002_xxx/
  2. 放入 solution.py（你要驗證的參考解或學生解）
  3. 在 problems/002_xxx/testdata/ 放入成對的 xxx.in / xxx.out
不需要動這支測試程式。
"""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import _lib  # noqa: E402

PROBLEMS_DIR = _lib.PROBLEMS_DIR
TIMEOUT_SECONDS = _lib.TIMEOUT_SECONDS  # 單一測資執行逾時秒數，避免無窮迴圈卡住整個測試


def discover_cases(problem_dir: Path):
    """回傳該題目底下 (case 名稱, .in 路徑, .out 路徑) 的排序列表。"""
    return _lib.discover_cases(problem_dir)


def run_solution(solution_path: Path, input_text: str) -> str:
    """以子行程實際執行 solution.py，模擬正式評測環境的行為。"""
    result = subprocess.run(
        [sys.executable, str(solution_path)],
        input=input_text,
        capture_output=True,
        text=True,
        timeout=TIMEOUT_SECONDS,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"solution.py 執行時發生錯誤 (exit code {result.returncode})\n"
            f"--- stderr ---\n{result.stderr}"
        )
    return result.stdout.strip()


def make_test_class(problem_dir: Path):
    solution_path = problem_dir / "solution.py"
    cases = discover_cases(problem_dir)

    class ProblemTestCase(unittest.TestCase):
        pass

    def build_test(in_file: Path, out_file: Path):
        def test(self):
            input_text = in_file.read_text(encoding="utf-8")
            expected = out_file.read_text(encoding="utf-8").strip()
            actual = run_solution(solution_path, input_text)
            self.assertEqual(
                actual,
                expected,
                msg=f"\n測資: {in_file.name}\n輸入:\n{input_text}\n"
                f"預期輸出: {expected!r}\n實際輸出: {actual!r}",
            )
        return test

    for case_name, in_file, out_file in cases:
        test_method = build_test(in_file, out_file)
        test_method.__name__ = f"test_{case_name}"
        setattr(ProblemTestCase, test_method.__name__, test_method)

    ProblemTestCase.__qualname__ = f"Test_{problem_dir.name}"
    ProblemTestCase.__name__ = f"Test_{problem_dir.name}"
    return ProblemTestCase


def _register_all_problem_tests():
    """為 problems/ 底下每一題產生一個 TestCase class，並注入模組全域變數。

    刻意包成函式呼叫，避免迴圈變數（如 problem_dir、cls）外洩成為模組層級的
    全域變數 —— 否則 unittest 的 TestLoader 會把同一個 class 透過不同的
    屬性名稱各收集一次，導致測試被重複執行兩次。
    """
    if not PROBLEMS_DIR.exists():
        return
    for problem_dir in sorted(PROBLEMS_DIR.iterdir()):
        if problem_dir.is_dir() and (problem_dir / "solution.py").exists():
            cls = make_test_class(problem_dir)
            globals()[cls.__name__] = cls


# 讓 `python -m unittest discover` / pytest 都能自動抓到每一題的 TestCase。
_register_all_problem_tests()


if __name__ == "__main__":
    unittest.main(verbosity=2)
