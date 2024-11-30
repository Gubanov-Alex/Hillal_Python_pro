import PySimpleGUI as sg

students = {
    1: {
        "name": "John Doe",
        "marks": [4, 3, 5, 2, 4, 1, 5],
        "info": "John is 21 y.o. Hobbies: music",
    },
    2:{
        "name": "Jane Smith",
        "marks": [2, 3, 5, 4, 3, 5, 2],
        "info": "Jane is 23 y.o. Hobbies: sports",
    },
    3:{
        "name": "Alice Johnson",
        "marks": [5, 4, 3, 2, 5, 4, 5],
        "info": "Alice is 20 y.o. Hobbies: reading",
    },
    4:{
        "name": "Robert Brown",
        "marks": [3, 3, 4, 2, 5, 4, 3],
        "info": "Robert is 22 y.o. Hobbies: traveling",
    },
    5:{
        "name": "Emily Davis",
        "marks": [5, 1, 5, 4, 3, 2, 4],
        "info": "Emily is 19 y.o. Hobbies: gaming",
    },
}
LAST_ID_CONTEXT = 5



def represent_students():
    """Showing Students"""
    result = []
    for id_, student in students.items():
            result.append(f"[{id_}] {student['name']}, marks: {student['marks']}")
    return "\n".join(result)

def ask_student_payload_add():
    """
        Input template:
        "John Doe;4,5,4,5,4,5" for full change
        "John Doe" for name only change
        "4,5,4,5,4,5" for marks only change

        Expected:
        John Doe:       str
        4,5,4,5,4,5:    list[int]
    """

    if not (payload := parse(sg.popup_get_text(
            "Enter student's payload using next template:"
              "\nJohn Doe;4,5,4,5,4,5\n", title="Student data add"))):
        sg.popup("No info added, please try again")
        return None
    else:
        name, marks = payload

    return {"name": name, "marks": marks}

def ask_student_payload_update():
    """
        Input template:
        "John Doe;4,5,4,5,4,5" for full change
        "John Doe" for name only change
        "4,5,4,5,4,5" for marks only change

        Expected:
        John Doe:       str
        4,5,4,5,4,5:    list[int]
    """


    if not (payload := parse(sg.popup_get_text(
            "Enter student's payload using next template:"
              "\n'John Doe;4,5,4,5,4,5' full change"
               "\n'John Doe' Name only change"
               " \n'4,5,4,5,4,5' Marks only change\n", title='Student data change'))):
        sg.popup("No info added, please try again")
        return None
    else:
        name, marks = payload

    return {"name": name, "marks": marks}

def parse(data: str) -> tuple[str or None, list[int] or None]:
    """Return student name and marks.

    user input template:
    "John Doe;4,5,4,5,4,5" for full change
    "John Doe" for name only change
    "4,5,4,5,4,5" for marks only change


    def foo(*args, **kwargs):
        pass

    """

    template = ("John Doe;4,5,4,5,4,5" "full change\n"
                "John Doe" "name only change\n"
                "4,5,4,5,4,5" "marks only change\n"
                )

    items = data.split(";")
    # items == ["John Doe", "4,5...."]

    if len(items) == 1:
        name = items[0]
        if name.replace(" ", "").isalpha():
            return name , None
        else:
            try:
                marks = [int(i) for i in name.split(",")]
                return None, marks
            except ValueError:
                sg.popup("Invalid value for marks", title="Input Error")

    elif len(items) == 2:
        name, raw_marks = items
        try:
            marks = [int(item) for item in raw_marks.split(",")]
        except ValueError as error:
            print(error)
            sg.popup("Invalid value for marks", title="Input Error")

        return name, marks

    else:
        sg.popup("No info added, please try again", title="Input Error")

def search_student(id_: int) -> dict | None:
    """Searching Students by ID"""
    return students.get(id_)

def update_student(id_: int, payload: dict) -> dict or None:
    """Updating Students by ID"""
    global students

    updated_student = students[id_].copy()

    if payload["name"] is not None:
        updated_student["name"] = payload["name"]
    if payload["marks"] is not None:
        updated_student["marks"] = payload["marks"]
    students[id_] = updated_student
    return updated_student

def add_student(student: dict) -> dict | None:
    """Adding Students"""
    global LAST_ID_CONTEXT

    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        LAST_ID_CONTEXT += 1
        students[LAST_ID_CONTEXT] = student

    return student

def delete_student(id_: int):
    """Deleting Students by ID"""
    if search_student(id_):
        del students[id_]
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is no student '{id_}' in the storage")

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