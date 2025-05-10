# realiza un script en python, que cumpla las siguientes condiciones:

# Buscar recursivamente todos los archivos
# buscar carpetas que inicien con el string "056314"
# Cuando ingrese debe revisar que todas estas carpetas tengan la siguiente estructura de carpetas:
# 01PrimeraInstancia/C01Principal
# Si la tiene debe verificar que la carpeta C01Principal contiene el archivo son el string "00IndiceElectronicoC01"
# y que el segundo archivo comience con el string "01"
# Si la carpeta que inicia con el string "056314" no cuenta con estas caracteristicas realiza un reporte creando un archivo en excel con la siguiente información:
# ARCHIVO, ESTADO, RUTA
# La columna ARCHIVO contiene el nombre de la carpeta o el archivo que es diferente al de la instrucción 01PrimeraInstancia, C01Principal,  "00IndiceElectronicoC01" o si segundo archivo de la carpeta no comience con el string "01", que se debe nombrar como "error primer digito"
# La columna ESTADO contiene los posibles valores: si es una carpeta o un archivo
# La columna RUTA contiene la ruta absoluta del archivo

# el script deberá hacer una segunda revisión por todas las carpetas que inicien por el string "056314"
# Cuando ingrese debe revisar que todas estas carpetas tengan la siguiente estructura de carpetas:01PrimeraInstancia/C05MedidasCautelares
# Si la tiene debe verificar que la carpeta C05MedidasCautelares contiene el archivo son el string "00IndiceElectronicoC05"
# y que el segundo archivo comience con el string "01"
# Si la carpeta que inicia con el string "056314" no cuenta con estas caracteristicas realiza un reporte creando un archivo en excel con la siguiente información:
# ARCHIVO, ESTADO, RUTA
# La columna ARCHIVO contiene el nombre de la carpeta o el archivo que es diferente al de la instrucción 01PrimeraInstancia, 05MedidasCautelares,  "00IndiceElectronicoC05" o si segundo archivo de la carpeta no comience con el string "01", que se debe ingresarlo como "error primer digito"
# La columna ESTADO contiene los posibles valores: si es una carpeta o un archivo
# La columna RUTA contiene la ruta absoluta del archivo

import os
import pandas as pd


# Función para verificar estructura de carpetas y archivos
def verificar_estructura_carpeta(
    ruta, carpeta_principal, nombre_indice, segundo_archivo_str
):
    errores = []

    ruta_principal = os.path.join(ruta, carpeta_principal)

    if not os.path.exists(ruta_principal):
        errores.append((carpeta_principal, "Carpeta", ruta))
    else:
        archivos = os.listdir(ruta_principal)
        archivos.sort()  # Aseguramos que los archivos estén ordenados

        if len(archivos) < 2:
            errores.append(("Faltan archivos", "Error", ruta_principal))
        else:
            # Verificar primer archivo
            if not archivos[0].startswith(nombre_indice):
                errores.append(
                    (archivos[0], "Archivo", os.path.join(ruta_principal, archivos[0]))
                )

            # Verificar segundo archivo
            if not archivos[1].startswith(segundo_archivo_str):
                errores.append(
                    (
                        "error primer digito",
                        "Archivo",
                        os.path.join(ruta_principal, archivos[1]),
                    )
                )

    return errores


# Función para recorrer directorios y generar el reporte
def generar_reporte_directorios(ruta_base):
    reporte_errores = []

    for ruta_actual, carpetas, archivos in os.walk(ruta_base):
        for carpeta in carpetas:
            if carpeta.startswith("056314"):
                ruta_carpeta = os.path.join(ruta_actual, carpeta)

                # Revisar primera estructura: 01PrimeraInstancia/C01Principal
                reporte_errores.extend(
                    verificar_estructura_carpeta(
                        ruta_carpeta,
                        "01PrimeraInstancia/C01Principal",
                        "00IndiceElectronicoC01",
                        "01",
                    )
                )

                # Revisar segunda estructura: 01PrimeraInstancia/C05MedidasCautelares
                reporte_errores.extend(
                    verificar_estructura_carpeta(
                        ruta_carpeta,
                        "01PrimeraInstancia/C05MedidasCautelares",
                        "00IndiceElectronicoC05",
                        "01",
                    )
                )

    return reporte_errores


# Función para guardar el reporte en un archivo Excel
def guardar_reporte_excel(reporte, nombre_archivo):
    df = pd.DataFrame(reporte, columns=["ARCHIVO", "ESTADO", "RUTA"])
    df.to_excel(nombre_archivo, index=False)


# Ruta base donde buscar
ruta_base = r"D:\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES"

# Generar el reporte de errores
reporte_errores = generar_reporte_directorios(ruta_base)

# Guardar el reporte en Excel
guardar_reporte_excel(reporte_errores, "./reports/reporte_errores.xlsx")

print(f"Reporte generado con {len(reporte_errores)} errores encontrados.")
