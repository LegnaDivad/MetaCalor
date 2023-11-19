from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Cartas import CartaRegistroAlimento
from Database import UserDatabase

class Index(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        self.lvDesayuno = ft.ListView(expand=True,padding=20,auto_scroll=True)
        self.lvAlmuerzo = ft.ListView(expand=True,padding=20,auto_scroll=True)
        self.lvCena = ft.ListView(expand=True,padding=20,auto_scroll=True)
        
        self.desayuno = ft.Card(
            expand=True,key='desayuno',
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.SUNNY,color='orange',size=25),
                                            ft.Text(value='Desayuno',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',on_click=self.buscadorDesayuno),
                                                    ft.Text('Registrar alimento',color='white')
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',on_click=lambda _: self.page.go('/buscador')),
                                                    ft.Text('Registrar Platillo',color='white')
                                                ]
                                            ),
                                            
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    ft.Container(
                        expand=True,
                        content=self.lvDesayuno
                    )
                ]
            ),
            color='#A7C957',
        )
        
        self.almuerzo = ft.Card(
            expand=True,key='almuerzo',
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.CLOUD,color='blue',size=25),
                                            ft.Text(value='Almuerzo',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',on_click=self.buscadorAlmuerzo),
                                                    ft.Text('Registrar alimento',color='white')
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',on_click=lambda _: self.page.go('/buscador')),
                                                    ft.Text('Registrar Platillo',color='white')
                                                ]
                                            ),
                                            
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    self.lvAlmuerzo
                ]
            ),
            color='#6A994E',
        )
        
        self.cena = ft.Card(
            expand=True,key='cena',
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.NIGHTLIGHT,color='purple',size=25),
                                            ft.Text(value='Cena',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',on_click=self.buscadorCena),
                                                    ft.Text('Registrar alimento',color='white')
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',on_click=lambda _: self.page.go('/buscador')),
                                                    ft.Text('Registrar Platillo',color='white')
                                                ]
                                            ),
                                            
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    self.lvCena
                ]
            ),
            color='#386641',
        )
        
        self.cont = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.ElevatedButton(text='Presioname',on_click=self.agregarComidas),
                    ft.Row(
                        expand=True,
                        controls=[
                            self.desayuno,
                            self.almuerzo,
                            self.cena
                        ]
                    )
                ]
            )
        )
        
    def buscadorDesayuno(self,e):
        self.route.buscador.establecer_Horario('desayuno')
        self.page.go('/buscador')
        
    def buscadorAlmuerzo(self,e):
        self.route.buscador.establecer_Horario('almuerzo')
        self.page.go('/buscador')
        
    def buscadorCena(self,e):
        self.route.buscador.establecer_Horario('cena')
        self.page.go('/buscador')
        
    def agregarComidas(self):
        self.lvDesayuno.clean()
        self.lvAlmuerzo.clean()
        self.lvCena.clean()
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.ObtenerRegistros(self.route.getId())
        mydb.close()
        
        for data in resultado:
            if data[2] == 'desayuno':
                item = CartaRegistroAlimento(self.route,data)
                self.lvDesayuno.controls.append(item)
            elif data[2] == 'almuerzo':
                item = CartaRegistroAlimento(self.route,data)
                self.lvAlmuerzo.controls.append(item)
            elif data[2] == 'cena':
                item = CartaRegistroAlimento(self.route,data)
                self.lvCena.controls.append(item)
        self.cont.update()
        
    def build(self):
        return self.cont
    
    def inicializar(self):
        self.route.page.bgcolor = '#F2E8CF'
        self.agregarComidas()
        print('Inicializando Index')