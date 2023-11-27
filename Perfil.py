from flet import *
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue



class Perfil(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route




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
                                                Text('  Datos de la cuenta                                                    ', color='#252422', size=30),
                                                ElevatedButton(text='Editar', style=ButtonStyle(color='#252422', shape=RoundedRectangleBorder(radius=10)), on_click=self.inicializar),
                                            ]
                                        ),
                                        Container(border_radius=border_radius.all(20), margin=15, expand=True, bgcolor='#252422', content=Row(
                                            expand=True,
                                            controls=[
                                                Column(
                                                    spacing=30,
                                                    expand=True,
                                                    controls=[
                                                        Container(content=Text('    Nombre: ', color='Black', size=25), margin=10, bgcolor='white', border_radius=border_radius.all(20)),
                                                        Row([Icon(),Icon(color="white",size=40,name=icons.FEATURED_VIDEO_ROUNDED), Text('Edad: ', color='white')]),
                                                        Row([Icon(),Icon(color="white",size=40,name=icons.PERSON), Text('Usuario: ', color='white')]),
                                                        Row([Icon(),Icon(color="white",size=40,name=icons.FOOD_BANK), Text('Alimentos Reg: ', color='white')]),
                                                        Row([Icon(),Icon(color="white",size=40,name=icons.SCALE), Text('Peso: ', color='white')]),
                                                        Row([Icon(),Icon(color="white",size=40,name=icons.LOCK), Text('Constrasena: ', color='white')]),
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

        print('Inicializando Perfil')