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
        self.GRIS = '#FFFFFF'
        
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
                    icon_content=ft.Icon(ft.icons.LOCAL_DINING_OUTLINED,color='black'),
                    selected_icon_content=ft.Icon(ft.icons.LOCAL_DINING),
                    label_content=ft.Text("Pagina Principal",color='black'),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS_OUTLINED,color='black'),
                    selected_icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS),
                    label_content=ft.Text("Informe",color='black'),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.SPORTS_HANDBALL,color='black'),
                    selected_icon_content=ft.Icon(ft.icons.SPORTS_HANDBALL),
                    label_content=ft.Text("Registro de Ejercicios",color='black'),
                ),
                ft.NavigationRailDestination(
                    icon_content=ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_SHARP,color='black'),
                    selected_icon_content=ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_SHARP),
                    label_content=ft.Text("Competencia",color='black'),
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
        elif e.control.selected_index == 2:
            self.route.page.go('/registro_ejercicios')
            self.route.page.update()
            self.update()
            return
        elif e.control.selected_index == 3:
            self.route.page.go('/competencia')
            self.route.page.update()
            self.update()
            return

    def build(self):
        return self.cont