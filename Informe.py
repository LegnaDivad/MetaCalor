from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
import datetime
from Database import UserDatabase

class Informe(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.colorBoton = '#eff1ed'
        
        self.fechaActual = datetime.datetime.now()
        self.aux = datetime.datetime.now()
        
        self.kcalTotales = ft.Text(color='black')
        self.informeBoton = ft.ElevatedButton(text='Descargar Informe',style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        self.semanaAnteriorBoton = ft.TextButton(text='Semana Anterior',style=ft.ButtonStyle(color='Black',shape=ft.RoundedRectangleBorder(radius=10)),on_click=self.retrocederSemana)
        self.semanaActualBoton = ft.TextButton(disabled=True,text='Semana Actual',style=ft.ButtonStyle(color='green',shape=ft.RoundedRectangleBorder(radius=10)),on_click=self.adelantarSemana)
        
        self.lipidos = None
        self.proteinas = None
        self.carbohidratos = None
        
        self.normal_radius = 100
        self.hover_radius = 110
        self.normal_badge_size = 40
        self.hover_badge_size = 50
        
        self.normal_title_style = ft.TextStyle(
            size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )
        
        self.hover_title_style = ft.TextStyle(
            size=16,
            color=ft.colors.WHITE,
            weight=ft.FontWeight.BOLD,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK54),
        )

        self.chart = ft.PieChart(
            sections_space=0,
            center_space_radius=0,
            on_chart_event=self.on_chart_event,
            expand=True,
        )
        
        self.informeAlimentos = ft.Container(
            expand=True,
            bgcolor='#bcbd8b',
            margin=70,
            padding=30,
            alignment=ft.alignment.center,
            content=ft.Row(
                expand=True,
                controls=[
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Text(value='Informe Semanal de Alimentos',color='black'), 
                            self.kcalTotales,
                        ]
                    ),
                    ft.Container(
                        expand=True,
                        content=self.chart
                    ),
                    ft.Column(
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                        controls=[
                            self.informeBoton,
                        ]
                    ),
                ]
            )
        )
        
        self.informeEjercicios = ft.Container(
            expand=True,
            bgcolor='#bcbd8b',
            margin=70
        )
        
        self.cont = ft.Container(
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Row(
                        controls=[
                            self.semanaAnteriorBoton,
                            self.semanaActualBoton
                        ]
                    ),
                    self.informeAlimentos,
                    self.informeEjercicios
                ]
            )
        )
        
    def retrocederSemana(self, e):
        self.semanaAnteriorBoton.style = ft.ButtonStyle(color='green')
        self.semanaActualBoton.style = ft.ButtonStyle(color='black')
        self.semanaAnteriorBoton.disabled = True
        self.semanaActualBoton.disabled = False
        
        if self.fechaActual.weekday() == 6:  # Si hoy es domingo
            fecha_domingo = self.fechaActual - datetime.timedelta(days=7)
        else:
            dias_para_restar = (self.fechaActual.weekday() + 1) % 7  # Ajuste para obtener el domingo
            fecha_domingo = self.fechaActual - datetime.timedelta(days=dias_para_restar)
        
        self.fechaActual = fecha_domingo
        self.obtenerInfo()
        
    def adelantarSemana(self,e):
        self.semanaAnteriorBoton.style = ft.ButtonStyle(color='black')
        self.semanaActualBoton.style = ft.ButtonStyle(color='green')
        self.semanaAnteriorBoton.disabled = False
        self.semanaActualBoton.disabled = True
        
        self.fechaActual = self.aux
        self.obtenerInfo()
        
    def badge(self,icon,size):
        return ft.Container(
            ft.Icon(icon),
            width=size,
            height=size,
            border=ft.border.all(1, ft.colors.BROWN),
            border_radius=size / 2,
            bgcolor=ft.colors.WHITE,
        )
        
    def on_chart_event(self,e: ft.PieChartEvent):
        for idx, section in enumerate(self.chart.sections):
            if idx == e.section_index:
                section.radius = self.hover_radius
                section.title_style = self.hover_title_style
            else:
                section.radius = self.normal_radius
                section.title_style = self.normal_title_style
        self.chart.update()
        
    def generarInforme(self,e):
        pass
    
    def obtenerInfo(self):
        # print(self.fechaActual)
        sumaKcal = 0
        sumaLipidos = 0
        sumaProteinas = 0
        sumaCarbohidratos = 0
        total = 0
        
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerRegistrosSemana(self.route.getId(),self.fechaActual)
        mydb.close()
        for dato in resultado:
            sumaKcal += dato[0]
            sumaLipidos += dato[1]
            sumaProteinas += dato[2]
            sumaCarbohidratos += dato[3]
            
        total = sumaLipidos + sumaProteinas + sumaCarbohidratos
        
        if total > 0:
            self.lipidos = round((sumaLipidos / total) * 100,2)
            self.proteinas = round((sumaProteinas / total) * 100,2)
            self.carbohidratos = round((sumaCarbohidratos / total) * 100,2)
            self.kcalTotales.value = f'Calorías consumidas en la semana: {sumaKcal}'
        else:
            self.lipidos = 0
            self.proteinas = 0
            self.carbohidratos = 0
            self.kcalTotales.value = 0
        
        self.chart.sections.clear()
        self.chart.sections.append(
            ft.PieChartSection(
                self.proteinas,
                title="Proteinas",
                title_style=self.normal_title_style,
                color=ft.colors.BLUE,
                radius=self.normal_radius,
                badge=self.badge(ft.icons.AC_UNIT, self.normal_badge_size),
                badge_position=0.98,
            ),
        )
        self.chart.sections.append(
            ft.PieChartSection(
                self.lipidos,
                title="Lipidos",
                title_style=self.normal_title_style,
                color=ft.colors.YELLOW,
                radius=self.normal_radius,
                badge=self.badge(ft.icons.AC_UNIT, self.normal_badge_size),
                badge_position=0.98,
            ),
        )
        self.chart.sections.append(
            ft.PieChartSection(
                self.carbohidratos,
                title="Carbohidratos",
                title_style=self.normal_title_style,
                color=ft.colors.RED,
                radius=self.normal_radius,
                badge=self.badge(ft.icons.AC_UNIT, self.normal_badge_size),
                badge_position=0.98,
            ),
        )
        
        self.cont.update()
        
    def build(self):
        return self.cont
    
    def inicializar(self):
        # self.kcalTotales.value = 0
        self.obtenerInfo()
        print('Inicializando Informe')