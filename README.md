# python-oj-testkit

出題後，用 `unittest` 自動驗證解答程式對所有測資（含公開測資與隱藏測資）是否正確的本地測試環境。

## 專案結構

```
python-oj-testkit/
├── .coveragerc                   # coverage.py 設定，排除 if __name__=="__main__" 樣板行
├── problems/
│   └── 001_buy_books/          # 每一題一個資料夾，資料夾名稱隨意（建議「編號_題名」）
│       ├── problem.md          # 題目敘述（非必要，方便留存對照）
│       ├── solution.py         # 要被驗證的程式：從 stdin 讀輸入、印出結果到 stdout
│       └── testdata/
│           ├── sample_01.in    # 公開測資（題目上會附的範例）
│           ├── sample_01.out
│           ├── hidden_01.in    # 隱藏測資（用來確保解答夠嚴謹，例如邊界值）
│           └── hidden_01.out
├── scripts/
│   ├── new_problem.py           # 一鍵建立新題目的鷹架
│   ├── add_testdata.py          # 幫既有題目追加明測/暗測
│   ├── check_coverage.py        # 檢查某一題全部測資對 solution.py 的覆蓋率
│   └── _lib.py                  # 上面三支腳本（與 tests/test_problems.py）共用的邏輯
└── tests/
    ├── __init__.py
    └── test_problems.py       # 通用測試框架，會自動掃描 problems/ 底下每一題
```

`tests/test_problems.py` **不需要因為新增題目而修改**。新增一題的步驟：

1. 在 `problems/` 底下新增資料夾，例如 `problems/002_xxx/`
2. 放入 `solution.py`
3. 在 `problems/002_xxx/testdata/` 放入成對的 `*.in` / `*.out`（檔名前綴 `sample_` / `hidden_` 只是慣例，方便你自己分辨哪些是題目公開範例、哪些是你額外补充的邊界測資，測試框架本身一視同仁全部執行）

框架會自動幫這個資料夾產生一個 `unittest.TestCase`，每筆 `.in`/`.out` 都是一個獨立的 test case，可以在測試報告中清楚看到「哪一筆測資」失敗、輸入是什麼、預期輸出與實際輸出的差異。

## 快速建立新題目：`scripts/new_problem.py`

手動一個一個資料夾、一個一個檔案建立很麻煩，所以提供了一支腳本，執行後會自動把某一題所需要的檔案都建好（`problem.md`、`solution.py` 都是空白，`testdata/` 底下明測、暗測各建立 3 組空白的 `.in`/`.out`）。

```bash
# 建立第 10 題（資料夾只會用補零後的題號命名：problems/010/）
./scripts/new_problem.py 10

# 建立第 10 題並順便取名（資料夾會是 problems/010_buy_snacks/）
./scripts/new_problem.py 10 buy_snacks

# 自訂明測 / 暗測組數（預設都是 3）
./scripts/new_problem.py 13 --samples 2 --hidden 5
```

（Windows 上若無法直接執行 `./scripts/new_problem.py`，改用 `python scripts/new_problem.py 10` 即可，效果相同。）

腳本的安全機制：

- **不會覆蓋既有的 `problem.md` / `solution.py`**：已經存在的話會顯示「略過（已存在）」，不會清空重寫。
- **測資是「追加」，不是「設定總數」**：`--samples`/`--hidden` 內部呼叫的是跟下一節 `add_testdata.py` 相同的追加邏輯。對全新題目來說，因為 `testdata/` 是空的，「追加 N 組」跟「總共 N 組」結果相同；但如果對**已經有測資**的題目重新執行 `new_problem.py`，`--hidden 5` 代表的是「再追加 5 組」，不是「湊到總共 5 組」（例如已有 3 組時會變成 8 組，不是 5 組）。想幫既有題目補測資，請直接用下一節的 `add_testdata.py`，語意比較不會搞混，也不會不小心因為預設值 `--samples 3 --hidden 3` 而多生出不想要的測資。
- **同一題號不會被不同名稱重複建立**：如果 `problems/011_buy_snacks/` 已經存在，之後執行 `./scripts/new_problem.py 11 something_else` 會直接中止並提示衝突，避免同一題號出現兩個資料夾搞混。

