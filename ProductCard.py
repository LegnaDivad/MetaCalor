from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class ProductCard(ft.UserControl):
    def __init__(self, route,data):
        super().__init__()
        self.route = route
        self.data = data

        self.card = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column(
                    expand=True,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            src=f"https://mymodernmet.com/wp/wp-content/uploads/2022/02/how-to-draw-a-book-1.jpg",
                            width=300,
                            height=200,
                            fit=ft.ImageFit.NONE,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                            border_radius=ft.border_radius.all(10),
                        ),
                        ft.Text(value=self.data[0],color='Black',weight=ft.FontWeight.BOLD),
                        ft.Text(value=f'${self.data[1]}',color='black'),
                        ft.Text(value=f'Vendedor: {self.data[2]}',color='black'),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton('Ver Información'),
                                ft.ElevatedButton('Agregar al Carrito'),
                            ],alignment=ft.MainAxisAlignment.CENTER
                        )
                    ]
                )
            ),
            width=800,color='white'
        )
        
    def build(self):
        return self.card