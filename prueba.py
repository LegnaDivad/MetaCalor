from datetime import datetime, timedelta

# Obtener la fecha y hora actual
hoy = datetime.now()

# Bucle para retroceder hasta encontrar el día lunes
while hoy.strftime('%A') != 'Monday':
    hoy -= timedelta(days=1)  # Restar un día
    # Puedes agregar una condición para evitar que retroceda indefinidamente si lo deseas

# Imprimir la fecha del último lunes
print("El último lunes fue:", hoy.strftime('%Y-%m-%d'))
