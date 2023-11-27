from typing import Any, List, Optional, Union
from flet import *
import datetime

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class RegistroPlatillo(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        
        self.contenedor = Container(
            expand=True,
            
        )