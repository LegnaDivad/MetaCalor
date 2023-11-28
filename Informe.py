from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from datetime import timedelta
import datetime
from Database import UserDatabase
from Cartas import CartaInforme
from PDFs import *

class Informe(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.colorBoton = '#eff1ed'
        
        self.fechaActual = datetime.datetime.now()
        self.aux = datetime.datetime.now()
        self.fechaF = datetime.datetime.now().date()
        self.fechas = []

        self.kcalTotales = ft.Text(color='black')
        self.informeBoton = ft.ElevatedButton(text='Descargar Informe en PDF',on_click=self.elaborarPDF,style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)))
        self.semanaAnteriorBoton = ft.TextButton(text='Semana Anterior',style=ft.ButtonStyle(color='Black',shape=ft.RoundedRectangleBorder(radius=10)),on_click=self.retrocederSemana)
        self.semanaActualBoton = ft.TextButton(disabled=True,text='Semana Actual',style=ft.ButtonStyle(color='green',shape=ft.RoundedRectangleBorder(radius=10)),on_click=self.adelantarSemana)
        
        self.lipidos = None
        self.proteinas = None
        self.carbohidratos = None
        
        self.normal_radius = 100
        self.hover_radius = 110
        self.normal_badge_size = 40
        self.hover_badge_size = 50

        self.sumaCalQuemadas = 0
        self.horasDeEjercicio = 0
        self.listCalQuemadasDiarias = []
        self.listCalConsumidasDiarias = []

        self.normal_title_style = ft.TextStyle(
            size=12, color=ft.colors.WHITE, weight=ft.FontWeight.BOLD
        )

        self.listView = self.SearchList = ft.ListView(expand=1,padding=5,auto_scroll=ft.ScrollMode.ALWAYS)
        
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
            expand=True,bgcolor='#023020', padding =20, border_radius=13,
            content= ft.Column(
                controls=[ft.Text("Informe de Quema de Calorias Semanal:"),self.listView]
            )
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
        self.fechaF = fecha_domingo.date()
        self.listView.controls.clear()
        self.obtenerInfo()
        
    def adelantarSemana(self,e):
        self.semanaAnteriorBoton.style = ft.ButtonStyle(color='black')
        self.semanaActualBoton.style = ft.ButtonStyle(color='green')
        self.semanaAnteriorBoton.disabled = False
        self.semanaActualBoton.disabled = True
        
        self.fechaActual = self.aux
        self.listView.controls.clear()
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

        self.listCalConsumidasDiarias.clear()
        self.listCalQuemadasDiarias.clear()
        
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerRegistrosSemana(self.route.getId(),self.fechaActual)
        peso = mydb.getPeso(self.route.getId())
        TMB = mydb.obtenerTMB(self.route.getId())
        resultadoQuemaDeCal = mydb.obtenerRegistrosSemanaEjercicios(self.route.getId(),self.fechaActual)
        resultadoConsumoCal = mydb.obtenerConsumoSemana(self.route.getId(),self.fechaActual)

        mydb.close()
        for dato in resultado:
            sumaKcal += dato[0]
            sumaLipidos += dato[1]
            sumaProteinas += dato[2]
            sumaCarbohidratos += dato[3]
            
        total = sumaLipidos + sumaProteinas + sumaCarbohidratos

        
        fechas = [self.fechaF - timedelta(days=d) for d in range(6, -1, -1)]
        
        i = 0
        limite = len(resultadoQuemaDeCal)
        print(limite)
        for dia in fechas:
            calDia = 0
            for data in resultado:
                if i > limite-1:
                    break
                if  resultadoConsumoCal[i][1] != dia: 
                    break

                duracionHoras = resultadoQuemaDeCal[i][1].total_seconds() / 3600.0
                cal = duracionHoras * resultadoQuemaDeCal[i][2] * peso[0]
                #print(duracionHoras,resultadoQuemaDeCal[i][2], peso[0], cal)
                calDia += cal
                i+=1
            calDia += TMB[0]
            self.listCalQuemadasDiarias.append(calDia)
            self.sumaCalQuemadas += calDia
            
        print("Calorias Quemadas Sumatoria: ", self.listCalQuemadasDiarias, resultadoQuemaDeCal)
        i = 0
        limite = len(resultadoConsumoCal)
        print(limite)
        for dia in fechas:
            calDia = 0
            for data in resultadoConsumoCal:
                print(i > limite-1)
                if i > limite-1:
                    break
                if  resultadoConsumoCal[i][1] != dia: 
                    break
                
                print(dia, resultadoConsumoCal[i][1])
                calDia += resultadoConsumoCal[i][0]
                i+=1
                print(i,limite)
            self.listCalConsumidasDiarias.append(calDia)
            
        print("Calorias Consumidas Sumatoria: ", self.listCalConsumidasDiarias, resultadoConsumoCal)

        self.fechas=fechas

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

        i=0
        while i < 7:
            item = CartaInforme(self.route,self.listCalConsumidasDiarias[i],self.listCalQuemadasDiarias[i], fechas[i])
            self.listView.controls.append(item)
            print(i)
            i+=1
        
        self.sumaCalQuemadas = 0

        self.cont.update()

    def elaborarPDF(self,e):

        mydb = UserDatabase(self.route)
        mydb.connect()

        pesoUsuario=mydb.getPeso(self.route.getId())
        alturaUsuario=mydb.getAltura(self.route.getId())
        nombreUsuario=mydb.getNombre(self.route.getId())
        
        nutrientes=[self.lipidos,self.proteinas,self.carbohidratos]

        generar_pdf(nombreUsuario[0],pesoUsuario[0],alturaUsuario[0],nutrientes,self.kcalTotales.value,self.listCalQuemadasDiarias,self.listCalConsumidasDiarias,self.fechas)

        mydb.close()
        #print(nombreUsuario,pesoUsuario,alturaUsuario,nutrientes,self.kcalTotales,self.listCalQuemadasDiarias,self.listCalConsumidasDiarias,self.fechas)
    
    def build(self):
        return self.cont
    
    def inicializar(self):
        # self.kcalTotales.value = 0
        self.obtenerInfo()
        print('Inicializando Informe')
