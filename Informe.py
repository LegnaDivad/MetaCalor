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
        
        
        self.kcalTotales = ft.Text(value='hola',color='black')
        
        
        self.index = ft.Container(
            expand=True,
            content=self.kcalTotales
        )
        
    def generarInforme(self,e):
        pass
    
    def obtenerInfo(self):
        fecha_actual = datetime.datetime.now()
        # fecha = datetime.datetime(fecha_actual.year, fecha_actual.month, 19)
        mydb = UserDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerRegistrosSemana(self.route.getId(),fecha_actual)
        mydb.close()
        suma = 0
        for dato in resultado:
            suma += dato[0]
        print(suma)
        
    def build(self):
        return self.index
    
    def inicializar(self):
        self.obtenerInfo()
        print('Inicializando Informe')