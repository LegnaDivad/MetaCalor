import flet as ft
from Cartas import CartaRegistroEjercicios,CartaBuscadorEjercicios
from Database import generalDatabaseAccess,EjerciciosDatabase
from Notification import Notification

class RegistroEjercicios(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        self.lvEjercicios = ft.ListView(expand=True,padding=20,auto_scroll=True)

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
                                            ft.Text(value='Tasa Metabolica Basal Actual',weight='bold',size=25,bgcolor=self.GRIS)
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
        self.page.go('/buscador_ejercicios')
        
    def agregarEjercicios(self):
        self.lvEjercicios.clean()

        mydb = EjerciciosDatabase(self.route)
        mydb.connect()
        resultado = mydb.ObtenerEjercicios(self.route.getId())
        
        for datos in resultado:
            fecha_comparar = datos[3].strftime(f"%Y-%m-%d")
            if self.route.index.fechaActual == fecha_comparar:
                # item = CartaBuscadorEjercicios(self.route,datos)
                item = CartaRegistroEjercicios(self.route,datos)
                self.lvEjercicios.controls.append(item)
        self.lvEjercicios.update()

        self.cont.update()
        
    def build(self):
        return self.cont
    
    def inicializar(self):
        # self.route.page.bgcolor = '#98FB98'
        self.agregarEjercicios()
        print('Inicializando Registro Ejercicios')