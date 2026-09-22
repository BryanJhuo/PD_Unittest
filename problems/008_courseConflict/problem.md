
def handle_input():
    course_number = int(input())
    course_time = []
    temp1 = int(input())
    temp2 = int(input())
    if ( temp1 > temp2 ) :
        course_time.append(temp2)
        course_time.append(temp1)
    else :
        course_time.append(temp1)
        course_time.append(temp2)
    return course_number, course_time


#兩堂課的衝堂判斷
def Check_conflict(course_time1, course_time2) :
    isconflict = False
    if (course_time1[1][0] == course_time2[1][0]) :
        print(f"{course_time1[0]} and {course_time2[0]} conflict on {course_time2[1][0]}")
        isconflict = True
    if (course_time1[1][0] == course_time2[1][1]) :
        print(f"{course_time1[0]} and {course_time2[0]} conflict on {course_time2[1][1]}")
        isconflict = True

    if (course_time1[1][1] == course_time2[1][0]) :
        print(f"{course_time1[0]} and {course_time2[0]} conflict on {course_time2[1][0]}")
        isconflict = True
    if (course_time1[1][1] == course_time2[1][1]) :
        print(f"{course_time1[0]} and {course_time2[0]} conflict on {course_time2[1][1]}")
        isconflict = True
    return isconflict


def main() :
    Couser_list = []
    course_number, course_time = handle_input()
    Couser_list.append([course_number, course_time])
    course_number, course_time = handle_input()
    Couser_list.append([course_number, course_time])
    course_number, course_time = handle_input()
    Couser_list.append([course_number, course_time])
    Couser_list = sorted(Couser_list, key = lambda x: x[0])

    isconflict1 = Check_conflict(Couser_list[0], Couser_list[1])
    isconflict2 = Check_conflict(Couser_list[0], Couser_list[2])
    isconflict3 = Check_conflict(Couser_list[1], Couser_list[2])
    if not isconflict1 and not isconflict2 and not isconflict3 :
        print("correct")




    
    
    

    

main()