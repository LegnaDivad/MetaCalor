import flet as ft
from SideMenu import SideMenu
from Index import Index
from Appbar import Appbar
from Competencia import Competencia
from Informe import Informe
from Login import Login
from Registro import Register


class Router:
    def __init__(self,page: ft.Page):
        self.page = page
        
        self.index = Index(self)
        self.competencia = Competencia(self)
        self.informe = Informe(self)
        self.login = Login(self)
        self.registro = Register(self)
        
        self.routes = {
            '/' : self.login,
            '/registro' : self.registro,
            '/index' : self.index,
            '/informe' : self.informe,
            '/competencia' : self.competencia,
        }
        
        self.llamada = {
            '/' : self.login.inicializar,
            '/registro' : self.registro.inicializar,
            '/index' : self.index.inicializar,
            '/informe' : self.informe.inicializar,
            '/competencia' : self.competencia.inicializar,
        }
        
        self.container = ft.Container(expand=True,content=self.routes['/'])
        
        self.menu = SideMenu(self)
        
        self.bar = Appbar(self)
        self.page.navigation_bar = self.bar.build()
        
        self.menu.visible = False
        self.page.navigation_bar.visible = False
        
        self.body = ft.Row(
            expand=True,
            controls=[
                self.menu,
                ft.VerticalDivider(color='black'),
                self.container,
            ]
        )
        
    def route_change(self,e):
        if self.page.route != '/' and self.page.route != '/registro':
            self.menu.visible = True
            self.page.navigation_bar.visible = True
        else:
            self.menu.visible = False
            self.page.navigation_bar.visible = False
        self.container.content = self.routes[e.route]
        self.page.update()
        
        self.llamada[e.route]()
        self.page.update()