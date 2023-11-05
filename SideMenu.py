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
        self.GRIS = '#252422'
        
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
                icon=ft.icons.HOME_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.HOME),
                label_content=ft.Text("Inicio"),
            ),
            ft.NavigationRailDestination(
                icon_content=ft.Icon(ft.icons.PRODUCTION_QUANTITY_LIMITS),
                selected_icon_content=ft.Icon(ft.icons.PRODUCTION_QUANTITY_LIMITS),
                label_content=ft.Text("Catalogo"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Producto"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.CHECKLIST_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.CHECKLIST),
                label_content=ft.Text("Citas"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.ADD_BUSINESS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.ADD_BUSINESS),
                label_content=ft.Text("Donaciones"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.PERSON_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.PERSON),
                label_content=ft.Text("Perfil"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.NOTIFICATIONS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.NOTIFICATIONS),
                label_content=ft.Text("Notificaciones"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.SETTINGS_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.SETTINGS),
                label_content=ft.Text("Ajustes"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.QUESTION_ANSWER_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.QUESTION_ANSWER),
                label_content=ft.Text("Preguntas"),
            ),
            ft.NavigationRailDestination(
                icon=ft.icons.LOGOUT_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.LOGOUT),
                label_content=ft.Text("Salir"),
            ),
        ], on_change=self.selectedIndex,
    )
        
    def selectedIndex(self,e):
        if e.control.selected_index == 0:
            self.page.go('/index')
        elif e.control.selected_index == 1:
            self.page.go('/catalogo')
        elif e.control.selected_index == 2:
            self.page.go('/CRUDProducto')
        # elif e.control.selected_index == 3:
        #     self.page.go('/')
        elif e.control.selected_index == 4:
            self.page.go('/donacion')
        elif e.control.selected_index == 5:
            self.page.go('/profile')
        # elif e.control.selected_index == 6:
        #     self.page.go('/')
        # elif e.control.selected_index == 7:
        #     self.page.go('/')
        # elif e.control.selected_index == 8:
        #     self.page.go('/')
        elif e.control.selected_index == 9:
            self.route.setId(None)
            self.page.go('/')
        
    def build(self):
        return self.rail