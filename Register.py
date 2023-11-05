from typing import Any, List, Optional, Union
import flet as ft
# from CRUD.CRUD_Usuario import CrudUsuario
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class Register(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.color = '#FFFCF2'
        self.GRIS = '#252422'
        self.usuario = ft.TextField(label='Usuario')
        self.apellidos = ft.TextField(label='Correo')
        self.nombre = ft.TextField(label='Nombre')
        self.codigo = ft.TextField(label='Codigo')
        self.contrasenia = ft.TextField(label='Contraseña',password=True)
        self.contrasenia2 = ft.TextField(label='Confirmar Contraseña')
        self.boton = ft.ElevatedButton(text='Registrarse',style=ft.ButtonStyle(color='black',bgcolor=self.color,surface_tint_color='black'))
        
    def build(self):
        return ft.Container(
            expand=True,height=1025,bgcolor=self.GRIS, #height=935
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        height=560,
                        width=725,
                        bgcolor=self.color,
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=30,
                            controls=[
                                ft.Text('Registro de Usuario',color='black'),
                                    ft.Row([
                                        self.nombre,
                                        self.apellidos
                                    ],alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        self.usuario,
                                        self.codigo
                                    ],alignment=ft.MainAxisAlignment.CENTER),
                                    ft.Row([
                                        self.contrasenia,
                                        self.contrasenia2
                                    ],alignment=ft.MainAxisAlignment.CENTER),
                                self.boton,
                                ft.Text(value='¿Ya tienes cuenta?'),
                                ft.TextButton(text='Inicia Sesión',on_click=lambda _: self.page.go('/'))
                            ]
                        )
                    )
                ]
            )
        )
        
    def inicializar(self):
        print('Inicializando página de Registro')