from datetime import datetime
from database import get_connection


def mark_attendance():
    roll_number = input("Enter student roll number: ").strip()
    subject = input("Enter subject: ").strip()
    status = input("Enter status (Present/Absent): ").strip().title()

    if not roll_number or not subject:
        print("\nRoll number and subject are required.")
        return

    if status not in ["Present", "Absent"]:
        print("\nInvalid status. Enter Present or Absent.")
        return

    attendance_date = input(
        "Enter attendance date (DD-MM-YYYY): "
    ).strip()

    try:
        attendance_date = datetime.strptime(
            attendance_date,
            "%d-%m-%Y"
        ).date()
    except ValueError:
        print("\nInvalid date format. Use DD-MM-YYYY.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_id, name
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
    student_name = student[1]

    cursor.execute(
        """
        SELECT attendance_id
        FROM attendance
        WHERE student_id = %s
          AND attendance_date = %s
          AND subject = %s
        """,
        (student_id, attendance_date, subject)
    )

    existing_attendance = cursor.fetchone()

    if existing_attendance is not None:
        print("\nAttendance already recorded for this student.")
        print(
            "Date:",
            attendance_date.strftime("%d-%m-%Y")
        )
        print("Subject:", subject)

        cursor.close()
        connection.close()
        return

    cursor.execute(
        """
        INSERT INTO attendance
        (student_id, attendance_date, subject, status)
        VALUES (%s, %s, %s, %s)
        """,
        (student_id, attendance_date, subject, status)
    )

    connection.commit()

    print("\nAttendance recorded successfully!")
    print("Student :", student_name)
    print("Roll No :", roll_number)
    print("Subject :", subject)
    print(
        "Date    :",
        attendance_date.strftime("%d-%m-%Y")
    )
    print("Status  :", status)

    cursor.close()
    connection.close()


def view_student_attendance():
    roll_number = input("Enter student roll number: ").strip()

    if not roll_number:
        print("\nRoll number cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_id, name, roll_number
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
        SELECT
            attendance_date,
            subject,
            status
        FROM attendance
        WHERE student_id = %s
        ORDER BY attendance_date DESC, subject
        """,
        (student_id,)
    )

    records = cursor.fetchall()

    print("\n================ STUDENT ATTENDANCE ================")
    print("Student Name :", student[1])
    print("Roll Number  :", student[2])
    print("-----------------------------------------------------")

    if not records:
        print("No attendance records found.")
    else:
        print(
            f"{'DATE':<15}"
            f"{'SUBJECT':<25}"
            f"{'STATUS'}"
        )

        print("-" * 55)

        for record in records:
            formatted_date = record[0].strftime("%d-%m-%Y")

            print(
                f"{formatted_date:<15}"
                f"{record[1]:<25}"
                f"{record[2]}"
            )

    print("=====================================================")

    cursor.close()
    connection.close()


def view_attendance_by_date():
    attendance_date = input(
        "Enter date (DD-MM-YYYY): "
    ).strip()

    try:
        attendance_date = datetime.strptime(
            attendance_date,
            "%d-%m-%Y"
        ).date()
    except ValueError:
        print("\nInvalid date format. Use DD-MM-YYYY.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            s.roll_number,
            s.name,
            a.subject,
            a.status
        FROM attendance a
        INNER JOIN students s
            ON a.student_id = s.student_id
        WHERE a.attendance_date = %s
        ORDER BY s.roll_number, a.subject
        """,
        (attendance_date,)
    )

    records = cursor.fetchall()

    print("\n================ ATTENDANCE BY DATE ================")
    print(
        "Date:",
        attendance_date.strftime("%d-%m-%Y")
    )
    print("----------------------------------------------------")

    if not records:
        print("No attendance records found.")
    else:
        print(
            f"{'ROLL NO':<15}"
            f"{'NAME':<25}"
            f"{'SUBJECT':<20}"
            f"{'STATUS'}"
        )

        print("-" * 75)

        for record in records:
            print(
                f"{record[0]:<15}"
                f"{record[1]:<25}"
                f"{record[2]:<20}"
                f"{record[3]}"
            )

    print("====================================================")

    cursor.close()
    connection.close()


def attendance_percentage():
    roll_number = input("Enter student roll number: ").strip()

    if not roll_number:
        print("\nRoll number cannot be empty.")
        return

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_id, name
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
        SELECT
            COUNT(*) AS total_classes,
            SUM(
                CASE
                    WHEN status = 'Present' THEN 1
                    ELSE 0
                END
            ) AS present_classes
        FROM attendance
        WHERE student_id = %s
        """,
        (student_id,)
    )

    result = cursor.fetchone()

    total_classes = result[0]
    present_classes = result[1] or 0

    if total_classes == 0:
        percentage = 0
    else:
        percentage = (present_classes / total_classes) * 100

    print("\n================ ATTENDANCE SUMMARY ================")
    print("Student Name    :", student[1])
    print("Roll Number     :", roll_number)
    print("Total Classes   :", total_classes)
    print("Present Classes :", present_classes)
    print("Absent Classes  :", total_classes - present_classes)
    print("Attendance      :", f"{percentage:.2f}%")
    print("=====================================================")

    cursor.close()
    connection.close()