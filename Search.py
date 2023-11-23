from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Database import FoodDatabase, generalDatabaseAccess
from Notification import Notification
from Cartas import CartaBuscador
from AlertDialog import RegisterDialog

class Search(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.focused_color = '#26587E'
        self.GRIS = '#4D4D4D'
        
        self.SearchButtom = ft.ElevatedButton(
            text='Buscar',
            icon=ft.icons.SEARCH,
            on_click=self.buscarElementos,
            style=ft.ButtonStyle(
                color="#26587E",
                bgcolor="#E3E9F0"
            )
        )
        
        self.SearchText = ft.TextField(
            label='Nombre de Alimento',
            autofocus=True,
            focused_color=self.focused_color,
            text_style=ft.TextStyle(color=self.GRIS),
            focused_border_color=self.GRIS,
            label_style=ft.TextStyle(color=self.GRIS),
            expand=True,
            color='black'
        )
        

        self.recomendaciones = ft.Text(
                           "Recomendaciones: ", 
                           ft.TextStyle(italic=True, color=ft.colors.WHITE))

        self.RecomendationField = ft.Card(
            content=ft.Container(
                self.recomendaciones,
                bgcolor ='#386641',
                expand=True,
                height = 40,
                padding  =5
            )
        )
        
        #self.SearchList = ft.ListView(expand=1,padding=20,auto_scroll=True,)

        self.SearchList = ft.ListView(expand=1,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)

        
        self.buscadorGUI = ft.Column(
            expand=True,
            controls=[
                self.RecomendationField,
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            self.SearchText,
                            self.SearchButtom
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    content=self.SearchList
                )
            ]
        )
        
    def establecer_Horario(self,string):
        self.horario = string
        print(self.horario)
        
    def buscarElementos(self,e):
        self.SearchList.clean()
        mydb = FoodDatabase(self.route)
        mydb.connect()
        
        if self.SearchText.value == '':
            return
            
        dato = self.SearchText.value
        resultado = mydb.ObtenerAlimentos(dato)
        mydb.close()
        
        for datos in resultado:
            item = CartaBuscador(self.route,datos)
            self.SearchList.controls.append(item)
        self.SearchList.update()

    def obtenerRecomendacion(self):
        lista_recomendaciones = [
        ["Verduras", 2100],
        ["Frutas", 1400],
        ["Cereales con Grasa", 300],
        ["Cereales sin Grasa", 1400],
        ["Origen Animal Muy Poca Grasa", 400],
        ["Origen Animal Poca Grasa", 300],
        ["Origen Animal Grasa Moderada", 200],
        ["Origen Animal Mucha Grasa", 100],
        ["Leche Descremada", 700],
        ["Leche Semidescremada", 500],
        ["Leche Entera", 200],
        ["Leche con Azúcar", 100],
        ["Grasas Sin Proteína", 700],
        ["Grasas Con Proteína", 500],
        ["Azucares Sin Grasa", 200],
        ["Azucares Con Grasa", 100],
        ["Libres de Energía", 1400],
        ["Bebidas Alcohólicas", 300],
        ]

        idusuario = self.route.getId()

        mydb = generalDatabaseAccess(self.route)
        mydb.connect()
        
        whereSentencia = "ID_Usuario = {} AND Registro_Alimentos.Fecha_Registro BETWEEN DATE_SUB(CURDATE(), INTERVAL 7 DAY) AND CURDATE()".format(idusuario)

        busqueda = mydb.recuperarRegistro("ID_Alimento, Cantidad_consumida", 
                                           "Registro_Alimentos", 
                                           whereSentencia)
        
        categorias = []
        if busqueda is not None:
            for fila in busqueda:
                idAlimento=fila[0]
                whereSentencia2 = "Alimentos.ID_Alimento = {}".format(idAlimento)
                categorias.append([mydb.recuperarRegistro("Categoria, ID_Usuario", 
                                                "Alimentos", 
                                                whereSentencia2),fila[1]])
        
        mydb.close()

        for cat in categorias:
            for recomendacion in lista_recomendaciones:
                if(cat == recomendacion[1]):
                    recomendacion[1] -= cat[1]

        resultados = sorted(lista_recomendaciones, key=lambda x: x[1], reverse=True)

        return resultados[0:5]
        
    def build(self):
        return self.buscadorGUI
    
    def inicializar(self):
        self.route.page.bgcolor = '#F2E8CF'
        self.SearchText.value = None
        self.SearchText.update()
        self.SearchList.clean()

        result = self.obtenerRecomendacion()
        stringRecom = "Recomendaciones: "

        for tipo in result:
            stringRecom += tipo[0] + ", "
            
        stringRecom = stringRecom.rstrip()[:-1]

        self.recomendaciones.value = stringRecom
        self.recomendaciones.update()

        print('Inicializando buscador', stringRecom)