> **提醒**：因為新建立的 `solution.py` 和所有 `.in`/`.out` 都是空白檔案，這時候如果跑 `pytest` / `unittest`，會因為「空輸出」對「空輸出」而顯示測試通過 —— 這只是巧合，不代表題目已經完成。實際填入題目敘述、參考解答、測資內容之後，測試結果才有意義。

## 幫既有題目追加更多測資：`scripts/add_testdata.py`

`new_problem.py` 只負責「從無到有」建立一題的骨架。如果題目已經建立好了，之後想再多加幾組明測/暗測（例如發現一個邊界情況要補測資），用這支腳本，語意是「追加」而不是「總數」——不用回頭去算現在已經有幾組。

```bash
# 用題號找（不論資料夾是 010 還是 010_buy_snacks 都找得到）
./scripts/add_testdata.py 10 --samples 2
./scripts/add_testdata.py 10 --hidden 1

# 也可以直接給資料夾路徑
./scripts/add_testdata.py problems/010_buy_snacks --samples 2 --hidden 1
```

例如題目 010 目前有 `sample_01~03`、`hidden_01~03`，執行 `./scripts/add_testdata.py 10 --samples 2` 之後，會新增 `sample_04`、`sample_05`，01~03 完全不受影響（腳本會自動偵測 `testdata/` 底下該類型目前最大的編號，接著往後新增）。

### 為什麼拆成兩支腳本，而不是一支腳本走到底？

一開始 `new_problem.py` 的 `--samples`/`--hidden` 是「總共要幾組」的語意，這在建立全新題目時沒問題（反正從 0 開始）；但如果拿同一套邏輯去操作「已經有 3 組暗測的題目」，`--hidden 5` 到底是「總共 5 組」還是「再加 5 組」就會混淆，容易誤觸發不小心把已有的測資邏輯搞亂。

所以把「怎麼新增一組空白測資」這件事抽成共用模組 `scripts/_lib.py`（內部函式 `add_cases()`，語意固定是「接續現有編號往後追加 N 組」），`new_problem.py` 跟 `add_testdata.py` 都呼叫同一份實作：

- `new_problem.py`：建立資料夾 + 空白 `problem.md`/`solution.py`，接著呼叫 `_lib.add_cases()` 建立初始的測資組（因為資料夾是全新的，「追加」跟「總數」在這個情境下結果一樣）。
- `add_testdata.py`：只做一件事——對「已經存在」的題目呼叫 `_lib.add_cases()` 追加測資，不會去動 `problem.md`/`solution.py`。

兩支腳本因為共用同一份 `add_cases()` 實作（直接 `import _lib` 共用函式，而不是互相呼叫對方、或用 subprocess 串接彼此），所以行為保證一致、之後只要改一個地方，兩邊都會同步更新，不用擔心兩份邏輯寫歪成不同行為。`_lib.py` 本身不能直接執行，純粹是共用邏輯的地方。

> **Python 版本相容性**：`scripts/_lib.py` 開頭有 `from __future__ import annotations`，讓型別註記（例如 `Path | None`）延遲求值，這三支腳本在 Python 3.8 以上都能正常執行，不需要 3.10 才有的新語法。

## 檢查測資的覆蓋率：`scripts/check_coverage.py`

出題時想確保「明測 + 暗測」合起來能把 `solution.py` 的每一行、每一個分支都測到，用這支腳本。

```bash
./scripts/check_coverage.py 1
./scripts/check_coverage.py 001_buy_books
./scripts/check_coverage.py problems/001_buy_books

# 自訂及格門檻（百分比），預設兩者都要 100
./scripts/check_coverage.py 1 --fail-under-stmt 90 --fail-under-branch 80

# 額外產生 HTML 報表，瀏覽器打開可以逐行看哪裡沒被測到
./scripts/check_coverage.py 1 --html
```

輸出長這樣（故意示範測資不夠的情況）：

```
對象：problems/001_buy_books/solution.py
共 1 組測資（sample + hidden 合計）

Statement (Instruction) Coverage: 80.0%  (8/10 行)
Branch Coverage:                  50.0%  (2/4 分支)

沒有任何一組測資執行到的行：
  line 12: total = (total * 9) // 10
  line 16: total -= 300

沒有任何一組測資走到的分支（來源行 -> 目的行，-1 代表函式/程式在該處結束）：
  11 -> 12   (line 11: if x + y + z >= 5:)
  15 -> 18   (line 15: if total >= 3000:)

未達門檻（statement >= 100.0%, branch >= 100.0%）
```

