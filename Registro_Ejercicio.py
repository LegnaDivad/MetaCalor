import flet as ft
from Cartas import CartaRegistroEjercicios
from Database import generalDatabaseAccess
from Notification import Notification
from datetime import datetime

class RegistroEjercicios(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        self.lvEjercicios = ft.ListView(expand=True,padding=20,auto_scroll=True)
        self.tmba = 0
        self.tmbaText =ft.Text(value="{}".format(self.tmba),weight='bold',size=25,bgcolor=self.GRIS,color=ft.colors.DEEP_ORANGE_500)

        self.tmbCard = ft.Card(
            key='tmba',
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.LOCAL_FIRE_DEPARTMENT_SHARP,color=ft.colors.DEEP_ORANGE_500,size=25),
                                            ft.Text(value='Tasa Metabolica Basal Actual:',weight='bold',size=25,bgcolor=self.GRIS),
                                            self.tmbaText
                                        ]
                                    )
                                )
                            ]
                        )
                    )
                ]
            ),
            color='#7CFC00', height= 100
        )
        
        self.botonRegistroEjercicio = ft.ElevatedButton(text='Registrar Ejercicio',
                                                     icon=ft.icons.ADD,style=ft.ButtonStyle(color ='white', bgcolor="#009E60"),
                                                     on_click=self.buscadorEjercicios)

        self.registroEjercicios = ft.Card(
            expand=True,key='registroEjercicios',
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.DIRECTIONS_RUN,color='red',size=25),
                                            ft.Text(value='Actividades del Dia',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            self.botonRegistroEjercicio
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    self.lvEjercicios
                ]
            ),
            color='#355E3B',
        )

        
        self.cont = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    self.tmbCard,
                    self.registroEjercicios,
                ]
            )
        )
        
    def buscadorEjercicios(self,e):
        self.route.buscador.establecer_Horario('cena')
        self.page.go('/buscador_ejercicios')

    def updateTMBA(self):
        mydb = generalDatabaseAccess(self.route)
        mydb.connect()
        self.tmba = mydb.recuperarRegistro("TMB",
                                              "Usuario",
                                              "ID_Usuario  = {}".format(self.route.getId()),
                                              1)[0][0]
        mydb.close()
        print("TMB:",self.tmba)
        self.tmbaText.value = self.tmba
        self.tmbCard.update()
        
    def agregarEjercicios(self):
        self.lvEjercicios.clean()

        idUsuario = self.route.getId()
        mydb = generalDatabaseAccess(self.route)
        mydb.connect()
        
        pesoUsuario = mydb.recuperarRegistro("Peso",
                                              "Usuario",
                                              "ID_Usuario  = {}".format(idUsuario) #
                                              )
        
        actFisicaUsuario = mydb.recuperarRegistro("A.Tipo_Act, R.Duración_Act, ID_RegDeAct, A.MET",
                                              "Registro_Actividad_Física AS R, Actividad_Física AS A",
                                              "R.ID_Usuario  = {} AND R.ID_AF = A.ID_AF AND R.Fecha_Registro = '{}'".format(idUsuario,self.route.getFecha()) #
                                              )
        mydb.close()

        if actFisicaUsuario is not None:
            for data in actFisicaUsuario:
                duracionHoras = data[1].total_seconds() / 3600.0
                cal = pesoUsuario[0][0] * duracionHoras * data[3]
                item = CartaRegistroEjercicios(self.route,data,cal)
                self.lvEjercicios.controls.append(item)
        else:
            Notification(self.page,'Busqueda sin Resultados','red').mostrar_msg()

        self.cont.update()
        
    def build(self):
        return self.cont
    
    def inicializar(self):
        self.route.page.bgcolor = '#98FB98'
        self.updateTMBA()
        self.agregarEjercicios()
        print('Inicializando Registro Ejercicios')
