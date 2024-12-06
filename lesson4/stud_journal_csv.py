import csv
from pathlib import Path



"""
Student:
    name: str
    marks: list[int]

Features:
- fetch all students from the database
- add another yet student to the database
- retrieve the student by NAME. UI/UX issues...
"""
from curses.ascii import isalpha

# ==================================================
# Simulated storage
# ==================================================
files_dir = Path(__name__).absolute().parent / "files1"
storage_file = "students.csv"


class StudentsStorage:
    def __init__(self) -> None:
        self.students = self.read_csv(storage_file)

    @staticmethod
    def read_csv(filename: str) -> dict:
        students = {}
        with open(files_dir / filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                id_ = row['id']
                students[id_] = {
                    "name": row['name'],
                    "marks": [int(mark) for mark in row['marks'].split(",")] if row['marks'] else []
                }
        return students

    @staticmethod
    def write_csv(filename: str, data: dict) -> None:
        with open(files_dir / filename, mode="w", newline='') as csvfile:
            fieldnames = ['id', 'name', 'marks']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for id_, student in data.items():
                writer.writerow({
                    'id': id_,
                    'name': student['name'],
                    'marks': ','.join(map(str, student['marks']))
                })

    def flush(self) -> None:
        self.write_csv(storage_file, self.students)


def represent_students():
    for id_, student in StudentsStorage().students.items():
        print(f"[{id_}] {student['name']}, marks: {student['marks']}")


# ==================================================
# CRUD (Create Read Update Delete)
# ==================================================
def student_create(student: dict) -> dict | None:
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


def search_student(id_: int) -> dict | None:
    """Searching Students by ID"""
    storage = StudentsStorage()
    return storage.students.get(str(id_))


def delete_student(id_: int):
    """Deleting Students by ID"""
    storage = StudentsStorage()

    if search_student(id_):
        del storage.students[str(id_)]
        storage.flush()
        print(f"Student with id '{id_}' is deleted")
    else:
        print(f"There is no student '{id_}' in the storage")


def update_student(id_: int, payload: dict) -> dict:
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
    print(f"Detailed info: [{student['name']}]...")


# ==================================================
# Handle user input
# ==================================================
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
                raise Exception(f"Marks are incorrect. Template: {template}")

    elif len(items) == 2:
        name, raw_marks = items
        try:
            marks = [int(item) for item in raw_marks.split(",")]
        except ValueError as error:
            print(error)
            raise Exception(f"Marks are incorrect. Template: {template}") from error

        return name, marks

    else:
        raise Exception(f"Incorrect data. Template: {template}")




def ask_student_payload_create():
    """
    Input template:
        'John Doe;4,5,4,5,4,5'

    Expected:
        John Doe:       str
        4,5,4,5,4,5:    list[int]
    """

    prompt = "Enter student's payload using next template:John Doe;4,5,4,5,4,5\n"

    if not (payload := parse(input(prompt))):
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

    prompt = ("Enter student's payload using next template:"
              "\n'John Doe;4,5,4,5,4,5' full change"
               "\n'John Doe' Name only change"
               " \n'4,5,4,5,4,5' Marks only change\n")

    if not (payload := parse(input(prompt))):
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

    if not (payload := input(prompt)):
        return None
    else:
        marks = [int(i) for i in payload.split(",")]
        return {"marks": marks}



def handle_management_command(command: str):
    if command == "show":
        represent_students()

    elif command == "retrieve":
        search_id = input("Enter student's id to retrieve: ")

        try:
            id_ = int(search_id)
        except ValueError as error:
            raise Exception(f"ID '{search_id}' is not correct value") from error
        else:
            if student := search_student(id_):
                student_details(student)
            else:
                print(f"There is not student with id: '{id_}'")

    elif command == "remove":
        delete_id = input("Enter student's id to remove: ")

        try:
            id_ = int(delete_id)
        except ValueError as error:
            raise Exception(f"ID '{delete_id}' is not correct value") from error
        else:
            delete_student(id_)

    elif command == "change":
        update_id = input("Enter student's id you wanna change: ")

        try:
            id_ = int(update_id)
        except ValueError as error:
            raise Exception(f"ID '{update_id}' is not correct value") from error
        else:
            if data := ask_student_payload_update():
                update_student(id_,data)
                print(f"✅ Student is updated")
                if student := search_student(id_):
                    student_details(student)
                else:
                    print(f"❌ Can not change user with data {data}")

    elif command == "create":
        data = ask_student_payload_create()
        if data is None:
            return None
        else:
            if not (student := student_create(data)):
                print(f"❌ Can't create user with data: {data}")
            else:
                print(f"✅ New student '{student['name']}' is created")

    elif command == "add marks":
        add_marks_id = input("Enter student's id, you want add marks: ")

        try:
            id_ = int(add_marks_id)
        except ValueError as error:
            raise Exception(f"ID '{add_marks_id}' is not correct value") from error
        else:
            if data := ask_student_payload_add_marks():
                student_add_marks(id_, data)
                print(f"✅ Student marks is added")
                if student := search_student(id_):
                    student_details(student)
                else:
                    print(f"❌ Can not add marks for user  {add_marks_id}")

    else:
        raise SystemExit(f"Unrecognized command: '{command}'")


def handle_user_input():
    """This is an application entrypoint."""

    SYSTEM_COMMANDS = ("quit", "help")
    MANAGEMENT_COMMANDS = ("show", "create", "retrieve", "remove", "change","add marks")
    AVAILABLE_COMMANDS = SYSTEM_COMMANDS + MANAGEMENT_COMMANDS

    help_message = (
        "Welcome to the Journal application. Use the menu to interact with the application.\n"
        f"Available commands: {AVAILABLE_COMMANDS}"
    )

    print(help_message)

    while True:
        command = input("Enter the command: ")

        if command == "quit":
            print(f"\nThanks for using Journal application. Bye!")
            break
        elif command == "help":
            print(help_message)
        elif command in MANAGEMENT_COMMANDS:
            handle_management_command(command=command)
        else:
            print(f"Unrecognized command '{command}'")


handle_user_input()