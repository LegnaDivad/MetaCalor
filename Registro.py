from typing import Any, List, Optional, Union
from flet import *
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase


class Register(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.nombre = TextField(label='Nombre',width=450)
        self.usuario = TextField(label='Usuario',width=450)
        self.contrasenia = TextField(label='Contraseña',width=450,password=True,can_reveal_password=True)
        self.contraseniaRep = TextField(label='Repetir Contraseña',width=450,password=True,can_reveal_password=True)
        self.botonRegistro = ElevatedButton(text='Registrarse',icon=icons.APP_REGISTRATION,style=ButtonStyle(bgcolor='white'),on_click=self.registrarUsuario)
        self.peso = TextField(label='Peso',width=450)    
        self.altura = TextField(label='Altura',width=450)
        self.edad = TextField(label='Edad',width=450)
        
        self.TMB = None    
        
        self.registroGUI = Container(
            expand=True,
            alignment=alignment.center,
            content=Container(
                height=900,width=700,
                border=border.all(1,'black'),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        Text('Registro de Usuario'),
                        self.nombre,
                        self.usuario,
                        self.contrasenia,
                        self.contraseniaRep,
                        self.altura,
                        self.peso,
                        self.edad,
                        self.botonRegistro,
                        TextButton(text='Iniciar Sesión',on_click=lambda _: self.page.go('/')),
                    ]
                )
            )
        )
        
    def calcularTMB(self):
        self.TMB = 88.362 + (13.397*float(self.peso.value)) + (4.799*float(self.altura.value)) - (5.677*float(self.edad.value))
        return self.TMB
        
    def registrarUsuario(self,e):
        mydb = UserDatabase(self.route)
        mydb.connect()
        datos = [self.nombre.value, self.usuario.value, self.contrasenia.value, self.calcularTMB()]
        resultado = mydb.registrarUsuario(datos)
        mydb.close()
        
        if resultado == 'introducido':
            print('insertado')
            self.route.page.go('/')
        else:
            print('error')
        
    def build(self):
        return self.registroGUI

    def inicializar(self):
        print('Inicializando Registro')