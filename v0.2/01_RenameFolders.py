import os
import re
import csv
from datetime import datetime

# CONFIGURACIÓN
execute_changes = False  # Cambia a True para ejecutar renombramientos
ruta_base = r'C:\Users\Usuario\Downloads\Proyectos\J1'
prefijo_despacho = "053804089001"

# Generar nombre del reporte con fecha y hora
fecha_hora_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
reporte_cambios = f"./reports/reporte_cambios_{fecha_hora_actual}.csv"
reporte_conflictos = f"./reports/reporte_conflictos_{fecha_hora_actual}.csv"

# Crear la carpeta 'reports' si no existe
os.makedirs("./reports", exist_ok=True)

# Función para limpiar el nombre
def limpiar_nombre(nombre):
    return re.sub(r'[^A-Za-z0-9]', '', nombre)

# Función para crear el nuevo nombre según la lógica
def crear_nuevo_nombre(nombre_original):
    numeros_proceso = re.search(r'(\d{4}-\d+)', nombre_original)
    if not numeros_proceso:
        return None

    numero_formato = numeros_proceso.group(1).replace('-', '')  # ej: 2023-00234 -> 202300234
    if len(numero_formato) < 9:
        numero_formato = numero_formato.zfill(9)

    parte_texto = nombre_original.replace(numeros_proceso.group(1), '').strip()
    parte_texto = re.sub(r'[^A-Za-z0-9]', '', parte_texto)
    nuevo_nombre = f"{prefijo_despacho}{numero_formato}00"

    if parte_texto:
        nuevo_nombre += f" {parte_texto}"

    return nuevo_nombre[:40]

# Preparar archivos de reporte
with open(reporte_cambios, 'w', newline='', encoding='utf-8') as f_cambios, \
     open(reporte_conflictos, 'w', newline='', encoding='utf-8') as f_conflictos:

    writer_cambios = csv.writer(f_cambios)
    writer_conflictos = csv.writer(f_conflictos)

    writer_cambios.writerow(["Ruta", "Nombre Original", "Nombre Nuevo"])
    writer_conflictos.writerow(["Ruta", "Nombre en Conflicto"])

    # Recorrer carpetas
    for dirpath, dirnames, _ in os.walk(ruta_base):
        for dirname in dirnames:
            ruta_completa = os.path.join(dirpath, dirname)

            if re.fullmatch(r'\d{23}', dirname):
                continue  # Ya cumple con los 23 dígitos

            nuevo_nombre = crear_nuevo_nombre(dirname)

            if not nuevo_nombre:
                continue  # No se pudo extraer número de proceso

            nueva_ruta = os.path.join(dirpath, nuevo_nombre)

            if os.path.exists(nueva_ruta):
                writer_conflictos.writerow([ruta_completa, nuevo_nombre])
                continue

            writer_cambios.writerow([ruta_completa, dirname, nuevo_nombre])

            if execute_changes:
                os.rename(ruta_completa, nueva_ruta)
                print(f"Renombrada: {dirname} -> {nuevo_nombre}")
            else:
                print(f"(Simulado) Renombraría: {dirname} -> {nuevo_nombre}")

print(f"Reporte generado: {reporte_cambios}")
print(f"Conflictos registrados: {reporte_conflictos}")
