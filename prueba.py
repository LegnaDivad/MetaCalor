import flet as ft

def main(page: ft.Page):
    
    a = ft.Container(
        height=50,width=50,bgcolor='blue'
    )
    
    b = ft.Container(
        height=50,width=50,bgcolor='pink'
    )
    
    c = ft.Container(
        height=50,width=50,bgcolor='blue'
    )
    
    r = ft.Row(
        controls=[
            a,b,c
        ]
    )
    
    page.add(r)
    
ft.app(target=main)