from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Index(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.index = ft.Container(
            expand=True,
            content=ft.Text(value='Hola',color='black')
        )
        
    def build(self):
        return self.index
    
    def inicializar(self):
        print('Inicializando Index')