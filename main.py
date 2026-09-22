from students import (
    add_student,
    view_students,
    search_student,
    delete_student
)

from attendance import (
    mark_attendance,
    view_student_attendance,
    view_attendance_by_date,
    attendance_percentage
)


def display_menu():
    print("\n")
    print("=" * 50)
    print("          ATTENDANCE TRACKER")
    print("=" * 50)

    print("\nSTUDENT MANAGEMENT")
    print("1. Add Student")
    print("2. View Students")
    print("3. Search Student")
    print("4. Delete Student")

    print("\nATTENDANCE MANAGEMENT")
    print("5. Mark Attendance")
    print("6. View Student Attendance")
    print("7. View Attendance By Date")
    print("8. Attendance Percentage")

    print("\n9. Exit")
    print("=" * 50)


def main():
    while True:
        display_menu()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            view_students()

        elif choice == "3":
            search_student()

        elif choice == "4":
            delete_student()

        elif choice == "5":
            mark_attendance()

        elif choice == "6":
            view_student_attendance()

        elif choice == "7":
            view_attendance_by_date()

        elif choice == "8":
            attendance_percentage()

        elif choice == "9":
            print("\nThank you for using the Attendance Tracker!")
            print("Goodbye!")
            break

        else:
            print("\nInvalid choice.")
            print("Please select a number from 1 to 9.")


if __name__ == "__main__":
    main()