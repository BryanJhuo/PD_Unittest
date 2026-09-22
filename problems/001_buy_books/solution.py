'''
商店販售 A、B、C 三本書，各自的定價如下：

- **A 書**：440 元
- **B 書**：1200 元
- **C 書**：130 元

一位顧客欲購買 **A 書 x 本**、**B 書 y 本**與 **C 書 z 本**。

為了吸引顧客，店家推出了以下優惠方案：

1. **九折優惠**：若總購買數量（x + y + z）達到 5 本或以上，原總金額可享有 **9 折優惠**（折扣後價格若有小數點，請**無條件捨去**取至整數）。
2. **滿額折抵**：在計算完上述折扣後，若最終金額**達到 3,000 元或以上**，可再**現折 300 元**。

請撰寫一隻程式，計算並輸出該顧客最終需支付的金額。

【輸入說明】

第一行輸入整數(int) x

第二行輸入整數(int) y

第三行輸入整數(int) z

(x、y、z 範圍皆≥0)

【輸出說明】

輸出購買書本總共所需要的花費
'''

def main():
    numA = int(input())
    numB = int(input())
    numC = int(input())
    numTotal = numA + numB + numC
    totalPrice = numA * 440 + numB * 1200 + numC * 130
    if numTotal >= 5:
        totalPrice = int(totalPrice * 0.9)

    if totalPrice >= 3000:
        totalPrice = totalPrice - 300

    print(totalPrice)

    return

if __name__ == "__main__":
    main()