直接告訴你哪幾行、哪幾個分支沒有任何測資走到，對照原始碼就知道該補什麼樣的測資（上面這個例子就是缺少「會觸發九折」跟「會觸發滿額折抵」的測資）。門檻沒達到時腳本會回傳非 0 的 exit code，之後要接 CI 也方便。

### 為什麼不是直接用 pytest-cov？

一開始想直接用 `pytest --cov=solution.py` 測，但實測會出現：

```
CoverageWarning: Module problems/001_buy_books/solution.py was never imported.
CoverageWarning: No data was collected.
```

原因是本專案的測試框架（`tests/test_problems.py`）**刻意**用 `subprocess` 開一個全新的 Python 行程去執行 `solution.py`（這樣才能不管解答內部是用 `input()` 還是 `sys.stdin.read()` 都測得到，見前面「測試框架的運作原理」那節）。`pytest-cov` 預設只追蹤「自己這個 process 內」執行到的程式碼，子行程裡發生的事，母行程裡的 `pytest --cov` 是看不到的——除非另外設定 coverage.py 的「子行程覆蓋率量測」機制（環境變數 `COVERAGE_PROCESS_START` + 在 site-packages 裡放一個會呼叫 `coverage.process_startup()` 的 `sitecustomize.py`），但那樣要動到 Python 環境的全域設定，較不直觀也較難維護。

`pytest-cov` 其實只是包了一層 `coverage.py`，所以這支腳本乾脆跳過 pytest 這層，直接呼叫 `coverage.py` 本人：把「執行 `solution.py`」這個動作換成 `python -m coverage run --branch --append solution.py`，每一筆測資都這樣跑一次，覆蓋率資料會一直累加進同一份暫存的 `.coverage` 資料檔，跑完全部測資後再統一用 `coverage json` 產生報表、解析出 Statement 跟 Branch 各自的百分比。這樣拿到的數字跟你原本想用 `pytest-cov` 拿到的是同一種東西（背後同一顆引擎），只是換一種驅動方式來配合本專案 subprocess 的架構，所以用不到 `pytest-cov` 這個套件本身，只需要 `coverage` 就夠了（已經加進 `requirements-dev.txt`）。

### 名詞對照：「Instruction Coverage」在 Python 對應到什麼？

`Instruction Coverage`（指令覆蓋率）是 Java 系工具（如 JaCoCo）常用的說法，量的是 bytecode 指令層級。Python 的 `coverage.py` 沒有這麼細的粒度，量的是 **Statement Coverage（陳述式/程式碼行覆蓋率）**——也就是「這一行程式碼有沒有被執行過」，實務上拿來當「Instruction Coverage」的替代指標是業界常見做法（畢竟目的一樣：確保每一行邏輯都至少被測過一次）。腳本輸出時同時標成 `Statement (Instruction) Coverage`，就是這個原因；`Branch Coverage`（分支覆蓋率）則是 `coverage.py` 原生支援的功能，量的是每個 `if`/`for` 等分支的「兩條路徑」是不是都至少走過一次，這跟你原本問的「Branch Coverage」定義是一致的，沒有轉換問題。

### 有個容易誤解的地方：`if __name__ == "__main__":` 這行

因為每支 `solution.py` 都用 `python3 solution.py` 直接執行、從來不會被別的模組 `import`，所以 `if __name__ == "__main__":` 這一行的「被 import、不執行 `main()`」那個分支，不管測資設計得再完整都不可能被走到——這不是測資的問題，是這行本來就量不到。已經在專案根目錄的 `.coveragerc` 裡把這行排除掉了（`exclude_lines`），所以不會讓每一題都卡在 99% 上不去。如果你的 `solution.py` 用了別的寫法（例如沒有 `if __name__ == "__main__":` 這個保護），不受影響。

## 環境建置

你的 Python 已安裝完成，這裡只需要建立一個獨立的虛擬環境即可（本專案本身完全只用標準函式庫 `subprocess` / `unittest` / `pathlib`，不需要額外套件；虛擬環境純粹是為了不要汙染系統環境、且未來若你想加 `pytest`、程式碼檢查工具等也有乾淨的地方裝）。

### 方案 A：原生 venv

```bash
cd python-oj-testkit
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# 目前不需要裝任何套件；若之後想用 pytest 執行同一批 unittest 測試：
pip install -r requirements-dev.txt
```

