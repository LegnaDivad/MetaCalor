from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import os
import platform
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.utils import ImageReader

def definirOS():
    sistema_operativo = platform.system()
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop")

    nombre_archivo = "Reporte Semana Metacalor.pdf"

    ruta_pdf = os.path.join(escritorio, nombre_archivo)

    os.makedirs(escritorio, exist_ok=True)

    return ruta_pdf

def definirImagen():
    sistema_operativo = platform.system()
    nombre = ""

    if sistema_operativo == "Windows":
        nombre = 'assets\\images\\Logo3.PNG'
    elif sistema_operativo == "Darwin":
        nombre = 'assets/images/Logo3.PNG'
    else:
        nombre = 'assets/images/Logo3.PNG'

    return nombre

def generar_pdf(name, peso, altura, nutrientes, kilocalorias, listQuemadas, listConsumidas, fechas):
    nombre = definirOS()
    print(nombre)
    pdf_canvas = canvas.Canvas(nombre, pagesize=letter)

    dirImagen = definirImagen()

    pdf_canvas.drawImage(dirImagen, 100, 700, width=200, height=100)

    pdf_canvas.setFont("Helvetica", 25)
    pdf_canvas.drawString(100, 680, "Reporte Semanal Metacalor")
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(100, 660, "Usuario: {}".format(name))
    pdf_canvas.drawString(100, 640, "Balance De Nutrientes:")

    dias = ["{}".format(fechas[0]), "{}".format(fechas[1]), "{}".format(fechas[2]),
            "{}".format(fechas[3]), "{}".format(fechas[4]), "{}".format(fechas[5]), "{}".format(fechas[6])]

    plt.bar(dias, listConsumidas, label='Kilocalorias Consumidas')
    plt.bar(dias, listQuemadas, label='Kilocalorias Quemadas', bottom=listConsumidas)

    plt.xlabel('Días')
    plt.ylabel('KiloCalorias')
    plt.title('Comparacaion de gestión de Calorias, Calorias Totales: {}'.format(kilocalorias))

    plt.legend()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_reader = ImageReader(buffer)

    pdf_canvas.drawImage(imagen_reader, 150, 620, width=500, height=300)

    pdf_canvas.showPage()

    plt.pie(nutrientes, labels=nutrientes, autopct='%1.1f%%', startangle=90)
    plt.title('Balance de Macronutrientes')

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    imagen_reader = ImageReader(buffer)

    pdf_canvas.drawImage(imagen_reader, 150, 700, width=400, height=400)

    print("casi")

    # Guardar el PDF
    pdf_canvas.save()
    print("yes")