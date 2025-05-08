import os
from datetime import datetime
import pandas as pd

import os
import pandas as pd

def encontrar_archivos_sin_extension(carpeta):
    archivos_sin_extension = []  # Lista para almacenar los archivos sin extensión

    # Recorrer recursivamente la carpeta
    for root, dirs, files in os.walk(carpeta):
        for file in files:
            # Separar el nombre del archivo y la extensión
            nombre, extension = os.path.splitext(file)
            # Verificar si la extensión está vacía
            if extension == '':
                # Agregar el nombre y la ruta a la lista
                archivos_sin_extension.append({
                    'nombre_archivo': nombre,
                    'ruta': os.path.join(root, file)
                })

    return archivos_sin_extension

def renombrar_archivos_sin_extension(archivos):
    for archivo in archivos:
        ruta_actual = archivo['ruta']
        nuevo_nombre = f"{archivo['nombre_archivo']}.pdf"  # Asigna la nueva extensión .pdf
        nueva_ruta = os.path.join(os.path.dirname(ruta_actual), nuevo_nombre)  # Nueva ruta con la nueva extensión

        try:
            os.rename(ruta_actual, nueva_ruta)  # Renombrar el archivo
            print(f"Renombrado: {ruta_actual} a {nueva_ruta}")
        except Exception as e:
            print(f"Error al renombrar {ruta_actual}: {e}")

def generar_reporte_excel(archivos, ruta_salida):
    # Crear un DataFrame de pandas a partir de la lista de archivos
    df = pd.DataFrame(archivos)
    # Guardar el DataFrame en un archivo Excel
    df.to_excel(ruta_salida, index=False)


def añadir_fecha_y_hora_al_nombre(archivo):
    fecha_hora_actual = datetime.now().strftime('%d-%m-%Y_%H-%M')
    nombre, extension = os.path.splitext(archivo)
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    return nuevo_nombre

if __name__ == "__main__":
    # Ruta de la carpeta a analizar (ajústala según tus necesidades)
    carpeta_a_recorrer = r'D:\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES'
    ruta_reporte = "./reports/17_" + añadir_fecha_y_hora_al_nombre("_Files_Without_Extensions.xlsx")

    # Encontrar archivos sin extensión
    archivos_sin_extension = encontrar_archivos_sin_extension(carpeta_a_recorrer)
    
    # Generar el reporte en Excel
    generar_reporte_excel(archivos_sin_extension, ruta_reporte)

    # Renombrar los archivos sin extensión a .pdf
    renombrar_archivos_sin_extension(archivos_sin_extension)

    print(f"Reporte generado con {len(archivos_sin_extension)} archivos sin extensión.")
