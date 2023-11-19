from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import FoodDatabase
from Notification import Notification
from Cartas import CartaBuscador
from AlertDialog import RegisterDialog

class Search(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.focused_color = '#26587E'
        self.GRIS = '#4D4D4D'
        
        self.SearchButtom = ft.ElevatedButton(
            text='Buscar',
            icon=ft.icons.SEARCH,
            on_click=self.buscarElementos,
            style=ft.ButtonStyle(
                color="#26587E",
                bgcolor="#E3E9F0"
            )
        )
        
        self.SearchText = ft.TextField(
            label='Nombre de Alimento',
            autofocus=True,
            focused_color=self.focused_color,
            text_style=ft.TextStyle(color=self.GRIS),
            focused_border_color=self.GRIS,
            label_style=ft.TextStyle(color=self.GRIS),
            expand=True,
            color='black'
        )
        
        self.SearchList = ft.ListView(expand=1,padding=20,auto_scroll=True,)
        
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
                    expand=True,
                    content=self.SearchList
                )
            ]
        )
        
    def establecer_Horario(self,string):
        self.horario = string
        print(self.horario)
        
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
            item = CartaBuscador(self.route,datos)
            self.SearchList.controls.append(item)
        self.SearchList.update()
        
    def build(self):
        return self.buscadorGUI
    
    def inicializar(self):
        self.route.page.bgcolor = '#F2E8CF'
        self.SearchText.value = None
        self.SearchText.update()
        self.SearchList.clean()
        print('Inicializando buscador')