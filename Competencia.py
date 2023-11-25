from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Competencia(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#4D4D4D'
        
        # -- Controles para el apartado de Usuario
        self.usuario = ft.Text(value='Usuario',color=self.GRIS,size=34,font_family="Arial Black",weight=ft.FontWeight.BOLD,)
        self.nicknameUsuario = ft.Container(
            height=60,width=240,
            bgcolor='white',
            border_radius=ft.border_radius.all(14),
            alignment=ft.alignment.center,
            content=ft.Text(value='nickname',color='black',weight=ft.FontWeight.BOLD)
        )
        self.metasUsuario = ft.Container(
            height=130,width=390,
            bgcolor='white',
            border_radius=ft.border_radius.all(14),
            alignment=ft.alignment.center,
            content=ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text('2',color='black',weight=ft.FontWeight.BOLD),
                            ft.Text('Metas Cumplidas',color='black',weight=ft.FontWeight.BOLD),
                        ]
                    ),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text('2',color='black',weight=ft.FontWeight.BOLD),
                            ft.Text('Top',color='black',weight=ft.FontWeight.BOLD),
                        ]
                    )
                ]
            )
        )
        
        # -- Apartados de Usuario
        self.infoUsuario = ft.Container(
            expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Container( ##Para la imagen
                        width=300,
                        height=400,
                        bgcolor='red',
                        content=ft.Text('imagen',color='black',)
                    ),
                    ft.Container(
                        expand=4,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                self.usuario,
                                self.nicknameUsuario,
                                self.metasUsuario
                            ]
                        )
                    )
                ]   
            )
        )
        
        # -- Cartas de Estadísticas
        self.metasCumplidas = ft.Container(
            bgcolor='white',
            height=220,width=330,
            border_radius=ft.border_radius.all(25),
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        bgcolor='#E5E5E5',
                        height=105,width=190,
                        border_radius=ft.border_radius.all(14),
                        alignment=ft.alignment.center,
                        content=ft.Icon(ft.icons.CHECK,color='black',size=60)
                    ),
                    ft.Text('1',color='black',weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER),
                    ft.Text('Metas cumplidas',color='black',weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        self.metasPorCumplir = ft.Container(
            bgcolor='white',
            height=220,width=330,
            border_radius=ft.border_radius.all(25),
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        bgcolor='#E5E5E5',
                        height=105,width=190,
                        border_radius=ft.border_radius.all(14),
                        alignment=ft.alignment.center,
                        content=ft.Icon(ft.icons.PRIORITY_HIGH,color='black',size=60)
                    ),
                    ft.Text('1',color='black',weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER),
                    ft.Text('Metas por cumplir',color='black',weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        # -- Apartado Estadísticas
        self.estadisticas = ft.Container(
            expand=True,
            # bgcolor='green',
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Text(value='Estadísticas',color=self.GRIS,size=34,weight=ft.FontWeight.BOLD,expand=1),
                    ft.Container(
                        expand=3,
                        # bgcolor='black'
                        content=ft.Row(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                self.metasCumplidas,
                                self.metasPorCumplir,
                            ]
                        )
                    )
                ]
            )
        )
        
        # -- Apartado de Metas Actuales
        self.metasActuales = ft.Container(
            expand=True,
            # bgcolor='green',
            border_radius=ft.border_radius.all(25),
            content=ft.Column(
                controls=[
                    ft.Text(value='Metas Actuales',color=self.GRIS,size=34,weight=ft.FontWeight.BOLD,expand=1),
                    ft.Container(
                        expand=3,
                        width=800,
                        padding=30,
                        bgcolor='white',
                        alignment=ft.alignment.center,
                        content=ft.Row(
                            expand=True,
                            controls=[
                                ft.Container(
                                    expand=1,
                                    border_radius=ft.border_radius.all(25),
                                    bgcolor='#E5E5E5',
                                    padding=30,
                                    content=ft.Icon(ft.icons.EMOJI_EVENTS,color='black',size=60)
                                ),
                                ft.Column(
                                    expand=3,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Row(
                                            # expand=True,
                                            # run_spacing=-30,
                                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                            controls=[
                                                ft.Text('1200 Calorias',color='black',size=15,weight=ft.FontWeight.BOLD,),
                                                ft.Text('7000/12000',color='black',size=15,weight=ft.FontWeight.BOLD,),
                                            ]
                                        ),
                                        ft.Text('Aca un progressbar')
                                    ]
                                )
                            ]
                        )
                    )
                ]
            )
        )
        
        self.contenedorTop = ft.Container(
            padding=40,
            expand=True,
            bgcolor='white',
            border_radius=ft.border_radius.all(15),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=1,
                        bgcolor='#E5E5E5',
                        border_radius=ft.border_radius.all(30),
                        content=ft.Row(
                            expand=True,
                            # alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    alignment=ft.alignment.center,
                                    content=ft.Text(size=30,color='black',value='TOP')
                                )
                            ]
                        )
                    ),
                    ft.Container(
                        expand=7,
                        bgcolor='#E5E5E5',
                    )
                ]
            )
        )
        
        self.index = ft.Container(
            expand=True,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Container(
                        expand=2,
                        # bgcolor='blue',
                        padding=15,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                self.infoUsuario,
                                self.estadisticas,
                                self.metasActuales,
                            ]
                        )
                    ),
                    ft.Container(
                        expand=1,
                        padding=60,
                        content=self.contenedorTop
                    ),
                ]
            )
        )
        
    def build(self):
        return self.index
    
    def inicializar(self):
        print('Inicializando Competencia')