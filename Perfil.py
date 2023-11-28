from flet import *
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import UserDatabase


class Perfil(UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        self.nickname = Text(weight=FontWeight.BOLD,color='white',size=20)
        self.nombre = Text(weight=FontWeight.BOLD,color='white',size=20)
        self.edad = Text(weight=FontWeight.BOLD,color='white',size=20)
        self.contrasena = Text(weight=FontWeight.BOLD,color='white', size=20)
        self.peso = Text(weight=FontWeight.BOLD,color='white', size=20)
        self.id = Text(weight=FontWeight.BOLD,color='#4D4D4D',size=35)



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
                                                Text('  Datos de la cuenta', color='#4D4D4D',weight=FontWeight.BOLD,size=30),
                       
                                                ElevatedButton(text='Editar', style=ButtonStyle(color='#E3E9F0', shape=RoundedRectangleBorder(radius=10)), on_click=self.EditarDatos),
                                            ]
                                        ),
                                        Container(border_radius=border_radius.all(20), margin=15, expand=True, bgcolor='#252422', content=Row(
                                            expand=True,
                                            controls=[
                                                Column(
                                                    spacing=50,
                                                    expand=True,
                                                    controls=[
                                                        Row(
                                                            
                                                            controls=[
                                                                Icon(),
                                                                Text('Nombre: ', color='White', size=25,weight=FontWeight.BOLD),
                                                                self.nombre
                                                            ]
                                                        ),
                                                        Row(
                                                            spacing=20,
                                                            controls=[
                                                                 Column(
                                                                    spacing=40,
                                                                    controls=[
                                                                    Row(controls=[Icon(),Icon(color="white",size=50,name=icons.PERSON), Text('Usuario: ', color='white',weight=FontWeight.BOLD,size=20), self.nickname],),
                                                                    Row(controls=[Icon(),Icon(color="white",size=50,name=icons.LOCK), Text('Constrasena: ', color='white',weight=FontWeight.BOLD,size=20), self.contrasena]),
                                                                    Row(controls=[Icon(),Icon(color="white",size=50,name=icons.SCALE), Text('Peso: ', color='white',weight=FontWeight.BOLD,size=20), self.peso]),
                                                                    Row(controls=[Icon(),Icon(color="white",size=50,name=icons.FEATURED_VIDEO_ROUNDED), Text('Edad: ', weight=FontWeight.BOLD,color='white', size=20), self.edad]),
                                                          
                                                            ],
                                                        ),
                                                        
                                                            ]
                                                        ),
                                                       
                                                        
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
                                                Row(
                                                    controls=[
                                                Column(
                                                    alignment=alignment.center,
                                                    controls=
                                                    [
                                                        Container(
                                                            margin=25,
                                                            expand=True,
                                                            
                                                            content=
                                                            Image(
                                                            src="/images/gato.PNG",
                                                            width=300,
                                                            height=300,
                                                            fit=ImageFit.CONTAIN
                                                            ),
                                                        ),
                                                        
                                                        
                                                    ]
                                                ),Row(alignment=alignment.top_left,controls=[Text(f"ID: ", color='#4D4D4D',weight=FontWeight.BOLD, size=40,), self.id,])
                                ])
                                        )
                                    ),
                                    Container(
                                        margin=10,
                                        expand=True,

                                    )
                                   
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


    def EditarDatos(self,e):
        global Editing, USER_ID
        USER_ID = self.id.value
        print("PrevID: ",USER_ID)
        Editing = True
        self.page.go('/registro')
            

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

   