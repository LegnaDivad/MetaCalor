from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import FoodDatabase
from Notification import Notification

class Search(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        
        self.SearchButtom = ft.ElevatedButton(text='Buscar',icon=ft.icons.SEARCH,on_click=self.buscarElementos)
        self.SearchText = ft.TextField(label='Nombre de Alimento',expand=True,color='black')
        
        self.SearchList = ft.ListView(
            expand=1,padding=20,auto_scroll=True,
        )
        
        self.buscadorGUI = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            self.SearchText,
                            self.SearchButtom
                        ]
                    )
                ),
                ft.Container(
                    expand=True,border=ft.border.all(width=1,color='black'),
                    content=self.SearchList
                )
            ]
        )
        
    def buscarElementos(self,e):
        self.SearchList.clean()
        mydb = FoodDatabase(self.route)
        mydb.connect()
        
        if self.SearchText.value == '':
            return
            
        dato = self.SearchText.value
        resultado = mydb.ObtenerAlimentos(dato)
        mydb.close()
        
        for datos in resultado:
            item = ft.Container(
                expand=True,height=80,margin=8,border=ft.border.all(width=1,color='black'),
                content=ft.Row(
                    expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(),
                                ft.Text(value=f'Alimento: {datos[0]} | Categoria: {datos[1]}',text_align='center',color='black'),
                            ]
                        ),
                        ft.Row(
                            controls=[
                            ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30),
                            ft.Icon(),
                            ]
                        ),
                    ]
                )
            )
            self.SearchList.controls.append(item)
            
        self.SearchList.update()
        
    def build(self):
        return self.buscadorGUI
    
    def inicializar(self):
        self.SearchText.value = None
        self.SearchText.update()
        self.SearchList.clean()
        print('Inicializando buscador')