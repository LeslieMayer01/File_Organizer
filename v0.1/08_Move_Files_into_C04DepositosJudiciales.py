import os
import shutil
from openpyxl import Workbook
from datetime import datetime


def mover_archivos_056314(ruta_base, reporte_excel):
    # Crear un libro de trabajo (workbook) y una hoja (worksheet)
    wb = Workbook()
    ws = wb.active
    ws.title = "Reporte Movimientos"

    # Escribir la cabecera del reporte
    ws.append(["Nombre del archivo", "Estado", "Ruta Anterior", "Nueva Ruta"])

    # Recorrer todas las carpetas y subcarpetas recursivamente
    for dirpath, dirnames, filenames in os.walk(ruta_base):
        # Verificar si la carpeta comienza con '056314'
        nombre_carpeta = os.path.basename(dirpath)
        if nombre_carpeta.startswith("056314"):
            # Definir rutas para 'C01Principal' y 'C04DepositosEspeciales' dentro de la misma carpeta '056314'
            ruta_c01_principal = os.path.join(
                dirpath, "01PrimeraInstancia", "C01Principal"
            )
            ruta_c04_depositos = os.path.join(
                dirpath, "01PrimeraInstancia", "C04DepositosJudiciales"
            )

            # Verificar si la carpeta C01Principal existe
            if os.path.exists(ruta_c01_principal):
                # Si la carpeta C04DepositosEspeciales no existe, crearla
                if not os.path.exists(ruta_c04_depositos):
                    os.makedirs(ruta_c04_depositos)

                # Recorrer los archivos en C01Principal
                for archivo in os.listdir(ruta_c01_principal):
                    # Verificar si el nombre del archivo contiene alguno de los strings: 'deposito', 'titulo', 'controldepago' (en minúsculas o mayúsculas)
                    if any(
                        substring in archivo.lower()
                        for substring in ["deposito", "titulo", "controldepago"]
                    ):
                        archivo_origen = os.path.join(ruta_c01_principal, archivo)
                        archivo_destino = os.path.join(ruta_c04_depositos, archivo)

                        # Comprobar que no haya un archivo con el mismo nombre en la carpeta destino
                        if not os.path.exists(archivo_destino):
                            # Mover el archivo
                            shutil.move(archivo_origen, archivo_destino)
                            estado = "Movido"
                        else:
                            estado = "Omitido"

                        # Agregar la fila al reporte en Excel
                        ws.append([archivo, estado, archivo_origen, archivo_destino])
            else:
                print(f"La carpeta C01Principal no existe en {dirpath}")

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
ruta_principal = r"C:\Users\LESLIE CRUZ\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DIGITALIZADOS DESDE JUNIO 2020"  # Cambia esta ruta por la que desees analizar
reporte_excel = "./reports/08_" + añadir_fecha_y_hora_al_nombre(
    "Move_Files_Into_C04DepositosJudiciales.xlsx"
)
mover_archivos_056314(ruta_principal, reporte_excel)
