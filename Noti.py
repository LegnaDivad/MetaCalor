from typing import Tuple
import flet as ft
from flet_core.control import Control
from flet_core.types import AnimationValue, ClipBehavior
import daemon
from daemon import runner

import datetime
import sys
from plyer import notification
from threading import Thread
import time

def get_user_input() -> Tuple[str, str]:
    msg = input("Ingrese el mensaje de la notificación: ")
    userInputTime = input("Ingrese la hora de la alarma (en formato HH:MM): ")
    return msg, userInputTime

class MyDaemonRunner(runner.DaemonRunner):
       def __init__(self, app):
           super().__init__(app)
           self.daemon_context = daemon.DaemonContext()

       def parse_args(self):
           pass

       def daemonize(self):
           pass

class Notification(ft.UserControl):
    def __init__(self, page, msg, color):
        super().__init__()
        self.page = page
        self.msg = msg
        self.color = color
        
        self.content = ft.Text(value=msg, color=color, style=ft.TextThemeStyle.BODY_LARGE)
        self.snack_bar = ft.SnackBar(
            bgcolor="#677C77",
            content=self.content,
            elevation=10,
            duration=6000,
            show_close_icon=True,
            behavior=ft.SnackBarBehavior.FLOATING,
            dismiss_direction=ft.DismissDirection.END_TO_START
        )
        
    def mostrar_msg(self):
        self.page.snack_bar = self.snack_bar
        self.snack_bar.open = True

def run():
        if len(sys.argv) < 3:
            msg, userInputTime = get_user_input()
        else:
            msg = sys.argv[1]
            userInputTime = sys.argv[2]

        # Obtener la fecha y hora actual
        timeNow = datetime.datetime.now()

        # Mostrar la fecha y hora de la alarma
        print(f'La alarma está configurada para: {userInputTime}')

        # Función que se ejecutará para mostrar la notificación
        def my_function():
            while True:
                # Obtener la fecha y hora actual
                currentTime = datetime.datetime.now()

                # Comprobar si la fecha y hora actual coincide con la fecha y hora de la alarma
                if currentTime.strftime('%H:%M') == userInputTime:
                    notification.notify(
                        # Título de la notificación
                        title="Metacalor",
                        # El texto de la notificación
                        message=msg,
                        # El icono de la notificación (debe estar en formato .ico)
                        app_icon="icon.ico",
                        # Tiempo de duración de la notificación en segundos (un minuto equivale a 60 segundos)
                        timeout=60
                    )
                
                # Esperar un segundo antes de verificar nuevamente la hora actual
                time.sleep(1)

        # Crear un hilo para ejecutar la función de notificación
        notification_thread = Thread(target=my_function)
        notification_thread.start()

        # Esperar a que el hilo de notificación termine antes de finalizar el programa principal
        notification_thread.join()

if __name__ == "__main__":
       my_daemon = MyDaemonRunner(run)
       my_daemon.do_action()
