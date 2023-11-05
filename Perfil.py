from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase

class Perfil(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.correo = ft.TextField(label='Correo',)
        self.nombre = ft.TextField(label='Nombre',)
        self.usuario = ft.TextField(label='Usuario',)
        self.codigo = ft.TextField(label='Código de Alumno',)
        self.contrasenia = ft.TextField(label='Contraseña actual',password=True,can_reveal_password=True)
        self.contrasenia2 = ft.TextField(label='Nueva contraseña',password=True,can_reveal_password=True)
        
        self.textUser = ft.Text(color='black')
        
        self.perfil = ft.Container(
            expand=True,
            # alignment=ft.alignment.center,
            content=ft.Column(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=50,
                controls=[
                    ft.Row( # Avatar y nombre
                        controls=[
                            ft.CircleAvatar(icon=ft.icons.PERSON,color=ft.colors.TRANSPARENT),
                            self.textUser
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row( # Correo y nombre
                        controls=[
                            self.correo,
                                self.nombre
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row( # Usuario y código
                        controls=[
                            self.usuario,
                            self.codigo
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row( # Contraseña actual y nueva contraseña
                        controls=[
                            self.contrasenia,
                            self.contrasenia2
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    ft.Row(
                        controls=[
                            ft.ElevatedButton(text='Guardar',)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ]
            )
        )
        
    def set_Name(self):
        mydb = UserDatabase(self.route)
        mydb.connect()
        id = self.route.returnId()
        resultado = mydb.ObtenerUsuario(id)
        mydb.close()
        
        self.textUser.value = resultado
        self.textUser.update()
        
    def build(self):
        return self.perfil
    
    def inicializar(self):
        self.set_Name()
        print('Inicializando página de Perfil')