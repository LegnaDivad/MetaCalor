import flet as ft
from Database import generalDatabaseAccess, EjerciciosDatabase
from Cartas import CartaBuscadorEjercicios

class SearchEjercicios(ft.UserControl):
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
        
        self.SearchText = ft.TextField(
            label='Filtrar por Nombre de Ejercicio',
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
                            self.SearchButtom
                        ]
                    )
                ),
                ft.Container(
                    expand=True,
                    content=self.SearchList
                )
            ]
        )
        
    def buscarElementos(self,e):
        self.SearchList.clean()        
        if self.SearchText.value == '':
            return
        
        mydb = generalDatabaseAccess(self.route)
        mydb.connect()

        dato = self.SearchText.value
        resultado = mydb.recuperarRegistro("Tipo_Act, ID_AF","Actividad_Física AS A","A.Tipo_Act LIKE '%{}%'".format(dato))
        mydb.close()
        
        if resultado is not None:
            for datos in resultado:
                item = CartaBuscadorEjercicios(self.route,datos)
                self.SearchList.controls.append(item)
            self.SearchList.update()
        else:
            return None

    def buscarTodo(self):
        self.SearchList.clean() 

        mydb = EjerciciosDatabase(self.route)
        mydb.connect()
        resultado = mydb.mostrarEjercicios()
        
        for datos in resultado:
            item = CartaBuscadorEjercicios(self.route,datos)
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

        print('Inicializando buscador de Ejercicios')
