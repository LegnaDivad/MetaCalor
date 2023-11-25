from typing import Any, List, Optional, Union
from flet import *
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Perfil(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.perfilcont = Container(
            expand=True,
            content=Text('Este es el perfil de usuario',color='black')
        )
        
    def build(self):
        return self.perfilcont
        
    def inicializar(self):
        print('Inicializando Perfil')