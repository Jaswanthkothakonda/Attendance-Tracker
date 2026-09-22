from database import get_connection


def add_student():
    roll_number = input("Enter roll number: ").strip()
    name = input("Enter student name: ").strip()
    department = input("Enter department: ").strip()
    email = input("Enter email: ").strip()

    if not roll_number or not name:
        print("\nRoll number and name are required.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_id
        FROM students
        WHERE roll_number = %s
        """,
        (roll_number,)
    )

    existing_student = cursor.fetchone()

    if existing_student is not None:
        print("\nA student with this roll number already exists.")
        cursor.close()
        connection.close()
        return

    cursor.execute(
        """
        INSERT INTO students
        (roll_number, name, department, email)
        VALUES (%s, %s, %s, %s)
        """,
        (roll_number, name, department, email)
    )

    connection.commit()

    print("\nStudent added successfully!")
    print("Student ID:", cursor.lastrowid)

    cursor.close()
    connection.close()


def view_students():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            student_id,
            roll_number,
            name,
            department,
            email
        FROM students
        ORDER BY student_id
        """
    )

    students = cursor.fetchall()

    print("\n==================== STUDENT LIST ====================")

    if not students:
        print("No students found.")
    else:
        print(
            f"{'ID':<5}"
            f"{'ROLL NO':<15}"
            f"{'NAME':<25}"
            f"{'DEPARTMENT':<20}"
            f"{'EMAIL'}"
        )

        print("-" * 85)

        for student in students:
            print(
                f"{student[0]:<5}"
                f"{student[1]:<15}"
                f"{student[2]:<25}"
                f"{student[3] or '':<20}"
                f"{student[4] or ''}"
            )

    print("=" * 85)

    cursor.close()
    connection.close()


def search_student():
    search_value = input(
        "Enter roll number or student name: "
    ).strip()

    if not search_value:
        print("\nSearch value cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            student_id,
            roll_number,
            name,
            department,
            email
        FROM students
        WHERE roll_number = %s
           OR name LIKE %s
        ORDER BY name
        """,
        (search_value, f"%{search_value}%")
    )

    students = cursor.fetchall()

    print("\n==================== SEARCH RESULTS ====================")

    if not students:
        print("No matching students found.")
    else:
        for student in students:
            print("\nStudent ID :", student[0])
            print("Roll Number:", student[1])
            print("Name       :", student[2])
            print("Department :", student[3] or "")
            print("Email      :", student[4] or "")
            print("-" * 50)

    print("=========================================================")

    cursor.close()
    connection.close()


def delete_student():
    roll_number = input(
        "Enter student's roll number to delete: "
    ).strip()

    if not roll_number:
        print("\nRoll number cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_id, roll_number, name
        FROM students
        WHERE roll_number = %s
        """,
        (roll_number,)
    )

    student = cursor.fetchone()

    if student is None:
        print("\nStudent not found.")
        cursor.close()
        connection.close()
        return

    student_id = student[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM attendance
        WHERE student_id = %s
        """,
        (student_id,)
    )

    attendance_count = cursor.fetchone()[0]

    if attendance_count > 0:
        print("\nCannot delete this student.")
        print("Attendance records exist for this student.")
        print("Delete the attendance records first if required.")

        cursor.close()
        connection.close()
        return

    confirm = input(
        f"Delete {student[2]} ({student[1]})? (yes/no): "
    ).strip().lower()

    if confirm != "yes":
        print("\nDeletion cancelled.")
        cursor.close()
        connection.close()
        return

    cursor.execute(
        """
        DELETE FROM students
        WHERE roll_number = %s
        """,
        (roll_number,)
    )

    connection.commit()

    print("\nStudent deleted successfully.")

    cursor.close()
    connection.close()