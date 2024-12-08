import PySimpleGUI as sg
import base64
import json
from pathlib import Path
from students_journal_module import represent_students, search_student, ask_student_payload_update, update_student, \
    ask_student_payload_add, add_student, delete_student, calculate_summary, ask_student_payload_add_marks, \
    student_add_marks



SYSTEM_COMMANDS = ("quit", "help")
MANAGEMENT_COMMANDS = ("show", "create", "retrieve", "remove", "change", "add marks")
AVAILABLE_COMMANDS = SYSTEM_COMMANDS + MANAGEMENT_COMMANDS

help_message = """Here are details of the available commands:
- quit: finish the application
- help: show this help message
- show: journal entries list
- create: add student
- retrieve: find student 
- remove: delete student data
- change: update student data
- add marks: add marks to student data
"""

# ==================================================
# Simulated storage
# ==================================================

files_dir = Path(__name__).absolute().parent / "files1"
storage_file = "students.json"


class StudentsStorage:
    def __init__(self) -> None:
        self.students = self.read_json(storage_file)

    def __len__(self):
        return len(self.students)

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





with open("journal_demo.png", "rb") as image_file:
    PSG_GRAPHIC = base64.b64encode(image_file.read())


# ==================================================
# START POINT
# ==================================================


def main():
    sg.theme('Darkblack')
    BLUE_BUTTON_COLOR = '#FFFFFF on #2196f2'
    GREEN_BUTTON_COLOR ='#FFFFFF on #00c851'
    LIGHT_GRAY_BUTTON_COLOR = f'#212021 on #e0e0e0'
    DARK_GRAY_BUTTON_COLOR = '#e0e0e0 on #212021'
    RED_BUTTON_COLOR = '#FFFFFF on #FF0000'
    YELLOW_BUTTON_COLOR = '#212021 on #FFFF00'

    total_students, average_marks = calculate_summary()

    layout = [[sg.Col([[sg.T("Welcome to Students Journal Application.\n",font=("Helvetica", 22, "italic"),
                             text_color="blue",justification='center')],
                            [sg.T("Use the menu to interact with the application.\n",font=("Helvetica", 14, "italic"),
                             justification='center',text_color="white")],
                            [sg.T(f"Available commands: {AVAILABLE_COMMANDS}",font=("Helvetica", 18, "italic"),
                             justification='center',text_color="green")],
                       [sg.T('Choose the command with button below: ')],
                       [sg.B('help', size=(10,2),button_color=LIGHT_GRAY_BUTTON_COLOR), sg.B('quit', size=(10,2), button_color=DARK_GRAY_BUTTON_COLOR)],
                       [sg.T()],
                       [sg.Image(data=PSG_GRAPHIC)],
                       [sg.T()],
                       [sg.B('retrieve', size=(14,2), button_color=DARK_GRAY_BUTTON_COLOR),
                        sg.B('show', size=(17, 3), button_color=BLUE_BUTTON_COLOR),
                        sg.B('change', size=(14,2), button_color=LIGHT_GRAY_BUTTON_COLOR)],
                       [sg.B('create', size=(14,2), button_color=GREEN_BUTTON_COLOR),
                        sg.B('add marks', size=(14, 2), button_color=YELLOW_BUTTON_COLOR),
                        sg.B('remove', size=(14,2), button_color=RED_BUTTON_COLOR)],
                       [sg.T(f'-TOTAL_STUDENTS-: {total_students}',
                             size=(40, 1), key='-TOTAL_STUDENTS-', font=("Helvetica", 12))],
                       [sg.T(f'-AVERAGE_SCORE-: {average_marks}',
                             size=(40, 1), key='-AVERAGE_SCORE-', font=("Helvetica", 12))],
                       [sg.T('Hillal Pyton_pro(30.11.2024)')]], element_justification='c', k='-TOP COL-')]]

    window = sg.Window('Window Title', layout)
    show_animation = False

    while True:             # Event Loop
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'quit':
            break

        elif event == 'help':
            sg.popup(help_message, title="Help")

        elif event == 'show':
            sg.popup(represent_students(), title="Students Journal",font=("Helvetica", 15, "italic"))

        elif event == 'retrieve':
            search_id = sg.popup_get_text('Input Student ID:', title='Student Search')
            if search_id is not None:
                try:
                    id_ = int(search_id)
                    student = search_student(id_)
                    if student is not None:
                        sg.popup(search_student(id_), title="Students Search",font=("Helvetica", 14, "italic"))
                    else :
                        sg.popup("Student ID not found", title="Input Error")
                except ValueError as e:
                        sg.popup("Invalid value for ID", title="Input Error")

        elif event == 'change':
            update_id = sg.popup_get_text('Input Student ID:', title='Student data change')
            if update_id is not None:
                try:
                    id_ = int(update_id)
                    student = search_student(id_)
                    if student is not None:
                        sg.popup(search_student(id_), title="Students Search", font=("Helvetica", 14, "italic"))
                        if data := ask_student_payload_update() :
                            update_student(id_, data)
                            sg.popup("✅ Student is updated", title="Student data change")
                        else:
                            sg.popup("❌ Student is not updated", title="Student data change")
                    else :
                        sg.popup("Student ID not found", title="Input Error")
                except ValueError as e:
                    sg.popup("Invalid value for ID", title="Input Error")
                #
                total_students, average_marks = calculate_summary()
                window['-TOTAL_STUDENTS-'].update(f'-TOTAL_STUDENTS: {total_students}')
                window['-AVERAGE_SCORE-'].update(f'-AVERAGE_SCORE-: {average_marks}')

        elif event == 'add marks':
            add_marks_id = sg.popup_get_text('Input Student ID:', title='Student add marks')
            if add_marks_id is not None:
                try:
                    id_ = int(add_marks_id)
                    student = search_student(id_)
                    if student is not None:
                        sg.popup(search_student(id_), title="Students Search", font=("Helvetica", 14, "italic"))
                        if data := ask_student_payload_add_marks() :
                            student_add_marks(id_, data)
                            sg.popup("✅ Student marks is add", title='Student add marks')
                        else:
                            sg.popup("❌ Student marks is not added", title='Student add marks')
                    else :
                        sg.popup("Student ID not found", title="Input Error")
                except ValueError as e:
                    sg.popup("Invalid value", title="Input Error")

                total_students, average_marks = calculate_summary()
                window['-TOTAL_STUDENTS-'].update(f'-TOTAL_STUDENTS: {total_students}')
                window['-AVERAGE_SCORE-'].update(f'-AVERAGE_SCORE-: {average_marks}')


        elif event == 'create':
            data = ask_student_payload_add()
            if data is None:
                return None
            else:
                if not (student := add_student(data)):
                    sg.popup(f"❌ Can't create user with data: {data}", title="Input Error")
                else:
                    sg.popup(f"✅ New student '{student['name']}' is created", title="Student added")

                total_students, average_marks = calculate_summary()
                window['-TOTAL_STUDENTS-'].update(f'-TOTAL_STUDENTS: {total_students}')
                window['-AVERAGE_SCORE-'].update(f'-AVERAGE_SCORE-: {average_marks}')

        elif event == 'remove':

            delete_id =sg.popup_get_text('Input Student ID:', title="Students delete", font=("Helvetica", 14, "italic"))
            try:
                id_ = int(delete_id)
                student = search_student(id_)
                if student is not None:
                    delete_student(id_)
                    sg.popup("✅ Student is deleted", title="Student data delete")

                    total_students, average_marks = calculate_summary()
                    window['-TOTAL_STUDENTS-'].update(f'-TOTAL_STUDENTS: {total_students}')
                    window['-AVERAGE_SCORE-'].update(f'-AVERAGE_SCORE: {average_marks}')
                else:
                    sg.popup("Student ID not found", title="Input Error")
                    sg.popup("❌ Student is not deleted", title="Student data delete")
            except ValueError :
                sg.popup("Invalid value for ID", title="Input Error")

            total_students, average_marks = calculate_summary()
            window['-TOTAL_STUDENTS-'].update(f'-TOTAL_STUDENTS: {total_students}')
            window['-AVERAGE_SCORE-'].update(f'-AVERAGE_SCORE-: {average_marks}')


    window.close()

if __name__ == '__main__':
    main()