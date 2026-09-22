def Adopt199(speakInside, speakOutside, home, messageInside, messageOutside):
    total = speakInside * 0.09 \
            + speakOutside * 0.15 \
            + home * 0.14 \
            + messageInside * 1.20 \
            + messageOutside * 1.60

    if total <= 199:
        return 199
    else:
        return int(total)


def Adopt399(speakInside, speakOutside, home, messageInside, messageOutside):
    total = speakInside * 0.075 \
            + speakOutside * 0.135 \
            + home * 0.125 \
            + messageInside * 1.15 \
            + messageOutside * 1.30

    if total <= 399:
        return 399
    else:
        return int(total)


def Adopt799(speakInside, speakOutside, home, messageInside, messageOutside):
    total = speakInside * 0.065 \
            + speakOutside * 0.11 \
            + home * 0.10 \
            + messageInside * 0.95 \
            + messageOutside * 1.10

    if total <= 799:
        return 799
    else:
        return int(total)


def func(speakInside, speakOutside, home, messageInside, messageOutside):

    Total199 = Adopt199(speakInside, speakOutside, home, messageInside, messageOutside)
    Total399 = Adopt399(speakInside, speakOutside, home, messageInside, messageOutside)
    Total799 = Adopt799(speakInside, speakOutside, home, messageInside, messageOutside)

    MinTotal = min(Total199, Total399, Total799)
    print(MinTotal)

    if MinTotal == Total199:
        print("199")
    elif MinTotal == Total399:
        print("399")
    elif MinTotal == Total799:
        print("799")


speakInside = int(input())
speakOutside = int(input())
home = int(input())
messageInside = int(input())
messageOutside = int(input())

func(speakInside, speakOutside, home, messageInside, messageOutside)