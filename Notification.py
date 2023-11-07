from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Notification(ft.UserControl):
    def __init__(self,page,msg,color):
        super().__init__()
        self.page = page
        self.msg = msg
        self.color = color
        
        self.content = ft.Text(value=msg,color=color,style=ft.TextThemeStyle.BODY_LARGE)
        self.snack_bar = ft.SnackBar(
            content=self.content,
            elevation=10,
            duration=6000,
            show_close_icon=True,
            behavior=ft.SnackBarBehavior.FLOATING,
            dismiss_direction=ft.DismissDirection.END_TO_START
        )
        
    def mostrar_msg(self):
        self.page.snack_bar = self.snack_bar
        self.snack_bar.open = True
        self.page.update()