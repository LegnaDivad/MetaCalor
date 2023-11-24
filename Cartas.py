from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Notification import Notification
from AlertDialog import *
from Database import FoodDatabase, UserDatabase
import datetime
import decimal


class CartaRegistroAlimento(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.datos = datos
        
        self.GRIS = '#252422'
        
        self.botonModificar = ft.IconButton(icon=ft.icons.EDIT,icon_color='blue')
        self.botonEliminar = ft.IconButton(icon=ft.icons.DELETE_OUTLINE,icon_color='red',on_click=self.eliminarAlimento)
        
        self.nombre = ft.Text(value=f"Nombre: {datos[0]}")
        self.calorias = ft.Text(value=f"Calorías: {datos[1]}")
        
        self.carta = ft.Card(

            content=ft.Container(
                padding=10,height=100,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Row(
                                expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self.nombre,
                                            self.calorias
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            self.botonModificar,
                                            self.botonEliminar
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ),
            color=self.GRIS
        )
        
    def eliminarAlimento(self,e):
        mydb = UserDatabase(self.route)
        mydb.connect()
        # resultado = mydb.ObtenerRegistros(self.datos[7])
        mydb.eliminarRegistroAlimento(self.datos[7])
        mydb.close()
        self.route.index.agregarComidas()
        self.route.page.update()
        
    def build(self):
        return self.carta

class CartaBuscador(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.dato = datos
        
        self.nombre = ft.Text(value=f'Alimento: {datos[0]} | Categoria: {datos[1]}',text_align='center',color='white')
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)
        
        self.peso = ft.Text(color='white',value=0)
        self.kcal = ft.Text(color='white',value=0)
        self.proteina = ft.Text(color='white',value=0)
        self.lipidos = ft.Text(color='white',value=0)
        self.hidratos = ft.Text(color='white',value=0)
        self.unidad = ft.Text(value=f'Unidad: {datos[2]}',color='white')
        
        self.cantidadDato = ft.TextField(value=0,label='Cantidad',on_submit=self.calcular_nutrientes)
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.nombre,
                    self.cantidadDato,
                    self.unidad,
                    ft.Row([
                        ft.Text('Kcal: '),self.kcal,
                    ]),
                    ft.Row([
                        ft.Text('Proteina: '),self.proteina,
                    ]),
                    ft.Row([
                        ft.Text('Lipidos: '),self.lipidos,
                    ]),
                    ft.Row([
                        ft.Text('Hidratos: '),self.hidratos,
                    ]),
                ]
            )
        )
        
        self.GRIS = '#252422'
        
        self.carta = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Row(
                                expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            self.nombre
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            self.BotonAgregar
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ),
            color=self.GRIS
        )
        
    def calcular_nutrientes(self,e):
        
        try:
            decimal.Decimal(self.cantidadDato.value)
        except (decimal.InvalidOperation, ValueError):
            print("El valor ingresado no es convertible a decimal.Decimal.")
            self.cantidadDato.value = 0 
            self.cantidadDato.update()
            
        valor_cantidad = decimal.Decimal(self.cantidadDato.value)
        if valor_cantidad < 0:
            print('No')
            self.cantidadDato.value = 0
            self.cantidadDato.update()
            return

        peso_por_taza = self.dato[8]
        energia_por_taza = self.dato[4]
        proteina_por_taza = self.dato[5]
        lipidos_por_taza = self.dato[6]
        hidratos_por_taza = self.dato[7]
        
        print(valor_cantidad)
        factor_conversion = valor_cantidad / self.dato[3]

        self.kcal.value = round(factor_conversion * energia_por_taza,2)
        self.proteina.value = round(factor_conversion * proteina_por_taza,2)
        self.lipidos.value = round(factor_conversion * lipidos_por_taza,2)
        self.hidratos.value = round(factor_conversion * hidratos_por_taza,2)
        self.route.page.update()
        
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarAlimento,self.content, "Ingrese la cantidad a registrar:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
        
    def registrarAlimento(self,e):
        id = self.route.getId()
        # fecha = datetime.datetime.today().strftime(f"%Y-%m-%d")
        fecha = self.route.index.fechaActual
        horario = self.route.buscador.horario

        #datos = [id, self.dato[9], fecha, self.kcal.value, horario]

        datos = [id, self.dato[9], fecha, self.kcal.value,self.lipidos.value,self.hidratos.value,self.proteina.value,horario]

        
        mydb = FoodDatabase(self.route)
        mydb.connect()
        resultado = mydb.registrarAlimentoDia(datos)
        mydb.close()
        
        if resultado is None:
            Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
            return
        Notification(self.page,'Se ha registrado el alimento correctamente!','green').mostrar_msg()
        self.route.page.go('/index')
        
    def build(self):
        self.kcal.value = 0
        self.proteina.value = 0
        self.lipidos.value = 0
        self.hidratos.value = 0
        self.cantidadDato.value = 0
        return self.carta