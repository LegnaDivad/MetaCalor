import flet as ft
from Routing import Router

def main(page: ft.Page):
    routing = Router(page)

    page.padding = 0
    page.bgcolor = "#FFFCF2"
    
    page.on_route_change = routing.route_change
    
    page.add(routing.body)
    
    page.go('/index')
    page.update()
    
# ft.app(target=main,assets_dir="assets",view=ft.AppView.WEB_BROWSER)
ft.app(target=main,assets_dir="assets")
