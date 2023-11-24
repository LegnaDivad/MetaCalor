from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Cartas import CartaRegistroAlimento
from Database import UserDatabase
from AlertDialog import RegisterDialog
import datetime

class Index(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        self.lvDesayuno = ft.ListView(expand=True,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        self.lvAlmuerzo = ft.ListView(expand=True,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        self.lvCena = ft.ListView(expand=True,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        
        self.calRestantes = ft.Text('Calorías restantes: 1000',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.calConsumidas = ft.Text(value='Calorías consumidas: 0',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.lipidos = ft.Text(value='Lipidos: 0%',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.proteinas = ft.Text(value='Proteinas: 0%',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.carbohidratos = ft.Text(value='Carbohidratos: 0%',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        
        self.fechaActual = datetime.datetime.today().strftime(f"%Y-%m-%d")
        
        self.dialogContent = ft.Container(

            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.TextField(label='Hora',expand=1),
                            ft.TextField(label='Minuto',expand=1),
                        ]
                    ),
                    ft.TextField(label='Mensaje'),
                ]
            ),
        )
        
        
        self.desayuno = ft.Card(
            expand=True,
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
                                            ft.Icon(name=ft.icons.SUNNY,color='orange',size=25),
                                            ft.Text(value='Desayuno',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',key='desayuno',on_click=self.tomarHorario),
                                                    ft.Text('Registrar alimento',color='white')
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',on_click=lambda _: self.page.go('/buscador')),
                                                    ft.Text('Registrar Platillo',color='white')
                                                ]
                                            ),
                                            
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    ft.Container(
                        expand=True,
                        content=self.lvDesayuno
                    )
                ]
            ),
            color='#A7C957',
        )
        
        self.almuerzo = ft.Card(
            expand=True,
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
                                            ft.Icon(name=ft.icons.CLOUD,color='blue',size=25),
                                            ft.Text(value='Almuerzo',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',key='almuerzo',on_click=self.tomarHorario),
                                                    ft.Text('Registrar alimento',color='white')
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',on_click=lambda _: self.page.go('/buscador')),
                                                    ft.Text('Registrar Platillo',color='white')
                                                ]
                                            ),
                                            
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    self.lvAlmuerzo
                ]
            ),
            color='#6A994E',
        )
        
        self.cena = ft.Card(
            expand=True,
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
                                            ft.Icon(name=ft.icons.NIGHTLIGHT,color='purple',size=25),
                                            ft.Text(value='Cena',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',key='cena',on_click=self.tomarHorario),
                                                    ft.Text('Registrar alimento',color='white')
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',on_click=lambda _: self.page.go('/buscador')),
                                                    ft.Text('Registrar Platillo',color='white')
                                                ]
                                            ),
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    self.lvCena
                ]
            ),
            color='#386641',
        )
        
        self.cont = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=1,
                        padding=10,
                        # border=ft.border.all(width=5,color=ft.colors.BLUE),
                        border_radius=ft.border_radius.all(11),
                        # bgcolor=ft.colors.ORANGE,
                        content=ft.Row(
                            expand=True,
                            alignment=ft.MainAxisAlignment.END,
                            spacing=130,
                            controls=[
                                ft.Column(
                                    # expand=1,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.calRestantes,
                                        self.calConsumidas,
                                    ]
                                ),
                                ft.Column(
                                    # expand=1,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.lipidos,
                                        self.proteinas,
                                        self.carbohidratos
                                    ]
                                ),
                                ft.Column(
                                    # expand=1,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(text='Añadir Recordatorio',icon=ft.icons.ACCESS_ALARM,style=ft.ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=self.boton_agregar),
                                        ft.ElevatedButton(text='Modificar Dia',style=ft.ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=self.modDia)
                                    ]
                                ),
                            ]
                        )
                    ),
                    ft.Row(
                        expand=8,
                        controls=[
                            self.desayuno,
                            self.almuerzo,
                            self.cena
                        ]
                    )
                ]
            )
        )
        
    def modDia(self,e):
        # Convertir la cadena a un objeto datetime
        fecha_actual_dt = datetime.datetime.strptime(self.fechaActual, f"%Y-%m-%d")

        # Sumar un día a la fecha actual
        fecha_siguiente = fecha_actual_dt + datetime.timedelta(days=1)

        # Convertir la fecha resultante de nuevo a una cadena si es necesario
        self.fechaActual = fecha_siguiente.strftime(f"%Y-%m-%d")
        print(self.fechaActual)
        self.inicializar()
        
    def tomarHorario(self,e):
        self.route.buscador.establecer_Horario(e.control.key)
        self.page.go('/buscador')
        
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarRecordatorio,self.dialogContent, "Ingrese los siguientes datos:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
        
    def registrarRecordatorio(self):
        print('Hola :D')
        
    def agregarComidas(self):
        sumaKcal = 0
        sumaProteinas = 0
        sumaLipidos = 0
        sumaCarbohidratos = 0
        total = 0
        self.lvDesayuno.clean()
        self.lvAlmuerzo.clean()
        self.lvCena.clean()
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.ObtenerRegistros(self.route.getId())
        mydb.close()
        
        for data in resultado:
            fecha_comparar = data[6].strftime(f"%Y-%m-%d")
            if self.fechaActual == fecha_comparar:
                if data[2].lower() == 'desayuno':
                    item = CartaRegistroAlimento(self.route,data)
                    self.lvDesayuno.controls.append(item)
                elif data[2].lower() == 'almuerzo':
                    item = CartaRegistroAlimento(self.route,data)
                    self.lvAlmuerzo.controls.append(item)
                elif data[2].lower() == 'cena':
                    item = CartaRegistroAlimento(self.route,data)
                    self.lvCena.controls.append(item)
                sumaKcal += data[1]
                sumaProteinas += data[3]
                sumaLipidos += data[4]
                sumaCarbohidratos += data[5]
        total = sumaProteinas + sumaLipidos + sumaCarbohidratos
        if total > 0:
            self.calConsumidas.value = f'Calorías consumidas: {sumaKcal}'
            self.proteinas.value = f'Proteinas: {round((sumaProteinas / total) * 100, 2)}%'
            self.lipidos.value = f'Lipidos: {round((sumaLipidos / total) * 100, 2)}%'
            self.carbohidratos.value = f'Cabrohidratos:: {round((sumaCarbohidratos / total) * 100, 2)}%'
        self.cont.update()
        
    def build(self):
        return self.cont
    
    def inicializar(self):
        self.route.page.bgcolor = '#F2E8CF'
        self.agregarComidas()
        print('Inicializando Index')
        if not self.route.bar.scheduler.running:
            self.route.bar.scheduler.start()