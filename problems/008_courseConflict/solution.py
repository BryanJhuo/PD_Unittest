def handle_input():
    course_number = int(input())
    t1 = int(input())
    t2 = int(input())

    if t1 > t2:
        small_time = t2
        big_time = t1
    else:
        small_time = t1
        big_time = t2

    course = [course_number, small_time, big_time]
    return course


def check_conflict(course_a, course_b):
    num_a = course_a[0]
    a_first = course_a[1]
    a_second = course_a[2]
    num_b = course_b[0]
    b_first = course_b[1]
    b_second = course_b[2]

    match_first = (a_first == b_first) or (a_first == b_second)
    match_second = (a_second == b_first) or (a_second == b_second)

    conflict_count = 0
    if match_first and match_second:
        print(f"{num_a} and {num_b} conflict on {a_first}")
        print(f"{num_a} and {num_b} conflict on {a_second}")
        conflict_count = 2
    elif match_first:
        print(f"{num_a} and {num_b} conflict on {a_first}")
        conflict_count = 1
    elif match_second:
        print(f"{num_a} and {num_b} conflict on {a_second}")
        conflict_count = 1

    return conflict_count


def main():
    course1 = handle_input()
    course2 = handle_input()
    course3 = handle_input()

    courses = [course1, course2, course3]
    sorted_courses = sorted(courses)  

    course_a = sorted_courses[0]
    course_b = sorted_courses[1]
    course_c = sorted_courses[2]

    total_conflict = 0
    total_conflict += check_conflict(course_a, course_b)
    total_conflict += check_conflict(course_a, course_c)
    total_conflict += check_conflict(course_b, course_c)

    if total_conflict == 0:
        print("correct")


if __name__ == "__main__":
    main()