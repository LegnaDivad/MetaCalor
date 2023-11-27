import flet as ft

class ConfirmDialog(ft.AlertDialog):

    def __init__(self, function, title="", content=""):
        super().__init__()
        self.function = function

        self.modal=True
        self.title=ft.Text(title)
        self.content=ft.Text(content)
        self.actions=[
            ft.TextButton("No", on_click=self.canceled),
            ft.TextButton(content=ft.Text("Si", color="red"), on_click=self.confirmed),
        ]
        self.actions_alignment=ft.MainAxisAlignment.END
        self.shape=ft.RoundedRectangleBorder(radius=10)

    def build(self):
        return self
    
    def confirmed(self, e):
        self.open = False
        self.update()
        self.function(self.data)
    
    def canceled(self, e):
        self.open = False
        self.update()
        
class RegisterDialog(ft.AlertDialog):
    def __init__(self, function, contenido, title=""):
        super().__init__()
        self.function = function

        self.modal=True
        self.title=ft.Text(title)
        self.content=contenido
        self.actions=[
            ft.TextButton(content=ft.Text("Cancelar", color="red"), on_click=self.canceled),
            ft.TextButton(content=ft.Text("Añadir", color="Green"), on_click=self.confirmed),
        ]
        self.actions_alignment=ft.MainAxisAlignment.END
        self.shape=ft.RoundedRectangleBorder(radius=10)

    def build(self):
        return self
    
    def confirmed(self, e):
        self.open = False
        self.update()
        self.function(self.data)
    
    def canceled(self, e):
        self.open = False
        self.update()
        
class EliminacionDialog(ft.AlertDialog):
    def __init__(self, function, title=""):
        super().__init__()
        self.function = function
        self.modal=True
        self.title=ft.Text(title)
        self.actions=[
            ft.TextButton(content=ft.Text("Regresar", color="blue"), on_click=self.canceled),
            ft.TextButton(content=ft.Text("Eliminar", color="red"), on_click=self.confirmed),
        ]
        self.actions_alignment=ft.MainAxisAlignment.END
        self.shape=ft.RoundedRectangleBorder(radius=10)

    def build(self):
        return self

    def confirmed(self, e):
        self.open = False
        self.update()
        self.function(self.data)

    def canceled(self, e):
        self.open = False
        self.update()

class ActualizacionDialog(ft.AlertDialog):
    def __init__(self, function, contenido, title=""):
        super().__init__()
        self.function = function

        self.modal=True
        self.title=ft.Text(title)
        self.content=contenido
        self.actions=[
            ft.TextButton(content=ft.Text("Cancelar", color="red"), on_click=self.canceled),
            ft.TextButton(content=ft.Text("Modificar", color="Green"), on_click=self.confirmed),
        ]
        self.actions_alignment=ft.MainAxisAlignment.END
        self.shape=ft.RoundedRectangleBorder(radius=10)

    def build(self):
        return self

    def confirmed(self, e):
        self.open = False
        self.update()
        self.function(self.data)

    def canceled(self, e):
        self.open = False
        self.update()