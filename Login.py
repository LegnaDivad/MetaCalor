from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase
from Notification import Notification

class Login(ft.UserControl):
    
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.texto = ft.Row([
                    ft.Text(value='¿No tienes cuenta?',color='black'),
                    ft.TextButton(text='Registrate aquí',on_click=lambda _: self.page.go('/register'))
                ],alignment=ft.MainAxisAlignment.CENTER)
        
        self.color = '#FFFCF2'
        self.GRIS = '#252422'
        self.usuario = ft.TextField(label='Usuario')
        self.contrasenia = ft.TextField(label='Contraseña',password=True,can_reveal_password=True)
        self.boton = ft.ElevatedButton(text='Iniciar Sesión',style=ft.ButtonStyle(color='black',bgcolor=self.color,surface_tint_color='black'),on_click=self.verificarLogin)

        self.error = ft.Text(value='Alguno de los valores que has proporcionado no es correcto!',color='red')
        self.error.visible=False
        
        self.login = ft.Container(
            expand=True,bgcolor=self.GRIS,height=1025,
            content=ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        width=600,
                        height=460,
                        bgcolor=self.color,
                        padding=ft.padding.all(30),
                        border_radius=ft.border_radius.all(20),
                        content=ft.Column(
                            tight=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,spacing=30,
                            controls=[
                                ft.Text(value='Iniciar Sesión',text_align=ft.TextAlign.CENTER,color='black'),
                                self.usuario,
                                self.contrasenia,
                                self.error,
                                self.boton,
                                self.texto,
                            ]
                        ),
                    )
                ]
            )
        )

    def verificarLogin(self,e):
        datos = [self.usuario.value,self.contrasenia.value]
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.login(datos)
        mydb.close()
        
        if resultado is None:
            Notification(self.page,'Usuario o contraseña incorrectos!','red').mostrar_msg()
            return
        else:
            self.route.setId(resultado)
            print(self.route.returnId())
            self.page.go('/index')
    
    def build(self):        
        return self.login
    
    def inicializar(self):
        print('Inicializando página de Login')