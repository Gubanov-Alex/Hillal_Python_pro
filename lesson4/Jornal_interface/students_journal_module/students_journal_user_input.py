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