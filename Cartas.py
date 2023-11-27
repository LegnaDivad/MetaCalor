from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue
from Notification import Notification
from AlertDialog import *
from Database import FoodDatabase, UserDatabase, MetaDatabase
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
        Kcal = self.datos[1]
        
        mydb = UserDatabase(self.route)
        mydb.connect()
        mydb.eliminarRegistroAlimento(self.datos[7])
        mydb.close()
        
        dia_actual = datetime.datetime.now()
        dia_actual_str = dia_actual.strftime('%Y-%m-%d')
        semana_actual = datetime.datetime.now().isocalendar()[1]
        semana_actual = semana_actual + 1
        
        mydb = MetaDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerRegistrosSem(self.route.getId(),'Calorica',semana_actual)
        
        if resultado:
            for dato in resultado:
                rest = dato[0] - decimal.Decimal(Kcal)
                
                mydb.registrarProgresoMeta(self.route.getId(),rest,'En Progreso',4)
                mydb.registrarProgresoMeta(self.route.getId(),rest,'En Progreso',5)
                
                
        if self.datos[8] == 'Verduras':
            resultado2 = mydb.obtenerRegistrosDiarios(self.route.getId(),2,dia_actual_str)
            if resultado2:
                if resultado2[1] == 'Completada':
                    mydb.restarObjetivosUsuario(self.route.getId())
                rest = resultado2[0] - 1
                mydb.registrarProgresoMeta(self.route.getId(),rest,'En Progreso',2)
                
            
        if self.datos[8] == 'Frutas':
            resultado2 = mydb.obtenerRegistrosDiarios(self.route.getId(),1,dia_actual_str)
            if resultado2:
                if resultado2[1] == 'Completada':
                    mydb.restarObjetivosUsuario(self.route.getId())
                rest = resultado2[0] - 1
                mydb.registrarProgresoMeta(self.route.getId(),rest,'En Progreso',1)
                
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
        
        self.valido = False
        
        self.nombre = ft.Text(value=f'Alimento: {datos[0]} | Categoria: {datos[1]}',text_align='center',color='white')
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
    
    def registrarProgresoMeta(self):
        fecha_actual = datetime.datetime.now()
        totalKcal = 0
        
        mydb = MetaDatabase(self.route)
        mydb.connect()
        resultados = mydb.obtenerMetasEnProgreso(self.route.getId())
        
        mydb2 = UserDatabase(self.route)
        mydb2.connect()
        resultadoCal = mydb2.obtenerRegistrosSemana(self.route.getId(),fecha_actual)
        
        for datosCal in resultadoCal:
            totalKcal += datosCal[0]
        
        if not resultados:
            print("no hay objetivos pendientes")
        else:
            for datos in resultados:
                # if datos[3] == 'Diaria':
                #     if self.dato[1] == 'Verduras':
                #         aux = datos[1]
                #         aux += 1
                #         # if aux == datos[2]:
                #         #     mydb.registrarProgresoMeta(self.route.getId(),aux,'Completada',2)
                #         #     mydb.actualizarObjetivosUsuario(self.route.getId())
                #         # elif aux < datos[2]:
                #         #     mydb.registrarProgresoMeta(self.route.getId(),aux,'En Progreso',2)
                #         if aux <= datos[2]:
                #             if aux == datos[2]:
                #                 mydb.registrarProgresoMeta(self.route.getId(), aux, 'Completada', 2)
                #                 mydb.actualizarObjetivosUsuario(self.route.getId())
                #             else:
                #                 mydb.registrarProgresoMeta(self.route.getId(), aux, 'En Progreso', 2)
                #     elif self.dato[1] == 'Frutas':
                #         # if datos[1] is None:
                #         #     aux = 1
                #         # else:
                #         aux = datos[1]
                #         if aux == datos[2]:
                #             mydb.registrarProgresoMeta(self.route.getId(),aux+1,'Completada',1)
                #             mydb.actualizarObjetivosUsuario(self.route.getId())
                #         elif aux < datos[2]:
                #             mydb.registrarProgresoMeta(self.route.getId(),aux,'En Progreso',1)
                if datos[4] == 'Calorica':
                    auxC = totalKcal
                    if auxC < datos[2] and datos[2] == 2000:
                        mydb.registrarProgresoMeta(self.route.getId(),auxC,'En progreso',4)
                    elif auxC >= datos[2] and datos[2] == 2000:
                        mydb.registrarProgresoMeta(self.route.getId(),auxC,'Completada',4)
                        mydb.actualizarObjetivosUsuario(self.route.getId())
                    if auxC < datos[2] and datos[2] == 10000:
                        mydb.registrarProgresoMeta(self.route.getId(),auxC,'En progreso',5)
                    elif auxC >= datos[2] and datos[2] == 10000:
                        mydb.registrarProgresoMeta(self.route.getId(),auxC,'Completada',5)
                        mydb.actualizarObjetivosUsuario(self.route.getId())
        mydb.close()

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
                            bgcolor='#E5E5E5',
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


class CartaIngrediente(CartaRegistroAlimento):
    def __init__(self,route,datos,list,pos):
        super().__init__(route,datos)
        self.pos = pos
        self.lista = list
        
    def eliminarAlimento(self,e):
        self.lista.pop(self.pos)
        self.route.index.agregarComidas()
        self.route.page.update()

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
    

class CartaPlatilloBuscador(ft.UserControl):
    def __init__(self,route,datos):
        self.route = route
        self.datos =datos
        self.listaDatos = []

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
        self.BotonAgregar = ft.IconButton(icon=ft.icons.ADD,icon_color='GREEN',icon_size=30,on_click=self.boton_agregar)
    

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

        datos = [idUsuario, data[9], fecha, calorias,lipidos,hidratos,proteinas]

        self.listaDatos.append(datos)
        
    
    def boton_agregar(self,e):
        dialog = RegisterDialog(self.registrarAlimento,self.content, "Información del Platillo")
        dialog.data = e.control.data
        self.route.page.dialog = dialog
        dialog.open = True
        self.route.page.update()

    def registrarAlimento(self,e):
        
        ladb = generalDatabaseAccess(self.route)
        ladb.connect()

        ladb.insertarRegistro("Registro_Platillo", "", "({},{}),{}".format(self.datos[0],self.datos[1],self.datos[2]))
        ladb.close()

        mydb = FoodDatabase(self.route)
        mydb.connect()

        resultado = not None

        for data in self.listaDatos:
            resultado = mydb.registrarAlimentoDia(data)
            if resultado == None:
                break
                
        mydb.close()
        if resultado is None:
                Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
                return
        
    def build(self):
        return self.carta
