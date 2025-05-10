import os
from openpyxl import Workbook
from datetime import datetime


def generar_reporte_carpeta_faltante(ruta_base, reporte_excel):
    # Crear un libro de trabajo (workbook) y una hoja (worksheet)
    wb = Workbook()
    ws = wb.active
    ws.title = "Carpetas Faltantes C01Principal"

    # Escribir la cabecera del reporte
    ws.append(["Ruta"])

    # Recorrer todas las carpetas y subcarpetas recursivamente
    for dirpath, dirnames, filenames in os.walk(ruta_base):
        # Verificar si la carpeta comienza con '056314'
        nombre_carpeta = os.path.basename(dirpath)
        if nombre_carpeta.startswith("056314"):
            # Definir la ruta de '01PrimeraInstancia'
            ruta_primera_instancia = os.path.join(dirpath, "01PrimeraInstancia")
            ruta_c01_principal = os.path.join(ruta_primera_instancia, "C01Principal")

            # Verificar si '01PrimeraInstancia' existe y si 'C01Principal' no existe
            if os.path.exists(ruta_primera_instancia) and not os.path.exists(
                ruta_c01_principal
            ):
                # Si la carpeta C01Principal no existe, agregar la ruta al reporte
                ws.append([ruta_c01_principal])

    # Guardar el archivo Excel
    wb.save(reporte_excel)
    print(f"Reporte guardado en: {reporte_excel}")


def añadir_fecha_y_hora_al_nombre(archivo):
    # Obtiene la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")

    # Separa el nombre del archivo y la extensión
    nombre, extension = os.path.splitext(archivo)

    # Crea el nuevo nombre con la fecha y hora al inicio
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"

    return nuevo_nombre


# Ejemplo de uso
ruta_principal = r"D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS"  # Cambia esta ruta por la que desees analizar
reporte_excel = "./reports/09_" + añadir_fecha_y_hora_al_nombre(
    "Verify_Folder_C01Principal.xlsx"
)
generar_reporte_carpeta_faltante(ruta_principal, reporte_excel)
