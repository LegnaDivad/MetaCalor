import datetime
import flet as ft

def main(page: ft.Page):
    # def change_time(e):
    #     print(f"Time picker changed, value (minute) is {time_picker.value.minute}")

    # def dismissed(e):
    #     print(f"Time picker dismissed, value is {time_picker.value}")

    # time_picker = ft.TimePicker(
    #     confirm_text="Confirm",
    #     error_invalid_text="Time out of range",
    #     help_text="Pick your time slot",
    #     on_change=change_time,
    #     on_dismiss=dismissed,
    #     time_picker_entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
    #     data=ft.Container(
    #         ft.Text('hi')
    #     )
        
    # )
    # time_picker.time_picker_entry_mode
    # page.overlay.append(time_picker)

    # date_button = ft.ElevatedButton(
    #     "Pick time",
    #     icon=ft.icons.TIME_TO_LEAVE,
    #     on_click=lambda _: time_picker.pick_time(),
    # )

    # page.add(date_button)
    r = ft.TextField(
    label="Only numbers are allowed :)",
    input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),
    # input_filter=ft.NumbersOnlyInputFilter()
    )
    
    page.add(r)


ft.app(target=main)
