import math


def main():
    n1 = int(input())
    n2 = int(input())
    n3 = int(input())

    m1 = 1
    m2 = 1
    m3 = 1

    if n1 < 11:
        pass
    elif n1 < 21:
        m1 = 0.9
    elif n1 < 31:
        m1 = 0.85
    else:
        m1 = 0.8

    if n2 < 11:
        pass
    elif n2 < 21:
        m2 = 0.95
    elif n2 < 31:
        m2 = 0.9
    else:
        m2 = 0.85

    if n3 < 11:
        pass
    elif n3 < 21:
        m3 = 0.85
    elif n3 < 31:
        m3 = 0.75
    else:
        m3 = 0.65

    n1 *= 250 * m1
    n2 *= 880 * m2
    n3 *= 150 * m3

    print(int(math.ceil(n1 + n2 + n3)))


if __name__ == "__main__":
    main()