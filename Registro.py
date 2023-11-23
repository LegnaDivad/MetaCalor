from typing import Any, List, Optional, Union
from flet import *
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase
from AlertDialog import ConfirmDialog
from Notification import Notification


class Register(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#4D4D4D'
        self.focused_color = '#26587E'
        
        self.nombre = TextField(label='Nombre',width=450,autofocus=True,focused_color=self.focused_color,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.usuario = TextField(label='Usuario',width=450,focused_color=self.focused_color,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.contrasenia = TextField(label='Contraseña',width=450,focused_color=self.focused_color,password=True,can_reveal_password=True,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.contraseniaRep = TextField(label='Repetir Contraseña',focused_color=self.focused_color,width=450,password=True,can_reveal_password=True,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.botonRegistro = ElevatedButton(text='Registrarse',icon=icons.APP_REGISTRATION,style=ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=self.registrarUsuario)
        self.peso = TextField(label='Peso kg.',focused_color=self.focused_color,width=120,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))    
        self.altura = TextField(label='Altura cm.',focused_color=self.focused_color,width=120,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.edad = TextField(label='Edad',focused_color=self.focused_color,width=120,text_style=TextStyle(color=self.GRIS),focused_border_color=self.GRIS,label_style=TextStyle(color=self.GRIS))
        self.genero = PopupMenuButton(
                    content= Icon(name=icons.TRANSGENDER,color='black'),
                                items=[
                                PopupMenuItem(icon=icons.MALE,text="Hombre",on_click=self.Hombre),
                                PopupMenuItem(),  # divider
                                PopupMenuItem(icon=icons.FEMALE,text="Mujer",on_click=self.Mujer),        
                                ]
                        
        )

       

        self.TMB = None    
        
        row = Row(
            spacing=21
            ,controls=[self.peso,self.altura,self.edad,self.genero],
            alignment = MainAxisAlignment.CENTER
            )
        self.registroGUI = Container(
            expand=True,
            alignment=alignment.center,
            
            content=Container(
                bgcolor="white",
                height=Page.window_max_height,width=500,
                border=border.all(1,self.GRIS),
                border_radius=border_radius.all(11),
                content=Column(
                    alignment=MainAxisAlignment.CENTER,
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    spacing=15,
                    controls=[
                        Text('Registro de Usuario',font_family="Arial #4D4D4D",size=30,color='#26587E'),
                        self.nombre,
                        self.usuario,
                        self.contrasenia,
                        self.contraseniaRep,
                        row,
                        #self.genero,
                        self.botonRegistro,
                        TextButton(text='Iniciar Sesión',style=ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=lambda _: self.page.go('/')),
                    ]
                    
                )
            )
        )

    def Hombre(self,e):
            self.genero = 1
            return self.genero
    def Mujer(self,e):
            self.genero = 2
            return self.genero
        
    def calcularTMB(self):
        self.TMB = 88.362 + (13.397*float(self.peso.value)) + (4.799*float(self.altura.value)) - (5.677*float(self.edad.value))
        return self.TMB
        
    def registrarUsuario(self,e):
        
        # Si no introduce valores que no son enteros o flotantes, se genera un error.
        try:
            edad = int(self.edad.value)
            altura = float(self.altura.value)
            peso = float(self.peso.value)
            nombre = "".join(self.nombre.value.split(" "))
            genero = self.genero
        except ValueError:
            Notification(self.page, 'Has dejado valores vacios o son inválidos!', 'red').mostrar_msg()
            return

        calculoTMB = self.calcularTMB()
        if(nombre.isalpha() == False):
            Notification(self.page,'El nombre no puede contener números!','red').mostrar_msg()
            return
        elif(self.usuario.value.isalnum() == False):
            Notification(self.page,'El usuario no puede contener caracteres especiales!','red').mostrar_msg()
            return
        elif(altura < 0 or peso < 0 or edad < 0):
            Notification(self.page,'No puede haber valores negativos!','red').mostrar_msg()
            return
        elif(self.altura.value == '' or self.peso.value == '' or self.edad.value == ''):
            Notification(self.page,'No puede haber valores vacios!','red').mostrar_msg()
            return
        elif(edad < 15):
            Notification(self.page,f'Estas seguro de que esta es tu edad? -> {edad}\nPara utilizar el programa debes ser mayor de 15 años','yellow').mostrar_msg()
            return
        elif(edad > 122):
            Notification(self.page,f'Estas seguro de que esta es tu edad? -> {edad}\nSi es así llama a los record Guinness para declarar un nuevo record antes de usar nuestro programa!!!','yellow').mostrar_msg()
            return
        elif(peso > 595):
            Notification(self.page,f'Estas seguro de que este es tu peso??!! -> {edad}\nSi es así llama a los record Guinness para declarar un nuevo record antes de usar nuestro programa!!!\nSi es que estas vivo para ese momento...','yellow').mostrar_msg()
            return
        elif(genero == None):
            Notification(self.page,'No has seleccionado un genero!','red').mostrar_msg()
            return
        else:
            datos = [self.nombre.value, self.usuario.value, self.contrasenia.value, calculoTMB]
        
        if self.contrasenia.value != self.contraseniaRep.value:
            Notification(self.page,'Las contraseñas no coinciden!','red').mostrar_msg()
            return
        
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.registrarUsuario(datos)
        mydb.close()
        
        if resultado is None:
            Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
            return
        Notification(self.page,'Se ha registrado correctamente!','green').mostrar_msg()
        print(genero)
        self.route.page.go('/')
            
    def build(self):
        return self.registroGUI

    def inicializar(self):
        self.nombre.value = None
        self.usuario.value = None
        self.contrasenia.value = None
        self.contraseniaRep.value = None
        self.peso.value = None
        self.altura.value = None
        self.edad.value = None
        self.genero = None
        self.registroGUI.update()
        print('Inicializando Registro')