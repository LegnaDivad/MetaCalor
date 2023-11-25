import flet as ft
import math
from Database import generalDatabaseAccess

class SeguimientoCalorias(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route

        self.dataCalorias = (870,500,1000)

        self.metaProgressbarG = ft.ProgressBar(height=18, color=ft.colors.GREEN_700, bgcolor=ft.colors.with_opacity(0, '#ff6666'))
        self.metaProgressbarG.value = self.dataCalorias[0] / self.dataCalorias[2]
        if(self.metaProgressbarG.value >= 0.85):
            self.metaProgressbarG.color = ft.colors.CYAN_500

        self.metaProgressbarO = ft.ProgressBar(height=10, color=ft.colors.ORANGE_700, bgcolor=ft.colors.with_opacity(0, '#ff6666'))
        self.metaProgressbarO.value = self.dataCalorias[1] / self.dataCalorias[2]
        self.metaProgressbarY = ft.ProgressBar(height=18, color=ft.colors.YELLOW_400, bgcolor="#647c90", rotate=math.pi)
        self.metaProgressbarY.value = 0.15

        self.barrasDeMedicion = ft.Stack(
            [
                self.metaProgressbarY,
                self.metaProgressbarG,
                ft.Column(controls=[self.metaProgressbarO], alignment=ft.MainAxisAlignment.CENTER)
                
            ], expand= True,
        )

        self.seguimientoDia = ft.Container(
            content= ft.Column(controls=[ft.Text(value='Seguimiento de Calorias: ',weight='bold',size=15,color=ft.colors.WHITE),
                                        self.barrasDeMedicion],
                                        spacing=5),
            bgcolor= '#252422',
            border_radius = 13,
            height = 50,
            padding = 5,
            expand= True
        )

    def actualizaSeguimiento(self):
        self.metaProgressbarG.value = self.dataCalorias[0] / self.dataCalorias[2]
        self.metaProgressbarO.value = self.dataCalorias[1] / self.dataCalorias[2]
        
        self.dataCalorias = self.obetenerSeguimientoDeCalorias(self.route)
        self.barrasDeMedicion.update()
        self.seguimientoDia.update()

    def getSeguimiento(self):
        return self.barrasDeMedicion.update()

    def obetenerSeguimientoDeCalorias(self, route):
        id_usuario = route.getId()

        mydb = generalDatabaseAccess(route)
        mydb.connect()

        dataUsuario = mydb.recuperarRegistro("TMB * FactorDeActividad, Peso, TMB",
                                              "Usuario",
                                              "ID_Usuario  = {}".format(id_usuario)
                                              )
    
        actFisicaUsuario = mydb.recuperarRegistro("A.MET, R.Duración_Act",
                                              "Registro_Actividad_Física AS R, Actividad_Física AS A",
                                              "R.ID_Usuario  = {} AND R.ID_AF = A.ID_AF AND R.Fecha_Registro = CURDATE()".format(id_usuario)
                                              )

        consumoUsuario = mydb.recuperarRegistro("SUM(Total_calorias)",
                                              "Registro_Alimentos",
                                              "ID_Usuario  = {} AND Fecha_Registro  = Fecha_Registro = CURDATE()".format(id_usuario)
                                              )

        if consumoUsuario == None:
            consumoUsuario = 0

        totalCalQuemadas = 0
        if actFisicaUsuario is not None:
            for act in actFisicaUsuario:
                totalCalQuemadas += (act[0] * dataUsuario[1] * act[1])

            totalCalQuemadas += dataUsuario[0]

        mydb.close()

        return (consumoUsuario, totalCalQuemadas, dataUsuario[2])
    
    def build(self):
        return self.seguimientoDia
    
    def inicializa(self):
        self.actualizaSeguimiento()
        print("Inicializando Seguimiento")