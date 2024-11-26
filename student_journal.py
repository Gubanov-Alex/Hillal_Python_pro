COMMANDS = ("quit", "show", "look", "add")
""" Available commands: quit, show, retrieve, add """

# Simulated database of the Students
students = [
    {
        "id": "ST1",
        "name": "John Doe",
        "marks": [4, 5, 1, 4, 5, 2, 5],
        "info": "John is 22 y.o. Hobbies: music",
    },
    {
        "id": "ST2",
        "name": "Marry Black",
        "marks": [4, 1, 3, 4, 5, 1, 2, 2],
        "info": "Marry is 23 y.o. Hobbies: football",
    },
{
        "id": "ST3",
        "name": "John Doe",
        "marks": [3, 4, 2, 3, 4, 3, 4],
        "info": "John is 23 y.o. Hobbies: sports",
    },
    {
        "id": "ST4",
        "name": "Jane Smith",
        "marks": [5, 5, 5, 4, 3, 4, 5],
        "info": "Jane is 21 y.o. Hobbies: reading",
    },
    {
        "id": "ST5",
        "name": "Michael Johnson",
        "marks": [2, 3, 2, 2, 4, 2, 1],
        "info": "Michael is 24 y.o. Hobbies: gaming",
    },
    {
        "id": "ST6",
        "name": "Emily Davis",
        "marks": [5, 4, 4, 5, 4, 5, 4],
        "info": "Emily is 20 y.o. Hobbies: painting",
    }
]


def find_students(student_id: str = None, student_name: str = None) -> list:
    """Search for Student functionality (Checking for duplicate names)"""
    results = []
    if student_id:
        results.extend([student for student in students if student["id"] == student_id])
    elif student_name:
        results.extend([student for student in students if student["name"].lower() == student_name.lower()])
    return results

def students_list(show_info: bool = True) -> None:
    """List all students with their details"""
    print("=" * 20)
    print("The list of students:\n")
    for student in students:
        details = f"ID: {student['id']}, Name: {student['name']}. Marks: {student['marks']}"
        if show_info:
            details += f" Details: {student['info']}"
        print(details)

    print("=" * 20)


def show_student(student_id: str = None, student_name:str = None) -> None:
    """Visualization of search results for a specific student"""
    if not student_id and not student_name:
        print("Specify at least student ID or student name.")
        return

    found_students = find_students(student_id, student_name)  #Checking the possibility for the same Name Students

    if not found_students:
        print(f"There is no student with ID {student_id} and name {student_name}.")
        return

    for student in found_students:
        print(
            f"ID: {student['id']}, "
            f"Name: {student['name']}. "
            f"Marks: {student['marks']}\n"
            f"Details: {student['info']}\n"
)


def add_student(student_id: str,student_name: str, info: str | None )-> dict:
    """Adding student functionality"""
    if any(student["id"] == student_id for student in students):
        print(f"Student with ID {student_id} already exists.")
        return None

    instance = {"id": student_id,"name": student_name, "marks": [], "info": info}
    students.append(instance)

    return instance


def main():
    print(f"Welcome to the Digital journal!\nAvailable commands: {', '.join(COMMANDS)}")
    while True:
        user_input = input("Enter the command: ").strip().lower()

        if user_input not in COMMANDS:
            print(f"Command {user_input} is not available.\n")
            continue

        if user_input == "quit":
            print("See you next time.")
            break

        try:
            if user_input == "show":
                show_info = input("Do you want to see additional info? (yes/no): ") == "yes"
                students_list(show_info)
            elif user_input == "look":
                student_id = input("Enter student's ID: ") or None
                student_name = input("Enter student Name you are looking for: ") or None
                show_student(student_id,student_name)
            elif user_input == "add":
                student_id = input("Enter student's ID: ")
                name_st = input("Enter student's name: ")
                info_st = input("Enter details (optional): ") or None
                add_student(student_id,name_st,info_st)
        except NotImplementedError as error:
            print(f"Feature '{error}' is not ready for live.")
        except Exception as error:
            print(error)


if __name__ == "__main__":
    main()