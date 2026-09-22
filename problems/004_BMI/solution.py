def getBMI(height, weight):
    return weight / (height * height)


def main():
    height_cm = float(input())
    weight_lb = int(input())
    
    height_m = height_cm / 100
    weight_kg = weight_lb * 0.454
    
    bmi = getBMI(height_m, weight_kg)
    
    if bmi < 18:
        print("Underweight")
    elif bmi < 24:
        print("Normal")
    elif bmi < 27:
        print("Overweight")
    elif bmi < 30:
        print("Mild obesity")
    elif bmi < 35:
        print("Moderate obesity")
    else:
        print("Severe obesity")
        

if __name__ == "__main__":
    main()