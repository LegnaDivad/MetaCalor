import flet as ft
from SideMenu import SideMenu
from IndexNuevo import Index
from Appbar import Appbar
from Competencia import Competencia
from Informe import Informe
from Login import Login
from Registro import Register
from Search import Search
from Perfil import Perfil
from datetime import datetime
from Registro_Ejercicio import RegistroEjercicios
from SearchEjercicios import SearchEjercicios
from CrearPlatillo import CreadorPlatillos
from SearchPlatillos import SearchPlatillos
from SearchIngredientes import SearchIngredientes

class Router:
    def __init__(self,page: ft.Page):
        self.page = page
        
        self.index = Index(self)
        self.competencia = Competencia(self)
        self.informe = Informe(self)
        self.login = Login(self)
        self.registro = Register(self)
        self.buscador = Search(self)
        self.perfil = Perfil(self)
        self.registroEjercicios = RegistroEjercicios(self)
        self.buscadorEjercicios = SearchEjercicios(self)
        self.crearPlatillo = CreadorPlatillos(self)
        self.buscadorPlatillos = SearchPlatillos(self)
        self.buscadorIngredientes = SearchIngredientes(self)
        
        self.idLogin = None
        fechaActual = datetime.now()
        fechaYYYYMMMDD = fechaActual.strftime("%Y:%m:%d")
        self.fechaHoy = fechaYYYYMMMDD
        
        self.routes = {
            '/' : self.login,
            '/registro' : self.registro,
            '/index' : self.index,
            '/informe' : self.informe,
            '/competencia' : self.competencia,
            '/buscador' : self.buscador,
            '/perfil' : self.perfil,
            '/registro_ejercicios' : self.registroEjercicios,
            '/buscador_ejercicios' : self.buscadorEjercicios,
            '/crear_platillo' : self.crearPlatillo,
            '/buscador_platillos':self.buscadorPlatillos,
            '/buscador_ingredientes':self.buscadorIngredientes
        }
        
        self.llamada = {
            '/' : self.login.inicializar,
            '/registro' : self.registro.inicializar,
            '/index' : self.index.inicializar,
            '/informe' : self.informe.inicializar,
            '/competencia' : self.competencia.inicializar,
            '/buscador' : self.buscador.inicializar,
            '/perfil' : self.perfil.inicializar,
            '/registro_ejercicios' : self.registroEjercicios.inicializar,
            '/buscador_ejercicios' : self.buscadorEjercicios.inicializar,
            '/crear_platillo' : self.crearPlatillo.inicializar,
            '/buscador_platillos':self.buscadorPlatillos.inicializar,
            '/buscador_ingredientes':self.buscadorIngredientes.inicializar
        }
        
        self.menu = SideMenu(self)
        self.bar = Appbar(self)
        self.page.appbar = self.bar.build()
        self.page.appbar.visible = False
        
        self.container = ft.Container(expand=True,content=self.routes['/'],padding=10)
        self.body = ft.Row(
            expand=True,
            controls=[
                self.menu,
                ft.VerticalDivider(color='black'),
                self.container,
            ]
        )
        
    def setLogInfo(self,datos):
        self.idLogin = datos[2]
        
    def getId(self):
        return self.idLogin

    def Logout(self):
        self.idLogin = None
        
    def getFecha(self):
        return self.fechaHoy
        
    def route_change(self,e):
        self.container.content = self.routes[e.route]
        self.page.update()
        
        self.llamada[e.route]()
        self.page.update()