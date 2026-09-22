'''
已知某位學生修習「國文」、「計算機概論」與「計算機程式設計」三門科目。請撰寫一隻程式，讀取學生的姓名、學號及三科成績，計算其**總成績**與**平均成績**，並依指定格式輸出結果。

【輸入說明】

- 輸入共有五行：
- 第一行：學生姓名（字串 string）
- 第二行：學生學號（整數 int）
- 第三行：國文成績（整數 int）
- 第四行：計算機概論成績（整數 int）
- 第五行：計算機程式設計成績（整數 int）
- 數據範圍：成績皆為整數且 0 ≤ 成績 ≤ 100

【輸出說明】

輸出共有四行，請使用格式化輸出（如 Python 的 format / f-string 或 C/C++ 的標準輸出）：
第一行輸出 Name (學生名字)
第二行輸出 Id (學生學號)
第三行輸出 Total (學生三科成績之總分)
第四行輸出 Average (學生三科成績之平均) (取至整數，無條件捨去小數點)
'''

def main():
    studentName = input()
    studentId = int(input())
    chineseScore = int(input())
    computerIntroScore = int(input())
    computerProgrammingScore = int(input())

    totalScore = chineseScore + computerIntroScore + computerProgrammingScore
    averageScore = totalScore // 3  # Use integer division to discard decimal part

    print("Name:{0}".format(studentName))
    print("Id:{0}".format(studentId))
    print("Total:{0}".format(totalScore))
    print("Average:{0}".format(averageScore))

    return

if __name__ == "__main__":
    main()