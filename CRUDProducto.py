from typing import Any, List, Optional, Union
import flet as ft

from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

from Catalogo import Catalogo
from Database import ProductDatabase
import datetime

class CRUDProducto(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.catalogo = Catalogo(self)
        
        self.color = '#FFFCF2'
        self.GRIS = '#252422' 
        
        self.nombreProducto = ft.TextField(label='Nombre de Producto')
        self.descripcion = ft.TextField(label='Descripcion',multiline=True)
        self.precio = ft.TextField(label='Precio')
        self.fecha = datetime.date(2023, 10, 12)
        
        self.categoria = ft.Dropdown(
            width=200,
            options=[
                ft.dropdown.Option("Libros"),
                ft.dropdown.Option("AudioLibros"),
                ft.dropdown.Option("Cursos"),
            ],
        )

    def registrarProducto(self,e):
        mydb = ProductDatabase(self.route)
        mydb.connect()
        id = self.route.returnId()
        datos = [self.nombreProducto.value,float(self.precio.value),self.categoria.value,id]
        resultado = mydb.registrarProducto(datos)
        mydb.close()
        
        if resultado == 'introducido':
            print('insertado')
        else:
            print('error')

    def build(self):
        return ft.Row(
            expand=True,
            height=900,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    width=725,height=560,padding=15,
                    bgcolor=self.color,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            self.nombreProducto,
                            self.descripcion,
                            self.precio,
                            self.categoria,
                            ft.ElevatedButton(text='Subir Imagen'),
                            ft.ElevatedButton(text='Subir Producto',on_click=self.registrarProducto)
                        ]
                    )
                )
            ]
        )
        
    def inicializar(self):
        print('Inicializando página de CRUDProductos')
        self.update()