from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Notification import Notification
from AlertDialog import *
from Database import FoodDatabase, UserDatabase, MetaDatabase, generalDatabaseAccess, EjerciciosDatabase
import datetime
import decimal


class CartaRegistroAlimento(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.datos = datos
        
        self.GRIS = '#252422'
        
        self.botonModificar = ft.IconButton(icon=ft.icons.EDIT,icon_color='blue',on_click=self.boton_modificar)
        self.botonEliminar = ft.IconButton(icon=ft.icons.DELETE_OUTLINE,icon_color='red',on_click=self.eliminarAlimento)
        
        self.valido = False
        
        self.nombre = ft.Text(value=f"Alimento: {datos[0]}",color='white',weight=ft.FontWeight.BOLD)
        self.calorias = ft.Text(value=f"Kcals: {datos[1]}",color='white',weight=ft.FontWeight.BOLD)
        
        self.cantidadDato = ft.TextField(
            label='Cantidad',
            on_change=self.calcular_nutrientes,
            input_filter=ft.InputFilter(
                regex_string=r"[0-9.]", 
                replacement_string=""
                )
            )
        
        self.peso = ft.Text(color='black',value=0)
        self.kcal = ft.Text(color='black',value=0)
        self.proteina = ft.Text(color='black',value=0)
        self.lipidos = ft.Text(color='black',value=0)
        self.hidratos = ft.Text(color='black',value=0)
        self.unidad = ft.Text(value=f'Unidad: {datos[2]}',color='black')
        
        self.content = ft.Container(
            expand=False,
            content=ft.ResponsiveRow(
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
        
        self.carta = ft.Card(

            content=ft.Container(
                padding=10,height=100,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Column(
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
        mydb.eliminarRegistroAlimento(self.datos[7])
        mydb.close()
        
        self.route.index.agregarComidas()
        self.route.page.update()
        
    def calcular_nutrientes(self,e):
        try:
            decimal.Decimal(self.cantidadDato.value)
            self.valido = True
        except (decimal.InvalidOperation, ValueError):
            self.valido = False
            self.proteina.value = 0
            self.kcal.value = 0
            self.lipidos.value = 0
            self.hidratos.value = 0
            self.cantidadDato.value = None
            self.route.page.update()
            return
        
        mydb = FoodDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerAlimentoId(self.datos[9],self.datos[7])
        mydb.close()
        
        valor_cantidad = decimal.Decimal(self.cantidadDato.value)
        
        # peso_por_taza = self.datos[8]
        energia_por_cantidad = resultado[4]
        proteina_por_cantidad = resultado[5]
        lipidos_por_cantidad = resultado[6]
        hidratos_por_cantidad = resultado[7]

        factor_conversion = valor_cantidad / resultado[3]

        self.kcal.value = round(factor_conversion * energia_por_cantidad,2)
        self.proteina.value = round(factor_conversion * proteina_por_cantidad,2)
        self.lipidos.value = round(factor_conversion * lipidos_por_cantidad,2)
        self.hidratos.value = round(factor_conversion * hidratos_por_cantidad,2)
        self.route.page.update()
        
    def boton_modificar(self,e):
        dialog = RegisterDialog(self.modificarRegistro,self.content, "Ingrese la nueva cantidad:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
        
    def modificarRegistro(self,e):
        if self.valido:
            IDRegistro= self.datos[7]
            id = self.route.getId()

            datos = [self.kcal.value,self.lipidos.value,self.proteina.value,self.hidratos.value,self.datos[7],self.route.getId()]
            
            mydb = UserDatabase(self.route)
            mydb.connect()
            resultado = mydb.modificarRegistro(datos)
            
            if resultado is None:
                Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
                return
            
            Notification(self.page,'Se ha modificado el alimento correctamente!','green').mostrar_msg()
            self.route.index.agregarComidas()
            self.route.page.go('/index')
        else:
            Notification(self.page,'Debes de registrar una cantidad valida!','red').mostrar_msg()
        
        
    def build(self):
        return self.carta

class CartaBuscador(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.dato = datos
        
        self.valido = False
        #color en listado de buscador
        self.nombre = ft.Text(value=f'Alimento: {datos[0]} | Categoria: {datos[1]}',text_align='center',color='white')
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)
        
        self.peso = ft.Text(color='black',value=0)
        self.kcal = ft.Text(color='black',value=0)
        self.proteina = ft.Text(color='black',value=0)
        self.lipidos = ft.Text(color='black',value=0)
        self.hidratos = ft.Text(color='black',value=0)
        self.unidad = ft.Text(value=f'Unidad: {datos[2]}',color='black')
        
        self.cantidadDato = ft.TextField(
            label='Cantidad',
            on_change=self.calcular_nutrientes,
            input_filter=ft.InputFilter(
                regex_string=r"[0-9.]", 
                replacement_string=""
                )
            )
        
        self.content = ft.Container(
            expand=False,
            content=ft.ResponsiveRow(
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
            self.valido = True
        except (decimal.InvalidOperation, ValueError):
            # print("El valor ingresado no es convertible a decimal.Decimal.")
            # self.cantidadDato.border_color = 'red'
            self.valido = False
            self.proteina.value = 0
            self.kcal.value = 0
            self.lipidos.value = 0
            self.hidratos.value = 0
            self.cantidadDato.value = None
            self.route.page.update()
            return
        
        valor_cantidad = decimal.Decimal(self.cantidadDato.value)
        
        peso_por_taza = self.dato[8]
        energia_por_cantidad = self.dato[4]
        proteina_por_cantidad = self.dato[5]
        lipidos_por_cantidad = self.dato[6]
        hidratos_por_cantidad = self.dato[7]
        
        print(valor_cantidad)
        factor_conversion = valor_cantidad / self.dato[3]

        self.kcal.value = round(factor_conversion * energia_por_cantidad,2)
        self.proteina.value = round(factor_conversion * proteina_por_cantidad,2)
        self.lipidos.value = round(factor_conversion * lipidos_por_cantidad,2)
        self.hidratos.value = round(factor_conversion * hidratos_por_cantidad,2)
        self.route.page.update()
        
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarAlimento,self.content, "Ingrese la cantidad a registrar:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
        
    def registrarAlimento(self,e):
        if self.valido:
            id = self.route.getId()
            # fecha = datetime.datetime.today().strftime(f"%Y-%m-%d")
            fecha = self.route.index.fechaActual
            horario = self.route.buscador.horario

            datos = [id, self.dato[9], fecha, self.kcal.value,self.lipidos.value,self.hidratos.value,self.proteina.value,horario]

            mydb = FoodDatabase(self.route)
            mydb.connect()
            resultado = mydb.registrarAlimentoDia(datos)
            mydb.close()
            
            if resultado is None:
                Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
                return
            
            Notification(self.page,'Se ha registrado el alimento correctamente!','green').mostrar_msg()
            self.registrarProgresoMeta()
            self.route.page.go('/index')
        else:
            Notification(self.page,'Debes de registrar una cantidad valida!','red').mostrar_msg()

    def build(self):
        self.kcal.value = 0
        self.proteina.value = 0
        self.lipidos.value = 0
        self.hidratos.value = 0
        self.cantidadDato.value = None
        # self.cantidadDato.update()
        return self.carta
    
class CartaMeta(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.dato = datos
        
        self.GRIS = '#252422'
        
        
        self.valorMeta = ft.Text(value=int(self.dato[0]),color=self.GRIS,size=20)
        self.valorActual = ft.Text(value=int(self.dato[2]),color=self.GRIS,size=20)
        valor = self.valorActual.value / self.valorMeta.value
        
        self.descripcion = ft.Text(value=self.dato[1],color=self.GRIS,size=25,weight=ft.FontWeight.BOLD,text_align='center')
        self.progreso = ft.ProgressBar(height=13,value=valor,width=700,color='blue',bgcolor='black')
        
        self.metasContenedor = ft.Card(
            color='#FFFCF2',
            height=180,
            content=ft.Container(
                expand=True,
                padding=25,
                content=ft.Row(
                    # expand=True,
                    controls=[
                        ft.Container(
                            # expand=1,
                            width=200,
                            height=210,
                            bgcolor='#FFFCF2',
                            border_radius=ft.border_radius.all(13),
                            content=ft.Icon(ft.icons.EMOJI_EVENTS,color='black',size=60)
                        ),
                        ft.Column(
                            expand=True,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.descripcion,
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        self.valorActual,
                                        ft.Text(value=" / ",color=self.GRIS,size=20),
                                        self.valorMeta
                                    ]
                                ),
                                self.progreso
                            ]
                        )
                    ]
                )
            )
        )
        
    def build(self):
        return self.metasContenedor
    
class CartaPlatillos(ft.UserControl):
    def __init__(self,route,datos):
        super().__init__()
        self.route = route
        self.datos = datos
        
        
        self.nombre = ft.Text(value=datos[2],color='black')
        self.kcal = ft.Text(value=datos[3],color='black')
        
        self.mostrarNombre = ft.Text(value=datos[2])
        self.mostrarKcal = ft.Text(value=datos[3])
        
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)
        
        self.content = ft.ResponsiveRow(
            controls=[
                self.mostrarNombre,
                self.mostrarKcal
            ]
        )
        
        self.carta = ft.Card(
                expand=True,
                height=70,
                color='white',
                content=ft.Container(
                    expand=True,
                    padding=15,
                    content=ft.Row(
                        expand=True,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(
                                controls=[
                                    self.nombre,
                                    self.kcal,
                                ]
                            ),
                            self.BotonAgregar
                        ]
                    )
                ),
        )
        
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarAlimentos,self.content, "¿Quieres añadir a tu registro de alimentos este platillo?")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.go('/index')
        self.route.page.update()
        
    def registrarAlimentos(self,e):
            id = self.route.getId()
            fecha = self.route.index.fechaActual
            horario = self.route.crearPlatillo.horario

            mydb = FoodDatabase(self.route)
            mydb.connect()
            
            mydb2 = FoodDatabase(self.route)
            mydb2.connect()
            
            resultado = mydb2.obtenerAlimentosPlatillosRegistro(id,self.datos[0])
            mydb2.close()
            
            for datos in resultado:
                lista = [id,datos[0],fecha,datos[1],datos[3],datos[4],datos[2],horario]
                mydb.registrarAlimentoDia(lista)
            mydb.close()
            
            Notification(self.page,'Se han añadido los alimentos!','green').mostrar_msg()
           

    
    def build(self):
        return self.carta
    
class CartaRegistroEjercicios(ft.UserControl):
    def __init__(self,route,datos):
        super().__init__()
        self.route = route
        self.datos = datos

        self.valido = False
        self.GRIS = '#252422'

        self.botonModificar = ft.IconButton(icon=ft.icons.EDIT,icon_color='blue',on_click=self.boton_actualizar_accion)
        self.botonEliminar = ft.IconButton(icon=ft.icons.DELETE_OUTLINE,icon_color='red', on_click=self.boton_eliminar_accion)

        self.nombre = ft.Text(value=f"Ejercicio: {datos[0]}")

        horas = datos[2].seconds // 3600
        minutos = (datos[2].seconds % 3600) // 60
        self.cantidadDisplay = ft.Text(value=f'Tiempo: {horas}:{minutos}',text_align='center',color='white')

        self.nuevaDuracion = datetime.time(0,0,0)
        
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
                ]
            ),
        )

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

    def boton_eliminar_accion(self, e):
        print(self.datos[4])
        dialog = EliminacionDialog(self.eliminarEjercicio, "¿Seguro de Querer Eliminar el Ejercicio?")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def eliminarEjercicio(self,e):
        mydb = EjerciciosDatabase(self.route)
        mydb.connect()
        mydb.eliminarRegistroAlimento(self.datos[4])
        
        Notification(self.page,'Ejercicio Eliminado con Éxito!','green').mostrar_msg()
        mydb.close()
        self.route.registroEjercicios.inicializar()

    def boton_actualizar_accion(self, e):
        dialog = ActualizacionDialog(self.actualizarEjercicio,self.dialogContent,"Ingrese la Nueva Duración del Ejercicio")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def actualizarEjercicio(self,e):
        if self.valido:
            nueva_hora = datetime.time(self.hora.value,self.minuto.value)
            mydb = EjerciciosDatabase(self.route)
            print(self.datos[4])
            mydb.connect()
            mydb.modificarRegistro(nueva_hora,self.datos[4])
            Notification(self.page,'Ejercicio Modificado con Éxito!','green').mostrar_msg()
            mydb.close()
            self.route.registroEjercicios.inicializar()
        
    def confirmarHora(self, e):
        try:
            hora_int = int(self.hora.value)
            if hora_int > 24:
                self.hora.value = None
            else:
                self.hora.value = hora_int
                self.valido = True
        except (TypeError, ValueError):
            self.hora.value = None 

        self.hora.update()

    def confirmarMinuto(self, e):
        try:
            minuto_int = int(self.minuto.value)
            if minuto_int > 59:
                self.minuto.value = None
            else:
                self.minuto.value = minuto_int
                self.valido = True
        except (TypeError, ValueError):
            self.minuto.value = None 

        self.minuto.update()

    def build(self):
        return self.carta

class CartaBuscadorEjercicios(ft.UserControl):
    def __init__(self,route,datos):
        super().__init__()
        self.route = route
        self.dato = datos

        self.valido = False
        
        self.nombre = ft.Text(value=f'Actividad: {datos[0]}',text_align='center',color='white')
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)

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
                ]
            ),
        )
        
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.nombre
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
        
    def confirmarHora(self, e):
        try:
            hora_int = int(self.hora.value)
            if hora_int > 24:
                self.hora.value = None
            else:
                self.hora.value = hora_int
                self.valido = True
        except (TypeError, ValueError):
            self.hora.value = None 

        self.hora.update()

    def confirmarMinuto(self, e):
        try:
            minuto_int = int(self.minuto.value)
            if minuto_int > 59:
                self.minuto.value = None
            else:
                self.minuto.value = minuto_int
                self.valido = True
        except (TypeError, ValueError):
            self.minuto.value = None 

        self.minuto.update()

    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarEjercicio,self.dialogContent, "Ingrese los siguientes datos:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
        
    def registrarEjercicio(self,e):
        if self.valido:
            id = self.route.getId()
            fecha = self.route.index.fechaActual
            tiempo = datetime.time(self.hora.value,self.minuto.value)

            datos = [id, self.dato[1], fecha, tiempo]

            mydb = EjerciciosDatabase(self.route)
            mydb.connect()
            resultado = mydb.registrarEjercicios(datos)
            mydb.close()
            
            if resultado is None:
                Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
                return
            
            Notification(self.page,'Se ha registrado el ejercicio correctamente!','green').mostrar_msg()
            self.route.page.go('/Index')
        else:
            Notification(self.page,'Debes de registrar una cantidad valida!','red').mostrar_msg()

    def build(self):
        return self.carta

