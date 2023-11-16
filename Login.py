from typing import Any, List, Optional, Union
from flet import *
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase
from Notification import Notification

class Login(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.usuario = TextField(label='Usuario',icon=icons.PERSON_2_OUTLINED,width=450)
        self.contrasenia = TextField(label='Contraseña',icon=icons.LOCK_CLOCK_OUTLINED,width=450,password=True,can_reveal_password=True)
        self.botonLogin = ElevatedButton(text='Iniciar Sesión',icon=icons.LOGIN,style=ButtonStyle(bgcolor='white'),on_click=self.login)
        
        self.loginGUI = Container(
            expand=True,
            alignment=alignment.center,
            content=Container(
                height=500,width=700,
                border=border.all(1,'black'),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        Text('Iniciar Sesión'),
                        self.usuario,
                        self.contrasenia,
                        self.botonLogin,
                        TextButton(text='Registrate aquí',on_click=lambda _: self.page.go('/registro')),
                    ]
                )
            )
        )
        
    def IniciarIndex(self,resultado):
        self.route.menu.cont.visible = True
        self.route.page.appbar.visible = True
        
        self.page.go('/index')
        self.route.bar.set_Nickname(resultado)
        
        self.route.menu.update()
        self.route.page.update()
        
    def login(self,e):
        datos = [self.usuario.value,self.contrasenia.value]
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.verificarLogin(datos)
        mydb.close()
        
        if resultado is None:
            Notification(self.page,'Usuario o contraseña incorrectos!','red').mostrar_msg()
            return
        else:
            self.IniciarIndex(resultado)
    
    def build(self):
        return self.loginGUI

    def inicializar(self):
        self.usuario.value = None 
        self.contrasenia.value = None
        self.usuario.update()
        self.contrasenia.update()
        
        print('Inicializando Login')