from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Appbar(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        
        self.nickname = ft.Text()
    
        self.bar = ft.AppBar(
            # leading=ft.Icon(ft.icons.PALETTE),
            leading_width=40,
            toolbar_height=80,
            title=ft.Image(
                src=f"/images/Logo3.PNG",
                width=380,
                height=85,
                fit=ft.ImageFit.CONTAIN,
            ),
            center_title=False,
            bgcolor=self.GRIS,
            actions=[
                self.nickname,
                ft.IconButton(
                    icon=ft.icons.NOTIFICATIONS_OUTLINED,
                    icon_size=40,
                ),
                ft.Icon(),
                ft.PopupMenuButton(
                    content=ft.Icon(ft.icons.PERSON_ROUNDED,size=40),
                    items=[
                        ft.PopupMenuItem(text="Perfil de Usuario"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(text="Cerrar Sesión",on_click=self.cerrarSesion),
                    ]
                ),
                ft.Icon(),
                ft.Icon(),
            ],
        )
        
    def cerrarSesion(self,e):
        self.nickname.value = ''
        self.route.menu.cont.visible = False
        self.route.page.appbar.visible = False
        self.route.menu.update()
        self.route.page.update()
        self.route.page.go('/')
        
    def set_Nickname(self,texto):
        self.nickname.value = texto
        self.route.page.update()
        
    def build(self):
        return self.bar