# Buscar todas las carpetas recursivamente que empiecen por 056314
# Crear adentro una carpeta llamada C01Principal si no existe

import os
import pandas as pd
from datetime import datetime


def crear_carpeta_principal(ruta_base, archivo_excel):
    datos_carpetas = []

    # Iterar recursivamente por todas las carpetas en el directorio base
    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            # Ruta completa de la carpeta actual
            ruta_carpeta = os.path.join(root, dir_name)

            # Verificar si el nombre de la carpeta comienza con "Cuaderno" o "PROCESO"
            if dir_name.startswith("Cuaderno") or dir_name.startswith("C01PrimeraInst"):
                nueva_carpeta = "C01Principal"
                nueva_ruta = os.path.join(root, nueva_carpeta)

                # Si existe una carpeta con el nombre "C01PrimeraInst", agregar sufijo
                contador = 1
                while os.path.exists(nueva_ruta):
                    nueva_carpeta = f"C01Principal"
                    nueva_ruta = os.path.join(root, nueva_carpeta)
                    contador += 1

                # Renombrar la carpeta
                os.rename(ruta_carpeta, nueva_ruta)
                ruta_carpeta = nueva_ruta  # Actualizar ruta de carpeta
                print(f"Renombrada: '{dir_name}' a '{nueva_carpeta}'")

            # Proceder a crear la carpeta 'C01Principal' dentro de la carpeta que comienza con '056314'
            if dir_name.startswith("056314"):
                ruta_c01principal = os.path.join(ruta_carpeta, "C01Principal")

                if not os.path.exists(ruta_c01principal):
                    # Crear la carpeta C01Principal
                    os.mkdir(ruta_c01principal)
                    estado = "CREADA"
                    print(f"Carpeta C01Principal creada en: {ruta_c01principal}")
                else:
                    estado = "OMITIDA"
                    print(f"La carpeta C01Principal ya existía en: {ruta_c01principal}")

                # Añadir la información al registro
                datos_carpetas.append({"Estado": estado, "Ruta": ruta_c01principal})

    # Crear un DataFrame con los datos recolectados
    df = pd.DataFrame(datos_carpetas, columns=["Estado", "Ruta"])

    # Guardar los datos en un archivo Excel
    df.to_excel(archivo_excel, index=False)
    print(f"Datos guardados en {archivo_excel}")


def añadir_fecha_y_hora_al_nombre(archivo):
    # Obtiene la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")

    # Separa el nombre del archivo y la extensión
    nombre, extension = os.path.splitext(archivo)

    # Crea el nuevo nombre con la fecha y hora al inicio
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"

    return nuevo_nombre


# Uso de la función
ruta_directorio = r"D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES"
archivo_excel = "./reports/05_" + añadir_fecha_y_hora_al_nombre(
    "Create_C01_Principal_Folder_Report.xlsx"
)
crear_carpeta_principal(ruta_directorio, archivo_excel)