class CartaRegistroIngrediente(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.datos = datos
        
        self.GRIS = '#252422'
        
        self.botonModificar = ft.IconButton(icon=ft.icons.EDIT,icon_color='blue')
        self.botonEliminar = ft.IconButton(icon=ft.icons.DELETE_OUTLINE,icon_color='red')
        
        self.nombre = ft.Text(value=f"Nombre: {datos['nombre']}",color='white',weight=ft.FontWeight.BOLD)
        self.calorias = ft.Text(value=f"Calorías: {datos['kcal']}",color='white',weight=ft.FontWeight.BOLD)
        
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
                                            # self.botonEliminar
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
        self.route.page.update()
    

    
    def build(self):
        return self.carta

class CartaPlatilloBuscador(ft.UserControl):
    def __init__(self, route, datos):
        super().__init__()
        self.route = route
        self.dato = datos
        
        self.valido = False
        
        self.nombre = ft.Text(value=f'Alimento: {datos[0]} | Categoria: {datos[1]}',text_align='center',color='white',weight=ft.FontWeight.BOLD)
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)
        
        self.peso = ft.Text(color='white',value=0)
        self.kcal = ft.Text(color='white',value=0)
        self.proteina = ft.Text(color='white',value=0)
        self.lipidos = ft.Text(color='white',value=0)
        self.hidratos = ft.Text(color='white',value=0)
        self.unidad = ft.Text(value=f'Unidad: {datos[2]}',color='white')
        
        self.cantidadDato = ft.TextField(
            label='Cantidad',
            on_change=self.calcular_nutrientes,
            input_filter=ft.InputFilter(
                regex_string=r"[0-9.]", 
                replacement_string=""
                )
            )
        
        self.content = ft.Container(
            expand=False,
            content=ft.ResponsiveRow(
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
            self.valido = True
        except (decimal.InvalidOperation, ValueError):
            # print("El valor ingresado no es convertible a decimal.Decimal.")
            # self.cantidadDato.border_color = 'red'
            self.valido = False
            self.proteina.value = 0
            self.kcal.value = 0
            self.lipidos.value = 0
            self.hidratos.value = 0
            self.cantidadDato.value = None
            self.route.page.update()
            return
        
        valor_cantidad = decimal.Decimal(self.cantidadDato.value)
        
        peso_por_taza = self.dato[8]
        energia_por_cantidad = self.dato[4]
        proteina_por_cantidad = self.dato[5]
        lipidos_por_cantidad = self.dato[6]
        hidratos_por_cantidad = self.dato[7]
        
        print(valor_cantidad)
        factor_conversion = valor_cantidad / self.dato[3]

        self.kcal.value = round(factor_conversion * energia_por_cantidad,2)
        self.proteina.value = round(factor_conversion * proteina_por_cantidad,2)
        self.lipidos.value = round(factor_conversion * lipidos_por_cantidad,2)
        self.hidratos.value = round(factor_conversion * hidratos_por_cantidad,2)
        self.route.page.update()
        
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.anadirAlimento,self.content, "Ingrese la cantidad a registrar:")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()
        
    def regresarDatos(self,data):
        self.route.crearPlatillo.anadirLista(data)
        
    def anadirAlimento(self,e):
        if self.valido:
            fecha = self.route.index.fechaActual

            datos_usuario = {
                'nombre': self.dato[0],
                'kcal': self.kcal.value,
                'idAlimento': self.dato[9],
                'fecha': fecha,
                'lipidos': self.lipidos.value,
                'hidratos': self.hidratos.value,
                'proteina': self.proteina.value
            }

            Notification(self.page,'Se ha añadido el alimento!','green').mostrar_msg()
            self.regresarDatos(datos_usuario)
        else:
            Notification(self.page,'Debes de registrar una cantidad valida!','red').mostrar_msg()

    def build(self):
        self.kcal.value = 0
        self.proteina.value = 0
        self.lipidos.value = 0
        self.hidratos.value = 0
        self.cantidadDato.value = None
        return self.carta
    

class CartaPlatillo(ft.UserControl):
    def __init__(self,route,datos):
        self.route = route
        self.datos =datos
        self.listaDatos = []
        self.horario = self.route.buscador.horario

        self.nombre = ft.Text("{}".format(datos[0]))

        mydb = generalDatabaseAccess(self.route)
        mydb.connect()

        resultado = mydb.recuperarRegistro("A.Alimento, A.Categoria, A.Unidad,Cantidad, A.Energia_kcal, A.Proteina_g, A.Lipidos_g, A.Hidratos_de_carbono_g, A.Peso_bruto_g, A.ID_Alimento R.Cantidad",
                                           "Alimentos AS A, Relación_Alimento_Platillo AS R",
                                           "R.ID_Platillo = {} AND R.ID_Platillo = {} AND A.ID_Alimento = R.ID_Alimento".format(self.datos[1], self.datos[2]))

        self.lista = ft.ListView(expand=True,padding=5,auto_scroll=True)

        mydb.close()
        self.cuentaCalorias = 0
        for datos in resultado:
            self.calcular_nutrientes(datos)
            self.cuentaCalorias += self.listaDatos[-1][3]
            item = ft.Card(
                content=ft.Container(
                padding=5,height=70,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Row(
                                expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        controls=[
                                            ft.Text("{}".format(datos[0])),
                                            ft.Text("Cantidad: {}".format(datos[3])),
                                            ft.Text("KiloCalorias: {}".format(self.listaDatos[-1][3]))
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ),
            color='#4D4D4D'
            )
            self.lista.controls.append(item)

        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.nombre,
                    self.lista
                ]
            )
        )

        self.calorias = ft.Text("Total Kilocalorias: {}".format(self.cuentaCalorias))
        self.BotonAgregar = ft.IconButton(icon=ft.icons.APPLE,icon_color='GREEN',icon_size=30,on_click=self.boton_verIngredientes)


        self.carta = ft.Card(
            content= ft.Container(
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
                                            self.calorias,
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
            color="#4D4D4D"
        )

    def calcular_nutrientes(self, data):
        idUsuario = self.route.getId()
        # fecha = datetime.datetime.today().strftime(f"%Y-%m-%d")
        fecha = self.route.index.fechaActual


        energia_por_cantidad = data[4]
        proteina_por_cantidad = data[5]
        lipidos_por_cantidad = data[6]
        hidratos_por_cantidad = data[7]

        print(data[11])
        factor_conversion = data[11] / data[3]

        calorias = round(factor_conversion * energia_por_cantidad,2)
        proteinas = round(factor_conversion * proteina_por_cantidad,2)
        lipidos = round(factor_conversion * lipidos_por_cantidad,2)
        hidratos = round(factor_conversion * hidratos_por_cantidad,2)

        datos = [idUsuario, data[9], fecha, calorias,lipidos,hidratos,proteinas,self.horario]

        self.listaDatos.append(datos)


    def boton_verIngredientes(self,e):
        dialog = PlatilloDialog(self.content, "Información del Platillo")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def build(self):
        return self.carta
    
class CartaIngredienteBuscador(CartaBuscador):
    def __init__(self,route,datos, listIngredientes):
        super().__init__(route,datos)
        self.lista = listIngredientes

    def registrarAlimento(self,e):
        if self.valido:
            datos = "{},{}".format(self.dato[9], self.valido)

            self.lista.append(datos)
            print(self.lista)
            if datos is None:
                Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
                return
            self.route.page.go('/crear_platillo')
        else:
            Notification(self.page,'Debes de registrar una cantidad valida!','red').mostrar_msg()

    
class CartaInforme(ft.UserControl):
    def __init__(self, route, CalConsumidas, calQuemadas, Fecha):
        super().__init__()
        self.route = route
        self.fecha = Fecha
        self.calQuemadas = calQuemadas
        self.CalConsumidas = CalConsumidas
        
        valCalQuem = 0
        valCalCom = 0

        if self.calQuemadas > self.CalConsumidas:
            valCalQuem = 1
            valCalCom = self.CalConsumidas / self.calQuemadas
        else:
            valCalQuem = self.calQuemadas / self.CalConsumidas
            valCalCom =  1

        self.barraCon = ft.ProgressBar(value=valCalCom,height=10, width = 400, color=ft.colors.GREEN_500, bgcolor=ft.colors.with_opacity(0, '#ff6666'))
        self.barraQuem = ft.ProgressBar(value=valCalQuem, height=10, width = 400, color='#900C3F', bgcolor=ft.colors.with_opacity(0, '#ff6666'))
        self.columnaBarras = ft.Container(
            content= ft.Column(
                controls=[
                    self.barraCon, self.barraQuem
                ]
            )
        )

        años, meses, días = self.descomponer_timedelta(self.fecha)
        self.columnaTexto = ft.Container(
             content= ft.Column(
                controls=[
                    ft.Text(value="{:.2f} Kiloalorias Consumidas".format(self.CalConsumidas),color= 'white'),
                    ft.Text(value="{:.2f} Kilocalorias Quemadas".format(self.calQuemadas),color= 'white')
                ]
            )
        )
        
        self.carta = ft.Card(
            content= ft.Container(
                padding=10,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            expand=True,
                            content=ft.Column(
                                        controls=[
                                        ft.Text(value="Calorias del Dia {} de {} del {}".format(días, meses, años),color= 'orange'),
                                            ft.Row(spacing=20,alignment=ft.MainAxisAlignment.CENTER,
                                            controls=[
                                            self.columnaTexto,
                                            self.columnaBarras
                                        ]
                                    )
                                ]
                            )
                        )
                    ]
                )
            ),
            color="#355E3B"
        )

    def descomponer_timedelta(self, delta):
        return delta.year, delta.month, delta.day
    
    def build(self):
        return self.carta

        
