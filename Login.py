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
        
        self.GRIS = '#4D4D4D'
        self.focused_color = '#26587E'
        
        banner_in_ses = Text(
            value='     Inicio de Sesión    ',
            color='#26587E',
            size=30,
            #weight='bold',
            font_family="Arial Black",
            weight=FontWeight.BOLD,
        )

        self.usuario = TextField(label='Usuario',prefix_icon=icons.PERSON_2_OUTLINED,width=450,autofocus=True,focused_color=self.focused_color,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.contrasenia = TextField(label='Contraseña',prefix_icon=icons.LOCK_CLOCK_OUTLINED,width=450,password=True,can_reveal_password=True,focused_color=self.focused_color,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.botonLogin = ElevatedButton(
            text='Iniciar Sesión',
            style=ButtonStyle(
                color="#26587E",
                bgcolor="#E3E9F0"
            ),
            icon=icons.LOGIN, on_click=self.login)
        
        self.loginGUI = Container(
            expand=True,
            alignment=alignment.center,
            content=Container(
                height=500,width=700,
                border=border.all(3,'white'),
                border_radius=border_radius.all(11),
                bgcolor='white',
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=30,
                    controls=[
                        banner_in_ses,
                        self.usuario,
                        self.contrasenia,
                        self.botonLogin,
                        TextButton(
                            text='Registrate aquí',
                            style=ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),
                            on_click=lambda _: self.page.go('/registro')),
                    ]
                ),
                shadow=BoxShadow(
                    spread_radius=1,
                    blur_radius=15,
                    color=colors.BLUE_GREY_300,
                    offset=Offset(0, 0),
                    blur_style=ShadowBlurStyle.OUTER,
                )
            ),
        )
        
    def IniciarIndex(self,resultado):
        nombre = resultado[0]
        id = resultado[2]
        self.route.setLogInfo(resultado)
        self.route.menu.cont.visible = True
        self.route.page.appbar.visible = True
        self.route.bar.set_Nickname(nombre)
        self.route.perfil.set_Nickname(nombre)
        self.route.perfil.set_info(id)
        self.route.menu.update()
        self.route.page.update()
        
        self.page.go('/index')
        
    def login(self,e):
        datos = [self.usuario.value,self.contrasenia.value]
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.verificarLogin(datos)
        mydb.close()
        
        if resultado is None:
            print('Usuario no encontrado!')
            Notification(self.page,'Usuario o contraseña incorrectos!','red').mostrar_msg()
            return
        Notification(self.page,'Se ha iniciado sesión!','green').mostrar_msg()
        self.IniciarIndex(resultado)
    
    def build(self):
        return self.loginGUI

    def inicializar(self):
        self.usuario.value = None
        self.contrasenia.value = None
        self.loginGUI.update()
        print('Inicializando Login')