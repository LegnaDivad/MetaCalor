import flet as ft
from Routing import Router
from Appbar import Appbar


def main(page: ft.Page):
    routing = Router(page) 
    page.window_width = 900
    page.window_height = 800
    page.padding = 0
    
    page.theme = ft.Theme(  
        scrollbar_theme=ft.ScrollbarTheme(
            main_axis_margin=10,
            thumb_color={
                ft.MaterialState.DEFAULT: 'black',
                ft.MaterialState.HOVERED: ft.colors.BLUE,
            },
            thickness=10,
            radius=4,
            interactive=True,
        )
    )
    
    page.on_route_change = routing.route_change
    
    page.add(routing.body)
    
    page.go('/')
    page.update()
    
# ft.app(target=main,assets_dir="assets",view=ft.AppView.WEB_BROWSER)
ft.app(target=main,assets_dir="assets")



