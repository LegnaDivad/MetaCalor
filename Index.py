from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Index(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.color = '#FFFCF2'
        self.GRIS = '#252422'
        
        self.texto1 = ft.Container(
                                ft.Text('CuceiComparte',size=40,color=self.color,weight=ft.FontWeight.BOLD),margin=ft.margin.only(left=35)
                        )
        self.texto2 = ft.Container(
                                ft.Text('Multiplica tu aprendizaje, comparte tu sabiduría; Cada recurso que compartes es una oportunidad de crecimiento y una fuente de recompensas',color=self.color,size=20,weight=ft.FontWeight.BOLD),margin=ft.margin.only(left=100)
                        )
        
        self.index = ft.Container( # Cuadro CuceiComparte
                        width=1000,height=600,bgcolor=self.GRIS,margin=ft.margin.only(left=80,top=110),
                        content=ft.Column([
                            self.texto1,
                            self.texto2
                        ],alignment=ft.MainAxisAlignment.CENTER,spacing=20)
                    )
        
    def build(self):
        return self.index
    
    def inicializar(self):
        print('Inicializando Index')