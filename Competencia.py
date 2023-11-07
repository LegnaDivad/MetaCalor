from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Competencia(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.index = ft.Container(
            expand=True,
            content=ft.Text(value='Aquí se mostrará el ranking',color='black')
        )
        
    def build(self):
        return self.index
    
    def inicializar(self):
        print('Inicializando Competencia')