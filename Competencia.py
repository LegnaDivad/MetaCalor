from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase, MetaDatabase
from Cartas import CartaMeta
import datetime

class Competencia(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#4D4D4D'
        self.lvMeta = ft.ListView(expand=3,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        # -- Controles para el apartado de Usuario
        self.usuario = ft.Text(color=self.GRIS,size=34,font_family="Arial Black",weight=ft.FontWeight.BOLD,)
        
        self.valorMeta = ft.Text('Hola',color=self.GRIS,size=20,weight=ft.FontWeight.BOLD)
        self.valorMetaNumero = ft.Text('Adiós',color=self.GRIS,size=20,weight=ft.FontWeight.BOLD)
        self.nickname = ft.Text(color='black',weight=ft.FontWeight.BOLD)
        
        
        self.nicknameUsuario = ft.Container(
            height=60,width=240,
            bgcolor='white',
            border_radius=ft.border_radius.all(14),
            alignment=ft.alignment.center,
            content=self.nickname
        )
        self.MetaUsuario = ft.Container(
            height=130,width=390,
            bgcolor='#eff1ed',
            border_radius=ft.border_radius.all(14),
            alignment=ft.alignment.center,
            content=ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text('Te encuentras en el lugar: ',color='black',weight=ft.FontWeight.BOLD,size=20),
                            ft.Row(alignment=ft.alignment.center,controls=[ft.Icon(ft.icons.SPORTS_SCORE_OUTLINED,color='black',size=60),
                            ft.Text('2°',color='black',weight=ft.FontWeight.BOLD,size=30)]),
                            
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

                        content= ft.Image(
                                src="/images/gato.PNG",
                                width=400,
                                height=145,
                                fit=ft.ImageFit.CONTAIN,
                            ),
                    ),
                    ft.Container(
                        expand=4,
                        content=ft.Column(
                            expand=True,
                            controls=[
                                ft.Row(controls=[ft.Text("      "),self.usuario,]),
                                
                                self.nicknameUsuario,
                                self.MetaUsuario
                            ]
                        )
                    )
                ]   
            )
        )
        
        self.metasCumplidasText = ft.Text(color='black',weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER)
        # -- Cartas de Estadísticas
        self.MetaCumplidas = ft.Container(
            bgcolor='#eff1ed',
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
                    self.metasCumplidasText,
                    ft.Text('Meta cumplidas',color='black',weight=ft.FontWeight.BOLD),
                ]
            )
        )
        
        self.metasCText = ft.Text(color='black',weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER)
        self.MetaPorCumplir = ft.Container(
            bgcolor='#eff1ed',
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
                    self.metasCText,
                    ft.Text('Meta por cumplir',color='black',weight=ft.FontWeight.BOLD),
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
                                self.MetaCumplidas,
                                self.MetaPorCumplir,
                            ]
                        )
                    )
                ]
            )
        )
        
        # -- Apartado de Meta Actuales
        self.MetaActuales = ft.Container(
            expand=True,
            # bgcolor='green',
            border_radius=ft.border_radius.all(25),
            content=ft.Column(
                controls=[
                    ft.Text(value='Meta Actuales',color=self.GRIS,size=34,weight=ft.FontWeight.BOLD,expand=1),
                    self.lvMeta
                ]
            )
        )
        
        self.contenedorTop = ft.Container(
            padding=40,
            expand=True,
            bgcolor='#eff1ed',
            border_radius=ft.border_radius.all(15),
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=1,
                        bgcolor='#E5E5E5',
                        border_radius=ft.border_radius.all(30),
                        content=ft.Column(
                            expand=True,
                            # alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    expand=True,
                                    bgcolor='#040273',
                                    alignment=ft.alignment.center,
                                    content=ft.Text(size=40,color='White',value='TOP',weight=ft.FontWeight.BOLD)
                                ),
                                

                            ]
                        )
                    ),
                    
       
                    ft.Column(
                        expand=7,
                        controls =[
                            ft.Container(
                                    expand=True,
                                    bgcolor='#FFD700',
                                    alignment=ft.alignment.center,
                                    content=ft.Text(size=30,color='black',value='First Place')
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor='#C0c0c0',
                                    alignment=ft.alignment.center,
                                    content=ft.Text(size=30,color='black',value='Second Place')
                                ),
                                ft.Container(
                                    expand=True,
                                    bgcolor='#cd7f32',
                                    alignment=ft.alignment.center,
                                    content=ft.Text(size=30,color='black',value='Third Place')
                                ),
                        ]
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
                            # expand=True,
                            controls=[
                                self.infoUsuario,
                                self.estadisticas,
                                self.MetaActuales
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
        # resultado = mydb.verificarMeta(self.route.getId(),fecha)
        
    def set_Datos(self,datos):
        self.nickname.value = datos[0]
        self.usuario.value = datos[3]
        
    def cargarMeta(self):
        self.lvMeta.clean()
        mydb = MetaDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerMeta(self.route.getId())
        mydb.close()
        
        for dato in resultado:
            item = CartaMeta(self.route,dato)
            self.lvMeta.controls.append(item)
        self.lvMeta.update()
        
        self.metasCumplidasText.value = resultado[0][3]
        self.metasCumplidasText.update()
        

    
    def build(self):
        return self.index
    
    def inicializar(self):
        self.cargarMeta()
        print('Inicializando Competencia')