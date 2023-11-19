from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from RegistroGUI import RegistroGUI

class Index(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.desayuno = RegistroGUI('Desayuno','SUNNY','orange')
        self.almuerzo = RegistroGUI('Almuerzo','CLOUD','blue')
        self.cena = RegistroGUI('Cena','nightlight','purple')
        
        self.index = ft.Container(
            expand=True,
            content=ft.Row(
                expand=True,
                spacing=60,
                controls=[
                    self.desayuno,self.almuerzo,self.cena
                ],
            )
        )
        
    def build(self):
        return self.index
    
    def inicializar(self):
        self.route.registroGUI.inicializar()
        self.route.page.bgcolor = 'white'
        print('Inicializando Index')