import flet as ft
from SideMenu import SideMenu
# from Index import Index
from IndexNuevo import Index
from Appbar import Appbar
from Competencia import Competencia
from Informe import Informe
from Login import Login
from Registro import Register
from Search import Search

class Router:
    def __init__(self,page: ft.Page):
        self.page = page
        
        self.index = Index(self)
        self.competencia = Competencia(self)
        self.informe = Informe(self)
        self.login = Login(self)
        self.registro = Register(self)
        self.buscador = Search(self)
        self.registroEjercicios = RegistroEjercicios(self)
        self.buscadorEjercicios = SearchEjercicios(self)
        
        self.idLogin = None
        
        self.routes = {
            '/' : self.login,
            '/registro' : self.registro,
            '/index' : self.index,
            '/informe' : self.informe,
            '/competencia' : self.competencia,
            '/buscador' : self.buscador,
            '/registro_ejercicios' : self.registroEjercicios,
            '/buscador_ejercicios' : self.buscadorEjercicios
        }
        
        self.llamada = {
            '/' : self.login.inicializar,
            '/registro' : self.registro.inicializar,
            '/index' : self.index.inicializar,
            '/informe' : self.informe.inicializar,
            '/competencia' : self.competencia.inicializar,
            '/buscador' : self.buscador.inicializar,
            '/registro_ejercicios' : self.registroEjercicios.inicializar,
            '/buscador_ejercicios' : self.buscadorEjercicios.inicializar
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
        
    def route_change(self,e):
        self.container.content = self.routes[e.route]
        self.page.update()
        
        self.llamada[e.route]()
        self.page.update()
