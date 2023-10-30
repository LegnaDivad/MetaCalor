from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Appbar(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.verde = '#6A994E'
        
        self.nickname = ft.Text()
    
        self.bar = ft.AppBar(
            # leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            toolbar_height=60,
            title=ft.Text("MetaCalor"),
            center_title=False,
            bgcolor=self.verde,
            actions=[
                self.nickname,
                ft.IconButton(
                    icon=ft.icons.NOTIFICATIONS_OUTLINED,
                    icon_size=40,
                ),
                ft.PopupMenuButton(
                    content=ft.Icon(ft.icons.PERSON_ROUNDED,size=40),
                    items=[
                        ft.PopupMenuItem(text="Perfil de Usuario"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(text="Cerrar Sesión",on_click=self.cerrarSesion),
                    ]
                ),
            ],
        )
        
    def cerrarSesion(self,e):
        self.nickname.value = ''
        self.route.page.update()
        self.route.page.go('/')
        
    def set_Nickname(self,texto):
        self.nickname.value = texto
        self.route.page.update()
        
    def build(self):
        return self.bar