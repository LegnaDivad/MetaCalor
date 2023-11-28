from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue


class RegistroGUI(ft.UserControl):
    def __init__(self,name,iconoSTR,color):
        super().__init__()
        self.name = name
        self.iconoSTR = iconoSTR
        self.color = color
        
        self.GRIS = '#252422'
        
        self.lv = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        
        self.GUI = ft.Container(
            expand=True,
            width=500,height=800,margin=ft.margin.only(left=15),border=ft.border.all(width=1,color='black'),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                height=80,
                                expand=True,
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Row(
                                            [
                                                ft.Icon(),
                                                ft.Icon(name=self.iconoSTR,color=self.color),
                                                ft.Text(value=self.name,color='white',weight='bold'),
                                            ]
                                        ),
                                        ft.IconButton(icon=ft.icons.ADD,on_click=lambda _: self.page.go('/buscador')),
                                    ]
                                ),
                                bgcolor=self.GRIS
                            ),
                        ]
                    ),
                    self.lv
                ]
            )
        )
        
    def agregaralista(self,e):
        self.lv.controls.append(ft.Text('Registro',color='black'))
        self.lv.update()
        
    def build(self):
        return self.GUI
    
    def inicializar(self):
        print('inicializando registroGUI')