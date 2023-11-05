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
        
        self.rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        # extended=True,
        min_width=150,
        min_extended_width=450,
        # leading=ft.FloatingActionButton(icon=ft.icons.CREATE, text="Add"),
        group_alignment=-0.9,
        bgcolor=self.GRIS,
        destinations=[
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.FOOD_BANK_OUTLINED,color='black'),
                selected_icon_content=ft.Icon(ft.icons.FOOD_BANK),
                label_content=ft.Text("Pagina Principal",color='black'),
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS_OUTLINED,color='black'),
                selected_icon_content=ft.Icon(ft.icons.LIBRARY_BOOKS),
                label_content=ft.Text("Informe",color='black'),
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_SHARP,color='black'),
                selected_icon_content=ft.Icon(ft.icons.FORMAT_LIST_NUMBERED_SHARP),
                label_content=ft.Text("Competencia",color='black'),
            ),
        ], on_change=self.selectedIndex,
    )
        
    def selectedIndex(self,e):
        if e.control.selected_index == 0:
            self.page.go('/index')
        elif e.control.selected_index == 1:
            self.page.go('/informe')
        elif e.control.selected_index == 2:
            self.page.go('/competencia')

        
    def build(self):
        return self.rail