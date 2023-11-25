from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Notification import Notification
from AlertDialog import *
from Database import FoodDatabase
from datetime import datetime, timedelta
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
        factor_conversion = valor_cantidad / self.dato[8]

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
        fecha = datetime.now()
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

class CartaRegistroEjercicios(ft.UserControl):
    def __init__(self,route,datos):
        super().__init__()
        self.route = route
        self.datos = datos
        
        self.GRIS = '#252422'
        
        self.botonModificar = ft.IconButton(icon=ft.icons.EDIT,icon_color='blue',on_click=self.boton_actualizar_accion)
        self.botonEliminar = ft.IconButton(icon=ft.icons.DELETE_OUTLINE,icon_color='red', on_click=self.boton_eliminar_accion)
        
        self.nombre = ft.Text(value=f"Ejercicio: {datos[0]}")

        horas = datos[1].seconds // 3600
        minutos = (datos[1].seconds % 3600) // 60
        self.cantidadDisplay = ft.Text(value=f'Tiempo: {horas}:{minutos}',text_align='center',color='white')
        
        self.cantidadDato = ft.TextField(value="0:0",label='Tiempo: HH:MM',on_submit=self.convertir_TIME)
        self.nuevaDuracion = time(0,0,0)

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
                                            self.nombre,
                                            self.cantidadDisplay
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

    def convertir_TIME(self, e):
        try:
            print(self.cantidadDato.value)
            stringHora = str(self.cantidadDato.value)
            partes_hora = stringHora.split(":")
            hora = int(partes_hora[0])
            minutos = int(partes_hora[1])
        except (decimal.InvalidOperation, ValueError):
            print("El valor ingresado es Inválido")
            self.cantidadDato.value = 0 
            self.cantidadDato.update()
            return None

        if hora < 0 or minutos < 0:
            print('No se Admiten Números Negativos')
            self.cantidadDato.value = 0
            self.cantidadDato.update()
            return None
        
        print(hora, minutos, stringHora)
        self.nuevaDuracion = time(hora, minutos, 0)

    def boton_eliminar_accion(self, e):
        dialog = EliminacionDialog(self.eliminarEjercicio, "¿Seguro de Querer Eliminar el Ejercicio?")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
    
    def eliminarEjercicio(self,e):
        mydb = generalDatabaseAccess(self.route)
        print(self.datos[2])
        mydb.connect()
        if mydb.eliminarRegistro("Registro_Actividad_Física","ID_RegDeAct = {}".format(self.datos[2])) != None:
            Notification(self.page,'Ejercicio Eliminado con Éxito!','green').mostrar_msg()
        mydb.close()
        self.route.registroEjercicios.inicializar()

    def boton_actualizar_accion(self, e):
        dialog = ActualizacionDialog(self.actualizarEjercicio,
                                self.cantidadDato,
                                "Ingrese la Nueva Duración del Ejercicio")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
    
    def actualizarEjercicio(self,e):
        self.convertir_TIME(e)

        mydb = generalDatabaseAccess(self.route)
        print(self.datos[2])
        mydb.connect()
        if mydb.modificarRegistro("Registro_Actividad_Física",
                                  "Duración_Act = '{}'".format(self.nuevaDuracion),
                                  "ID_RegDeAct = {}".format(self.datos[2])) != None:
            Notification(self.page,'Ejercicio Modificado con Éxito!','green').mostrar_msg()
        mydb.close()

        self.route.registroEjercicios.inicializar()
        
    def build(self):
        return self.carta


class CartaBuscadorEjercicios(ft.UserControl):
    def __init__(self,route,datos):
        super().__init__()
        self.route = route
        self.dato = datos
        
        self.TIME = time(0,0)

        self.nombre = ft.Text(value=f'Actividad: {datos[0]}',text_align='center',color='white')
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)
        
        self.cantidadDato = ft.TextField(value="0:0",label='Tiempo: HH:MM',on_submit=self.convertir_TIME)
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.nombre,self.cantidadDato
                ]
            ),height= 400
        )
        
        self.GRIS = '#252422'
        
        self.carta = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            height = 100,
                            content=ft.Row(
                                expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Column(
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
            color=self.GRIS, height=66
        )
    
    def convertir_TIME(self, e):
        try:
            stringHora = self.cantidadDato.value
            partes_hora = stringHora.split(":")
            hora = int(partes_hora[0])
            minutos = int(partes_hora[1])
        except (decimal.InvalidOperation, ValueError):
            print("El valor ingresado es Inválido")
            self.cantidadDato.value = 0 
            self.cantidadDato.update()
            return None

        if hora < 0 or minutos < 0:
            print('No se Admiten Números Negativos')
            self.cantidadDato.value = 0
            self.cantidadDato.update()
            return None
        
        print(hora, minutos, stringHora)
        self.TIME = time(hora, minutos, 0)

        return not None
    
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarEjercicio, self.content, "Ingrese la duración del ejercicio:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def registrarEjercicio(self,e):
        if self.convertir_TIME(e) == None:
            Notification(self.page,'Tiempo Inválido!','red').mostrar_msg()
            return

        id = self.route.getId()
        fecha = datetime.now()
        
        print(self.dato[1],id,self.TIME,fecha)

        mydb = generalDatabaseAccess(self.route)
        mydb.connect()
        resultado = mydb.insertarRegistro("Registro_Actividad_Física ",
                                              "(ID_AF, ID_Usuario, Duración_Act, Fecha_Registro)",
                                              "({}, {}, '{}', '{}')".format(self.dato[1],id,self.TIME,fecha))
        mydb.close()
        
        if resultado is None:
            Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
            return
        Notification(self.page,'Se ha registrado el ejercicio correctamente!','green').mostrar_msg()
        self.route.page.go('/registro_ejercicios')
    
    def build(self):
        self.cantidadDato.value = 0
        return self.carta
