import flet as ft
from Cartas import CartaIngrediente
from Database import generalDatabaseAccess

class CreadorPlatillos(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.GRIS = '#252422'
        self.lvIngredientes = ft.ListView(expand=True,padding=20,auto_scroll=True)
        self.listaIngredientes = []

        self.crearButton = ft.ElevatedButton(text='Crear Platillo',
                                    icon=ft.icons.CHECK,
                                    style=ft.ButtonStyle(color ='white', bgcolor="#009E60"),
                                    on_click=self.crearPlatillo)
        
        self.limpiarButton = ft.ElevatedButton(text='Cancelar',
                                    icon=ft.icons.ARROW_BACK,
                                    style=ft.ButtonStyle(color ='white', bgcolor=ft.colors.RED_500),
                                    on_click=self.cancelarPlatillo)

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
            input_filter=ft.TextOnlyInputFilter(),
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
            input_filter=ft.TextOnlyInputFilter(),
            height= 70, border_color='#50C878', bgcolor='white'
        )
        
        self.row2=ft.Row(
            controls=[
                self.SearchTextDescripción,self.limpiarButton
            ], alignment= ft.MainAxisAlignment
        )

        self.LabelsCarD = ft.Card(
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

        self.botonRegistroEjercicio = ft.ElevatedButton(text='Registrar Ingrediente',
                                                     icon=ft.icons.ADD,style=ft.ButtonStyle(color ='white', bgcolor="#009E60"),
                                                     on_click=self.buscadorIngredientes)

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

        
        self.mainContainer = ft.Container(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    self.LabelsCarD,
                    self.registroIngredientes,
                ]
            )
        )

    def crearPlatillo(self,e):
        self.lvIngredientes.clean()
        mydb = generalDatabaseAccess(self.route)
        mydb.connect()
        newID = mydb.insertarRegistro("Platillo","(ID_Usuario, Nombre_platillo, Descripción)",
                              "{},'{}','{}'".format(self.route.getId(),
                                                    self.SearchTextNombre,
                                                    self.SearchTextDescripción))

        if  newID == None:
            print("Sin_ID")
            return

        grandString = ""
        for ingrediente in self.listaIngredientes:
             grandString += "({},{}), ".format(newID,ingrediente[0])
            
        mydb.insertarRegistro("Relación_Alimento_Platillo",
                               "(ID_Platillo,ID_Alimento,Cantidad)",
                               "{}".format(grandString))

        mydb.close()
        self.listaIngredientes.remove()

        self.cancelarPlatillo()

    def cancelarPlatillo(self):
        pass
        
    def buscadorIngredientes(self,e):
        self.page.go('/buscador_ingredientes')
        
    def agregarIngredientes(self):
        self.lvIngredientes.clean()
        
        i = 0
        if self.listaIngredientes is not None:
            for dataIngrediente in self.listaIngredientes:
                item = CartaIngrediente(self.route,dataIngrediente,self.lvIngredientes,i)
                self.lvIngredientes.controls.append(item)
                i+=1
        self.lvIngredientes.update()
        self.route.page.update()
        
    def build(self):
        return self.mainContainer
    
    def inicializar(self):
        # self.route.page.bgcolor = '#98FB98'
        self.agregarIngredientes()
        self.route.page.update()
        print('Inicializando Creador de Platillos')