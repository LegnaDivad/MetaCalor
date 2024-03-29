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
        
        self.calRestantes = ft.Text(weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.calConsumidas = ft.Text(value='Calorías consumidas: 0',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.lipidos = ft.Text(value='Lipidos: 0%',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.proteinas = ft.Text(value='Proteinas: 0%',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        self.carbohidratos = ft.Text(value='Carbohidratos: 0%',weight=ft.FontWeight.BOLD,size=15,color=self.GRIS)
        
        self.fechaActual = datetime.datetime.today().strftime(f"%Y-%m-%d")
        self.hora = ft.TextField(
            label='Hora',
            expand=1,
            on_change=self.confirmarHora,
            input_filter=ft.InputFilter(
                regex_string=r"[0-9]", 
                replacement_string=""
            ),
        )
        
        self.minuto = ft.TextField(
            label='Minuto',
            expand=1,
            on_change=self.confirmarMinuto,
            input_filter=ft.InputFilter(
                regex_string=r"[0-9]", 
                replacement_string=""
            ),
        )
        
        self.dialogContent = ft.Container(
            content=ft.ResponsiveRow(
                controls=[
                    ft.Row(
                        controls=[
                            self.hora,
                            ft.Text(':'),
                            self.minuto,
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
                        content=ft.Column(
                            expand=True,alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(name=ft.icons.SUNNY,color='orange',size=40),
                                            ft.Text(color="white",value='Desayuno',weight='bold',size=25,bgcolor="self.GRIS")
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Row(
                                                spacing=10,
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',key='desayuno',on_click=self.tomarHorario,icon_size=30),
                                                    ft.Text('Registrar \nalimento',color='white'),
                                                ]
                                            ),
                                            ft.Icon(),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',key='desayuno',on_click=self.tomarHorarioPlatillo,icon_size=30),
                                                    ft.Text('Registrar \nPlatillo',color='white'),
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
                        content=ft.Column(
                            expand=True,alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(name=ft.icons.CLOUD,color='blue',size=30),
                                            ft.Text(color="white",value='Almuerzo',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Row(
                                                alignment=ft.MainAxisAlignment.CENTER,
                                                spacing=10,
                                                controls=[
                                                     ft.Icon(),
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',key='almuerzo',on_click=self.tomarHorario, icon_size=30),
                                                    ft.Text('Registrar \nalimento',color='white'),
                                                    ft.Icon()
                                                ]
                                            ),
                                            ft.Row(
                                                controls=[

                                                    ft.Icon(),
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',key='almuerzo',on_click=self.tomarHorarioPlatillo, icon_size=30),
                                                    ft.Text('Registrar \nPlatillo',color='white'),
                                                    ft.Icon()
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
                        content=ft.Column(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        spacing=10,
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(name=ft.icons.NIGHTLIGHT,color='purple',size=30),
                                            ft.Text(color="white",value='Cena',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        spacing=10,
                                        controls=[
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.ADD,icon_color='green',key='cena',on_click=self.tomarHorario,icon_size=30),
                                                    ft.Text('Registrar \nalimento',color='white'),
                                                ]
                                            ),
                                            ft.Icon(),
                                            ft.Row(
                                                controls=[
                                                    ft.IconButton(icon=ft.icons.DINNER_DINING,icon_color='green',key='cena',on_click=self.tomarHorarioPlatillo,icon_size=30),
                                                    ft.Text('Registrar \nPlatillo',color='white'),
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
                            spacing=100,
                            #expand=True,
                            #alignment=ft.MainAxisAlignment.START,
                            controls=[
                                ft.Column(
                                    spacing=10,

                                    # expand=1,
                                    #alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.calRestantes,
                                        self.calConsumidas,
                                        
                                    ]
                                ),
                                ft.Column(
                                    spacing=10,
                                    # expand=1,
                              
                                    controls=[
                                        self.lipidos,
                                        self.proteinas,
                                        self.carbohidratos
                                        ]
                                    ),
                                ft.Column(
                                   
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.ElevatedButton(text='           Añadir Recordatorio              ',icon=ft.icons.ACCESS_ALARM,style=ft.ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=self.boton_agregar),
                                        # ft.Row([
                                        #     ft.ElevatedButton(text='    Retrasar dia    ',style=ft.ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=self.modDia2),
                                        #     ft.ElevatedButton(text='    Adelantar    ',style=ft.ButtonStyle(color="#26587E",bgcolor="#E3E9F0"),on_click=self.modDia)])
                                        ]
                                    ),
                            ]
                        )
                    ),
                    ft.Row(
                        expand=6,
                        controls=[
                            self.desayuno,
                            self.almuerzo,
                            self.cena
                        ]
                    )
                ]
            )
        )
        
    def confirmarHora(self, e):
        try:
            hora_int = int(self.hora.value)
            if hora_int > 24:
                self.hora.value = None
            else:
                self.hora.value = str(hora_int)
        except (TypeError, ValueError):
            self.hora.value = None 

        self.hora.update()

    def confirmarMinuto(self, e):
        try:
            minuto_int = int(self.minuto.value)
            if minuto_int > 59:
                self.minuto.value = None
            else:
                self.minuto.value = str(minuto_int)
        except (TypeError, ValueError):
            self.minuto.value = None 

        self.minuto.update()

    
    def modDia(self,e):
        # Convertir la cadena a un objeto datetime
        fecha_actual_dt = datetime.datetime.strptime(self.fechaActual, f"%Y-%m-%d")

        # Sumar un día a la fecha actual
        fecha_siguiente = fecha_actual_dt + datetime.timedelta(days=1)

        # Convertir la fecha resultante de nuevo a una cadena si es necesario
        self.fechaActual = fecha_siguiente.strftime(f"%Y-%m-%d")
        print(self.fechaActual)
        self.inicializar()
        
    def modDia2(self,e):
        # Convertir la cadena a un objeto datetime
        fecha_actual_dt = datetime.datetime.strptime(self.fechaActual, f"%Y-%m-%d")

        # Sumar un día a la fecha actual
        fecha_siguiente = fecha_actual_dt - datetime.timedelta(days=1)

        # Convertir la fecha resultante de nuevo a una cadena si es necesario
        self.fechaActual = fecha_siguiente.strftime(f"%Y-%m-%d")
        print(self.fechaActual)
        self.inicializar()
        
    def tomarHorarioPlatillo(self,e):
        self.route.crearPlatillo.establecer_Horario(e.control.key)
        self.page.go('/crear_platillo')
        
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
        tmb = mydb.obtenerTMB(self.route.getId())
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
        if total > 0 and sumaKcal: #sumaKcal aquí no es necesario_?
            self.calConsumidas.value = f'Calorías consumidas: {round(sumaKcal,2)}'
            self.proteinas.value = f'Proteinas: {round((sumaProteinas / total) * 100, 2)}%'
            self.lipidos.value = f'Lipidos: {round((sumaLipidos / total) * 100, 2)}%'
            self.carbohidratos.value = f'Cabrohidratos:: {round((sumaCarbohidratos / total) * 100, 2)}%'
        #Esto no es necesario, solamente es para las pruebas
        else:
            self.calConsumidas.value = f'Calorías consumidas: 0'
            self.proteinas.value = f'Proteinas: 0%'
            self.lipidos.value = f'Lipidos: 0%'
            self.carbohidratos.value = f'Cabrohidratos: 0%'
        string = round(float(tmb[0]) - sumaKcal,2)
        self.calRestantes.value = f'Calorías restantes: {string}'
        if string < 0 :
            self.calRestantes.color = 'red'
        elif string > 0 :
            self.calRestantes.color = self.GRIS
        self.cont.update()
        
    def build(self):
        return self.cont
    
    def inicializar(self):
        self.route.page.bgcolor = '#F2E8CF'
        self.agregarComidas()
        print('Inicializando Index')
        if not self.route.bar.scheduler.running:
            self.route.bar.scheduler.start()