import flet as ft
from Cartas import CartaPlatilloBuscador,CartaRegistroIngrediente,CartaPlatillos
from Database import generalDatabaseAccess, FoodDatabase
from Notification import Notification

class CreadorPlatillos(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        self.lvIngredientes = ft.ListView(expand=4,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        self.lvPlatillos = ft.ListView(expand=4,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        self.listaIngredientes = []
        
        self.SearchList = ft.ListView(expand=1,padding=20,auto_scroll=ft.ScrollMode.ALWAYS)
        
        self.focused_color = '#26587E'
        
        self.crearButton = ft.ElevatedButton(
            text='Crear Platillo',
            icon=ft.icons.CHECK,
            style=ft.ButtonStyle(color ='white', bgcolor="#009E60"),
            on_click=self.registrarPlatillo
        )
        
        self.limpiarButton = ft.ElevatedButton(text='Cancelar',
                                    icon=ft.icons.ARROW_BACK,
                                    style=ft.ButtonStyle(color ='white', bgcolor=ft.colors.RED_500),
                                    )

        self.SearchTextNombre = ft.TextField(
            label='Nombre del Platillo',
            autofocus=True,
            focused_color='#26587E',
            text_style=ft.TextStyle(color='#43962c'),
            focused_border_color='#50C878',
            label_style=ft.TextStyle(color='#50C878'),
            expand=True,
            color='#50C878',
            max_length=99,
            input_filter=ft.InputFilter(regex_string=r"[a-z,.;'1-9 ]"),
            height= 70, border_color='#50C878', bgcolor='white'
            )
        
        self.row1 = ft.Row(
            controls=[
                self.SearchTextNombre,self.crearButton
            ], alignment= ft.MainAxisAlignment
        )
        self.SearchTextDescripción = ft.TextField(
            label='Descripción del Platillo',
            autofocus=True,
            focused_color='#26587E',
            text_style=ft.TextStyle(color='#43962c'),
            focused_border_color='#50C878',
            label_style=ft.TextStyle(color='#50C878'),
            expand=True,
            color='#50C878',
            max_length=255,
            input_filter=ft.InputFilter(regex_string=r"[a-z,.;'1-9 ]"),
            height= 70, border_color='#50C878', bgcolor='white'
        )
        
        self.row2=ft.Row(
            controls=[
                self.SearchTextDescripción,self.limpiarButton
            ], alignment= ft.MainAxisAlignment
        )
        
        self.LabelsCarD = ft.Container(
        ft.Card(
            key='tmba',
            content=ft.Container(
                content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=5,bgcolor=self.GRIS,border_radius=13,
                        content=ft.Column(
                            controls=[
                                self.row1,
                                self.row2
                            ]
                        )
                    )
                ]
            ),
            ),
            color='#43962c'
        )
        )

        self.botonRegistroEjercicio = ft.ElevatedButton(
            text='Eliminar todos',
            color ='white', bgcolor="red",
            on_click=self.eliminarTodos
            )

        self.SearchButtom = ft.IconButton(
            icon=ft.icons.SEARCH,
            on_click=self.buscarElementos,
            style=ft.ButtonStyle(
                color="#26587E",
                bgcolor="#E3E9F0"
            )
        )
        
        self.SearchText = ft.TextField(
            label='Nombre de Alimento',
            focused_color=self.focused_color,
            text_style=ft.TextStyle(color=self.GRIS),
            focused_border_color=self.GRIS,
            label_style=ft.TextStyle(color=self.GRIS),
            # expand=True,
            color='white',
            bgcolor='white'
        )

        self.registroIngredientes = ft.Card(
            expand=True,key='registraIngredientes',
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            ft.Icon(name=ft.icons.APPLE_ROUNDED,color='red',size=25),
                                            ft.Text(value='Ingredientes',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        controls=[
                                            self.botonRegistroEjercicio
                                        ],
                                    )
                                ),
                            ]
                        )  
                    ),
                    self.lvIngredientes
                ]
            ),
            color='#2AAA8A',
        )
        
        self.anadidos = ft.Card(
            expand=True,
            content=ft.Column(
                expand=True,horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Container(
                        padding=20,bgcolor=self.GRIS,border_radius=ft.border_radius.only(top_left=13,top_right=13),
                        content=ft.Row(
                            expand=True,alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Container(
                                    content=ft.Row(
                                        controls=[
                                            # ft.Icon(name=ft.icons.APPLE_ROUNDED,color='red',size=25),
                                            ft.Text(value='Añadidos',weight='bold',size=25,bgcolor=self.GRIS)
                                        ]
                                    ),
                                ),
                                self.SearchText,
                                self.SearchButtom
                            ]
                        )  
                    ),
                    self.SearchList
                ]
            ),
            color='#2AAA8A',
        )
        
        
        self.contenedorDesc = ft.Container(
            expand=True,
            padding=10,
            border_radius=ft.border_radius.all(12),
            bgcolor=self.GRIS,
            content=ft.Column(
                expand=True,
                controls=[
                    self.SearchTextNombre,
                    self.SearchTextDescripción,
                    self.crearButton,
                ]
            )
        )
        
        self.contenedorPlatillos = ft.Container(
            expand=True,
            padding=10,
            border_radius=ft.border_radius.all(12),
            bgcolor=self.GRIS,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=1,
                        content=ft.Text('Tus platillos',weight='bold',size=25)
                    ),
                    self.lvPlatillos
                ]
            )
        )
        
        
        self.mainContainer = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        expand=3,
                        content=ft.Row(
                            controls=[
                                self.contenedorDesc,
                                self.contenedorPlatillos,
                            ]
                        ),
                    ),
                    
                    ft.Container(
                        expand=5,
                        content=ft.Row(
                            controls=[
                                self.registroIngredientes,
                                self.anadidos,
                            ]
                        )
                    ),
                ]
            )
        )
        
    def eliminarTodos(self,e):
        self.listaIngredientes.clear()
        self.lvIngredientes.clean()
        self.lvIngredientes.update()
        
    def buscarElementos(self,e):
        self.SearchList.clean()
        mydb = FoodDatabase(self.route)
        mydb.connect()
        
        if self.SearchText.value == '':
            return
            
        dato = self.SearchText.value
        resultado = mydb.ObtenerAlimentos(dato)
        mydb.close()
        
        for datos in resultado:
            item = CartaPlatilloBuscador(self.route,datos)
            self.SearchList.controls.append(item)
        self.SearchList.update()
        
    def anadirLista(self,datosDic):
        
        self.SearchList.clean()
        self.SearchText.value = ''
        self.listaIngredientes.append(datosDic)
        item = CartaRegistroIngrediente(self.route,datosDic)
        self.lvIngredientes.controls.append(item)
        self.lvIngredientes.update()
        
        # print(self.listaIngredientes)
        
        
        self.mainContainer.update()
        
    def establecer_Horario(self,string):
        self.horario = string
        print(self.horario)
        
    def registrarPlatillo(self,e):
        total_kcal = 0
        total_lipidos = 0
        total_proteinas = 0
        total_hidratos = 0
        
        for alimento in self.listaIngredientes:
            total_kcal += alimento['kcal']
            total_lipidos += alimento['lipidos']
            total_proteinas += alimento['proteina']
            total_hidratos += alimento['hidratos']
        
        mydb = FoodDatabase(self.route)
        mydb.connect()
        
        datos = [self.route.getId(),self.SearchTextNombre.value,self.SearchTextDescripción.value,total_kcal]
        
        resultado = mydb.registrarPlatillo(datos,self.listaIngredientes)
        
        if resultado is not None:
            Notification(self.page,'Ha ocurrido un error!','red').mostrar_msg()
            return
        Notification(self.page,'Se ha registrado correctamente!','green').mostrar_msg()
        self.lvPlatillos.clean()
        self.lvIngredientes.clean()
        self.listaIngredientes.clear()
        self.SearchTextDescripción.value = None
        self.SearchTextNombre.value = None
        self.route.page.update()
        self.inicializar()
        

    def cargarPlatillos(self):
        self.lvPlatillos.clean()
        mydb = FoodDatabase(self.route)
        mydb.connect()
        resultado = mydb.obtenerPlatillos(self.route.getId())
        mydb.close()
        
        for datos in resultado:
            item = CartaPlatillos(self.route,datos)
            self.lvPlatillos.controls.append(item)
        self.lvPlatillos.update()

    def build(self):
        return self.mainContainer
    
    def inicializar(self):
        # self.route.page.bgcolor = '#98FB98'
        # self.agregarIngredientes()
        self.cargarPlatillos()
        self.route.page.update()
        print('Inicializando Creador de Platillos')