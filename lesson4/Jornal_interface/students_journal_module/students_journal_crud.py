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

def student_add_marks(id_: int, payload: dict) -> dict:
    """Add marks to student"""
    global students
    try:
        marks_add = students[id_].copy()
    except KeyError:
        raise ValueError(f"Student with id {id_} does not exist")

    else:
        marks_add["marks"].extend(payload["marks"])
        students[id_] = marks_add
        return marks_add