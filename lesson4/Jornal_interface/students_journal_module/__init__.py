from itertools import count

import PySimpleGUI as sg
import json
from pathlib import Path

files_dir = Path(__name__).absolute().parent / "files1"
storage_file = "students.json"

class StudentsStorage:
    def __init__(self) -> None:
        self.students = self.read_json(storage_file)

    @staticmethod
    def read_json(filename: str) -> dict:
        with open(files_dir / filename) as file:
            return json.load(file)

    @staticmethod
    def write_json(filename: str, data: dict) -> None:
        with open(files_dir / filename, mode="w") as file:
            return json.dump(data, file)

    def flush(self) -> None:
        self.write_json(storage_file, self.students)



def represent_students():
    """Showing Students"""
    result = []

    for id_, student in StudentsStorage().students.items():
        name = student.get('name', 'Unknown Name')
        marks = student.get('marks', 'Unknown Marks')
        result.append(f"ID: {id_}, Name: {name}, Marks: {marks}\n")

    return ''.join(result)


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

def ask_student_payload_add_marks():
    """
    Input template:
        4,5,4,5,4,5

    Expected:

        4,5,4,5,4,5:    list[int]
    """

    prompt = "Enter student's marks for add, using next template:4,5,4,5,4,5\n"

    if not (payload := sg.popup_get_text(prompt)):
        return None
    else:
        marks = [int(i) for i in payload.split(",")]
        return {"marks": marks}

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
    storage = StudentsStorage()
    return storage.students.get(str(id_))


def update_student(id_: int, payload: dict) -> dict or None:
    """Updating Students by ID"""
    storage = StudentsStorage()

    try:
        updated_student = storage.students[str(id_)].copy()
    except KeyError:
        raise ValueError(f"Student with id {id_} does not exist")

    if payload["name"] is not None:
        updated_student["name"] = payload["name"]
    if payload["marks"] is not None:
        updated_student["marks"] = payload["marks"]
    storage.students[str(id_)] = updated_student
    storage.flush()
    return updated_student

def add_student(student: dict) -> dict | None:
    """Adding Students"""
    storage = StudentsStorage()
    if storage.students:
        max_id = max(map(int, storage.students.keys()))
    else:
        max_id = 0

    if len(student) != 2:
        return None
    elif not student.get("name") or not student.get("marks"):
        return None
    else:
        new_id = max_id + 1
        storage.students[str(new_id)] = student

    storage.flush()
    return student

def delete_student(id_: int):
    """Deleting Students by ID"""
    storage = StudentsStorage()

    if search_student(id_):
        del storage.students[str(id_)]
        storage.flush()
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is no student '{id_}' in the storage")

def student_add_marks(id_: int, payload: dict) -> dict:
    """Add marks to student"""
    storage = StudentsStorage()

    try:
        marks_add = storage.students[str(id_)].copy()
    except KeyError:
        raise ValueError(f"Student with id {id_} does not exist")

    else:
        marks_add["marks"].extend(payload["marks"])
        storage.students[str(id_)] = marks_add
        storage.flush()
        return marks_add

def student_details(student: dict) -> None:
    """Showing Students Details"""
    sg.popup(f"Detailed info: [Name: {student['name']}, "
             f"Marks: {student['marks']}, "
             f"Info: {student['info']}]"
             )

def calculate_summary():
    """Calculate total students and average score."""
    storage = StudentsStorage()
    total_students = len(storage.students)
    total_marks = 0
    total_mark_entries = 0
    for student in storage.students.values():
        total_marks += sum(student.get('marks', []))
        total_mark_entries += len(student.get('marks', []))

    average_marks = round(float(total_marks) / total_mark_entries, 2)

    return total_students, average_marks

