from typing import Any, List, Optional, Union
import flet as ft
from flet_core.control import Control, OptionalNumber
from flet_core.ref import Ref
from flet_core.types import AnimationValue, ClipBehavior, OffsetValue, ResponsiveNumber, RotateValue, ScaleValue

class SideMenu(ft.UserControl):
    def __init__(self, route):
        super().__init__()
        self.route = route
        
        self.color = '#FFFCF2'
        self.GRIS = '#4D4D4D'
        
        self.cont = ft.Container(            
            padding=ft.padding.all(5),
            #bgcolor=colors.ON_INVERSE_SURFACE,                       
            border_radius=ft.border_radius.all(5),
            visible=False,
        )       
        
        self.rail = ft.NavigationRail(
            expand=True,
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            # extended=True,
            min_width=150,
            min_extended_width=450,
            # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
            group_alignment=-0.9,
            bgcolor='#F2E8CF',
            
            destinations=[
                ft.NavigationRailDestination(
                    
                    padding=ft.padding.all(50),
                    icon_content=ft.Icon(ft.icons.LOCAL_DINING_OUTLINED,color='#4D4D4D', size=45),
                    selected_icon_content=ft.Icon(ft.icons.LOCAL_DINING, size=70,color='#5F6F52'),
                    label_content=ft.Text("Pagina Principal",color='black',size=15),
                ),
                ft.NavigationRailDestination(
                    padding=ft.padding.all(50),
                    icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS_OUTLINED,color='#4D4D4D', size=45),
                    selected_icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS, size=70,color='#5F6F52'),
                    label_content=ft.Text("Informe",color='black',size=15),
                ),
                ft.NavigationRailDestination(
                    padding=ft.padding.all(50),
                    icon_content=ft.Icon(ft.icons.SPORTS_HANDBALL,color='#4D4D4D', size=45),
                    selected_icon_content=ft.Icon(ft.icons.SPORTS_HANDBALL, size=70,color='#5F6F52'),
                    label_content=ft.Text("Registro de Ejercicios",color='black',size=15),
                ),
                ft.NavigationRailDestination(
                    padding=ft.padding.all(50),
                    icon_content=ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_SHARP,color='#4D4D4D', size=45),
                    selected_icon_content=ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_SHARP, size=70,color='#5F6F52'),
                    label_content=ft.Text("Competencia",color='black',size=15),
                ),
            ], on_change=self.selectedIndex,
        )
        self.cont.content = self.rail
        
    def selectedIndex(self,e):
        if e.control.selected_index == 0:
            self.route.page.go('/index')
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 1:
            self.route.page.go('/informe')
            self.route.page.update()
            self.update()
            return
        # elif e.control.selected_index == 2:
        #     self.route.page.go('/ejercicio')
        #     self.route.page.update()
        #     self.update()
        #     return
        elif e.control.selected_index == 3:
            self.route.page.go('/competencia')
            self.route.page.update()
            self.update()
            return

    def build(self):
        return self.cont