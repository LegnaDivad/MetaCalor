from typing import Any, List, Optional, Union
from flet import *
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase


class Perfil(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.nickname = Text(weight=FontWeight.BOLD,color='white',text_align=TextAlign.CENTER,expand=True, size=20)
        self.nombre = Text(weight=FontWeight.BOLD,color='white',text_align=TextAlign.CENTER,expand=True, size=20)
        self.edad = Text(weight=FontWeight.BOLD,color='red',text_align=TextAlign.CENTER,expand=True, size=25)
        self.contrasena = Text(weight=FontWeight.BOLD,color='red',text_align=TextAlign.CENTER,expand=True, size=25)
        self.peso = Text(weight=FontWeight.BOLD,color='red',text_align=TextAlign.CENTER,expand=True, size=25)
        self.id = Text(weight=FontWeight.BOLD,color='red',text_align=TextAlign.CENTER,expand=True, size=25)
        
        
       

        self.perfilcont = Container(
            expand=True,
            content=Row(
                expand=True,
                controls=[
                    Column(
                        alignment=alignment.center,
                        expand=True,
                        controls=[
                            Image(
                                src="/images/Logo4.PNG",
                                width=400,
                                height=145,
                                fit=ImageFit.CONTAIN,
                            ),
                            Container(
                                border_radius=border_radius.all(20),
                                expand=True,
                                bgcolor="white",
                                margin=10,
                                content=Column(
                                    #alignment=alignment.bottom_left,
                                    expand=True,
                                    controls=[
                                        Row(
                                            alignment=alignment.top_center,
                                            controls=[
                                                Text('  Datos de la cuenta                                           ', color='#252422', size=30),
                                                ElevatedButton(text='Editar', style=ButtonStyle(color='#252422', shape=RoundedRectangleBorder(radius=10)), on_click=self.inicializar),
                                            ]
                                        ),
                                        Container(border_radius=border_radius.all(20), margin=15, expand=True, bgcolor='#252422', content=Row(
                                            expand=True,
                                            controls=[
                                                Column(
                                                    spacing=100,
                                                    expand=True,
                                                    controls=[
                                                        Row(
                                                            
                                                            controls=[
                                                                Text('    Nombre: ', color='White', size=25),
                                                                self.nombre
                                                            ]
                                                        ),
                                                        Row(
                                                            spacing=250,
                                                            controls=[
                                                                 Column(
                                                                    spacing=100,
                                                            controls=[
                                                            
                                                            Row([Icon(),Icon(color="white",size=40,name=icons.PERSON), Text('Usuario: ', color='white')]),
                                                            Row([Icon(),Icon(color="white",size=40,name=icons.LOCK), Text('Constrasena: ', color='white')]),
                                                          
                                                            ],
                                                        ),
                                                        Column(
                                                            spacing=100,
                                                            controls=[
                                                            Row([Icon(),Icon(color="white",size=40,name=icons.SCALE), Text('Peso: ', color='white')]),
                                                            Row(
                                                                
                                                            [Icon(),Icon(color="white",size=40,name=icons.FEATURED_VIDEO_ROUNDED), Text('Edad: ', color='white')]
                                                            
                                                            ),
                                                           
                                                    ]),
                                                            ]
                                                        ),
                                                       
                                                          Row([Icon(),Icon(color="white",size=40,name=icons.FOOD_BANK), Text('Alimentos Reg: ', color='white')]),
                                                    ]
                                                ),
                                                
                                            ]
                                        )),

                                        
                                    ]
                                ),
                            ),
                        ]
                    ),
                    Column(
                        alignment=alignment.center_right,
                        expand=True,
                        controls=[
                            Column(
                                expand=True,
                                controls=[
                                    Container(
                                        margin=10,
                                        expand=True,
                                        border_radius=border_radius.all(20),
                                        alignment=alignment.top_right,
                                        bgcolor='white',
                                        content=
                                            Container(
                                                alignment=alignment.center,
                                                margin=10,
                                                expand=True,
                                                border_radius=border_radius.all(20),
                                                bgcolor="#E3E9F0",
                                                content=
                                                Column(
                                                    alignment=alignment.center,
                                                    controls=
                                                    [
                                                        Container(
                                                            margin=15,
                                                            expand=True,
                                                            bgcolor='white',
                                                            content=
                                                            Image(
                                                            src="/images/Logo3.PNG",
                                                            width=300,
                                                            height=300,
                                                            fit=ImageFit.CONTAIN
                                                            ),
                                                        ),
                                                        
                                                        Text("                 ID: 123456789", color='#4D4D4D', size=20)
                                                    ]
                                                )
                                        )
                                    ),
                                    Container(
                                        margin=10,
                                        expand=True,
                                        border_radius=border_radius.all(20),
                                        alignment=alignment.center,
                                        bgcolor='white',
                                        content=
                                        Column(
                                            alignment=alignment.center_right,
                                            controls=
                                            [
                                                Text('                                Metas  ', color='#4D4D4D', size=40),
                                                Container(
                                                    margin=15,
                                                    #expand=True,
                                                    
                                                    bgcolor='#4D4D4D',
                                                    border_radius=border_radius.all(20),
                                                    height=250,
                                                    width=900,
                                                    content=
                                                    Image(
                                                    src="/images/Logo3.PNG",
                                                    width=300,
                                                    height=300,
                                                    fit=ImageFit.CONTAIN
                                                    )
                                                ),
                                        
                                                Row(alignment=alignment.center, controls=[
                                                    Text('                                                                 '),
                                                    ElevatedButton(width=300,text='Editar', style=ButtonStyle(color='#4D4D4D', shape=RoundedRectangleBorder(radius=10)), on_click=self.inicializar),

                                                    ]
                                                    )
                                                
                                            ]
                                        )
                                        
                                    ),
                                ]
                            )
                        ]
                    )   
                ]
            ),
        )
        
    def build(self):
        return self.perfilcont
        
    def inicializar(self):
        
        print('Inicializando Perfil')

    def set_Nickname(self, texto):
        self.nickname.value = texto
        self.route.page.update()


    

    def set_info(self,id):
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.get_info(id)
        mydb.close()
        
        self.set_Nombre(resultado[0])
        self.set_Edad(resultado[1])
        self.set_Contrasena(resultado[2])
        self.set_Peso(resultado[3])
        self.set_ID(resultado[4])
        # self.set_Alimentos(resultado[5])
        # self.set_Metas(resultado[6])

    def set_Nombre(self, texto):
        self.nombre.value = texto
        self.route.page.update()
    
    def set_Edad(self, texto):
        self.edad.value = texto
        self.route.page.update()
    
    def set_Contrasena(self, texto):
        self.contrasena.value = texto
        self.route.page.update()

    def set_Peso(self, texto):
        self.peso.value = texto
        self.route.page.update()

    def set_ID(self, texto):
        self.id.value = texto
        self.route.page.update()

    # def set_Alimentos(self, texto):
    #     self.alimentos.value = texto
    #     self.route.page.update()
    
    # def set_Metas(self, texto):
    #     self.metas.value = texto
    #     self.route.page.update()

   