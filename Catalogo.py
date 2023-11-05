from typing import Any, List, Optional, Union
import flet as ft
import datetime
from ProductCard import ProductCard
from CRUD.CRUD_Producto import CrudProducto
from Database import ProductDatabase
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Catalogo(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route

        self.lv = ft.GridView(
            expand=True,
            runs_count=5,
            max_extent=450,
            child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
        )
        
        self.pagAct = False
        
        self.nombreProducto = ft.TextField(label='Nombre de Producto')
        self.descripcion = ft.TextField(label='Descripcion',multiline=True)
        self.precio = ft.TextField(label='Precio')
        self.fecha = datetime.date(2023, 10, 12)
        
    def actualizarPagina(self):
        self.lv.clean()
        mydb = ProductDatabase(self.route)
        mydb.connect()
        # id = self.route.returnId()
        resultado = mydb.seleccionarProductos()
        mydb.close()
        
        for data in resultado:
            self.card = ProductCard(self,data) 
            self.lv.controls.append(self.card)
            self.lv.update()
            self.card = None
        
    def build(self):
        return ft.Container(
            height=900,expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Row(
                        expand=True,
                        controls=[
                            self.lv
                        ]
                    )
                ],
            )
        )
        
    def inicializar(self):
        print('Inicializando página de catálogo')
        self.actualizarPagina()