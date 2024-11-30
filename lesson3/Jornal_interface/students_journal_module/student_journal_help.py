def student_details(student: dict) -> None:
    """Showing Students Details"""
    sg.popup(f"Detailed info: [Name: {student['name']}, "
             f"Marks: {student['marks']}, "
             f"Info: {student['info']}]"
             )

def calculate_summary():
    """Calculate total students and average score."""
    total_students = len(students)
    total_marks = sum(sum(student["marks"]) for student in students.values())
    total_entries = sum(len(student["marks"]) for student in students.values())
    average_score = total_marks / total_entries if total_entries else 0
    return total_students, round(average_score, 2)