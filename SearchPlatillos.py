import flet as ft
from Database import generalDatabaseAccess
from Cartas import CartaPlatilloBuscador

class SearchPlatillos(ft.UserControl):
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

        self.AddButtom = ft.ElevatedButton(
            text='Crear un Nuevo Platillo',
            icon=ft.icons.SEARCH,
            on_click=self.crearPlatillo,
            style=ft.ButtonStyle(
                color="#26587E",
                bgcolor="#E3E9F0"
            )
        )
        
        self.SearchText = ft.TextField(
            label='Filtrar por Nombre de Platillo',
            autofocus=True,
            focused_color=self.focused_color,
            text_style=ft.TextStyle(color=self.GRIS),
            focused_border_color=self.GRIS,
            label_style=ft.TextStyle(color=self.GRIS),
            expand=True,
            color='black'
        )
        
        self.SearchList = ft.ListView(expand=1,padding=20,auto_scroll=True,)
        
        self.buscadorGUI = ft.Column(
            expand=True,
            controls=[
                ft.Container(
                    alignment=ft.alignment.center,
                    content=ft.Row(
                        vertical_alignment=ft.CrossAxisAlignment.START,
                        controls=[
                            self.SearchText,
                            self.SearchButtom,
                            self.AddButtom
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    content=self.SearchList
                )
            ]
        )

    def crearPlatillo(self, e):
        self.route.page.bgcolor = '#F2E8CF'
        self.SearchText.value = None
        self.SearchText.update()
        self.SearchList.clean()

        self.route.page.go('/crear_platillo')
        
    def buscarElementos(self,e):
        self.SearchList.clean()        
        if self.SearchText.value == '':
            return
        
        mydb = generalDatabaseAccess(self.route)
        mydb.connect()

        dato = self.SearchText.value
        resultado = mydb.recuperarRegistro("Nombre_platillo, ID_Platillo, Descripción",
                                           "Platillo AS P",
                                           "P.Nombre_platillo LIKE '%{}%'".format(dato))
        
        resultado2 = mydb.recuperarRegistro("Nombre_platillo, ID_Platillo Descripción",
                                           "Platillo AS P",
                                           "P.Nombre_platillo LIKE '%{}%' AND P.ID_Usuario ={}".format(dato, self.route.getId()))
        
        mydb.close()
        
        if resultado is not None:
            for datos in resultado:
                item = CartaPlatilloBuscador(self.route,datos)
                self.SearchList.controls.append(item)

        
        if resultado2 is not None:
            for datos in resultado2:
                item = CartaPlatilloBuscador(self.route,datos)
                self.SearchList.controls.append(item)

        self.SearchList.update()

    def buscarTodo(self):
        self.SearchList.clean() 

        mydb = generalDatabaseAccess(self.route)
        mydb.connect()

        resultado = mydb.recuperarRegistro("Nombre_platillo, ID_Platillo, Descripción",
                                           "Platillo AS P",
                                           "1")
        resultado2 = mydb.recuperarRegistro("Nombre_platillo, ID_Platillo, Descripción ",
                                           "Platillo AS P",
                                           "P.ID_Usuario ={}".format(self.route.getId()))
        mydb.close()
        
        for datos in resultado:
            item = CartaPlatilloBuscador(self.route,datos)
            self.SearchList.controls.append(item)
        self.SearchList.update()

        for datos in resultado2:
            item = CartaPlatilloBuscador(self.route,datos)
            self.SearchList.controls.append(item)
        self.SearchList.update()
        
    def build(self):
        return self.buscadorGUI
    
    def inicializar(self):
        self.route.page.bgcolor = '#F2E8CF'
        self.SearchText.value = None
        self.SearchText.update()
        self.SearchList.clean()
        self.buscarTodo()

        print('Inicializando buscador de Platillos')