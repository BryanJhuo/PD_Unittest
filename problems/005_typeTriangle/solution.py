a = int(input())
b = int(input())
c = int(input())

if a < 0 or b < 0 or c < 0:
    print("Not Triangle")   
elif a + b <= c or a + c <= b or b + c <= a:
    print("Not Triangle")
else:
    # 正三角形判斷
    if a == b and b == c:
        print("Equilateral Triangle")

    # 等腰三角形判斷（只要任意兩邊相等即可）
    if a == b or b == c or a == c:
        print("Isosceles Triangle")

    # 角度判斷（透過手動找最大邊來對應計算）
    if a >= b and a >= c:
        max_sq = a * a
        sum_sq = b * b + c * c
    elif b >= a and b >= c:
        max_sq = b * b
        sum_sq = a * a + c * c
    else:
        max_sq = c * c
        sum_sq = a * a + b * b

    if max_sq > sum_sq:
        print("Obtuse Triangle")
    elif max_sq < sum_sq:
        print("Acute Triangle")
    else:
        print("Right Triangle")

    # 輸出周長
    print(a + b + c)