### 方案 B：uv（推薦，速度快、鎖版本方便）

```bash
cd python-oj-testkit
uv venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 同樣是選用；只有想用 pytest 才需要
uv pip install -r requirements-dev.txt
```

兩者選一即可，對本專案的執行方式沒有差異，`uv` 主要優勢在安裝套件速度與可重現性（之後若要在 CI 上重建環境會更省時間）。

## 執行測試

```bash
# 方式一：純標準函式庫，最貼近題目要求的「unittest 方式」
python3 -m unittest discover -s tests -t . -v

# 方式二：只跑某一題
python3 -m unittest tests.test_problems.Test_001_buy_books -v

# 方式三（選用）：改用 pytest 執行（一樣是底下的 unittest TestCase，只是換一個 runner，
# 錯誤訊息排版更好看、可以平行執行）
pytest tests/ -v
```

### 只用 pytest 測試單一題目

每一題會被收集成一個 class，名稱是 `Test_<資料夾名稱>`（例如 `problems/001_buy_books/` → `Test_001_buy_books`）。

```bash
# 用 node id 指定整個 class：只跑這一題的所有測資
pytest tests/test_problems.py::Test_001_buy_books -v

# node id 再加上 :: 方法名，可以只跑「這一題的其中一筆測資」
pytest tests/test_problems.py::Test_001_buy_books::test_sample_01 -v

# 用 -k 關鍵字篩選（不用記完整 node id，模糊比對 class 名稱/方法名稱即可）
pytest tests/ -k "001_buy_books" -v

# -k 也可以組合條件，例如只跑這一題裡的 hidden 測資
pytest tests/ -k "001_buy_books and hidden" -v
```

用 `pytest --collect-only tests/` 可以先看一下目前 `problems/` 底下所有題目、測資會被收集成什麼名字，再決定要用哪種方式篩選。

看到 `OK` 代表 `solution.py` 通過該題目底下所有 `.in`/`.out` 測資；`FAILED` 時，錯誤訊息會列出是哪一筆測資（例如 `sample_03`）、當時的輸入、預期輸出與實際輸出，方便直接定位問題。

## 測試框架的運作原理

`run_solution()` 是用 `subprocess.run()` 實際「開一個新的 Python 行程」執行 `solution.py`，把 `.in` 檔內容當作標準輸入餵進去，並擷取標準輸出跟 `.out` 檔比對（去除頭尾空白後逐字比對）。

這樣設計的理由：

- **貼近真實評測情境**：無論 `solution.py` 內部是用 `input()`、`sys.stdin.readline()` 還是 `sys.stdin.read()`，只要程式最終照題目規定讀 stdin、印 stdout，測試都能正確驗證，不需要知道解答程式內部怎麼寫。
- **行程隔離**：每筆測資都是全新的 Python 行程，不會有前一筆測資殘留的變數/狀態互相汙染。
- **可偵測逾時與例外**：設定了 5 秒逾時（`TIMEOUT_SECONDS`），若解答程式無窮迴圈或當機（非 0 的 exit code），會直接判定該筆測資失敗並顯示錯誤內容（`stderr`），而不是讓整個測試卡死。

另一種常見做法是「直接 import 解答模組、monkeypatch `sys.stdin`」，優點是速度快（省去行程啟動開銷），缺點是要求解答程式碼被 import 時不能有副作用、且模組層級的變數會在多次測試間殘留，需要額外處理。以你目前題目的規模（單題幾筆測資），subprocess 方式的效能完全夠用，穩定性也更好，因此框架採用這個方式。

## 之後可以視需求擴充的方向

- **CI 自動化**：把 `python3 -m unittest discover -s tests -t .` 接到 GitHub Actions / GitLab CI，每次出新題、修改測資都自動跑一次。
- **多份解答比對**：如果同一題想同時驗證「參考解」與「學生繳交的程式」，可以讓 `run_solution()` 多接受一個 `solution_path` 參數（目前已經是這樣設計），在測試裡多加一個維度即可，不需要動測資本身。
- **效能/複雜度測資**：若題目要考慮大量資料下的效能，可以額外加一批 `perf_*.in`（不附 `.out`，改成量測執行時間），另外寫一支效能測試，跟正確性測試分開執行，避免拖慢日常開發的測試速度。
```

把這份內容整份覆蓋掉你原本的 `README.md` 即可。