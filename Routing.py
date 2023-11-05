import flet as ft
from Index import Index
from Login import Login
from SideMenu import SideMenu
from Register import Register
from Catalogo import Catalogo
from CRUDProducto import CRUDProducto
from Perfil import Perfil
from Donaciones import Donaciones

class Router:
    def __init__(self,page: ft.Page):
        self.page = page
        
        self.index = Index(self)
        self.login = Login(self)
        self.register = Register(self)
        self.catalogo = Catalogo(self)
        self.crudproducto = CRUDProducto(self)
        self.perfil = Perfil(self)
        self.donaciones = Donaciones(self)
        
        self.IdLogin = None
        
        self.routes = {
            '/' : self.login,
            '/index' : self.index,
            '/register' : self.register,
            '/catalogo' : self.catalogo,
            '/CRUDProducto' : self.crudproducto,
            '/profile' : self.perfil,
            '/donacion' : self.donaciones 
        }
        
        self.llamada = {
            '/' : self.login.inicializar,
            '/index' : self.index.inicializar,
            '/register' : self.register.inicializar,
            '/catalogo' : self.catalogo.inicializar,
            '/CRUDProducto' : self.crudproducto.inicializar,
            '/profile' : self.perfil.inicializar,
            '/donacion' : self.donaciones.inicializar 
        }
        
        self.container = ft.Container(expand=True,content=self.routes['/'])
        
        self.menu = SideMenu(self)
        self.menu.visible = False
        
        self.body = ft.Row(
            expand=True,
            controls=[
                self.menu,
                self.container,
            ]
        )
        
    def setId(self,dato):
        self.IdLogin = dato
        
    def returnId(self):
        return self.IdLogin
        
    def route_change(self,e):
        if self.page.route != '/' and self.page.route != '/register':
            self.menu.visible = True
        else:
            self.menu.visible = False
        self.container.content = self.routes[e.route]
        self.page.update()
        
        self.llamada[e.route]()
        self.page.update()