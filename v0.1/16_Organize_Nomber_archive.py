# Buscar recursivamente todos los archivos
# Al entrar a una carpeta que contenga archivos, crear un arreglo con el siguiente diccionaro que contiene
# la información de cada archivo excluyendo los archivos que se llamen zcontroldepagos:
# {"nombre_actual": prueba1.pdf, "nombre_nuevo": ""}
# Una vez construido el arreglo con la información de todos los archivos de una carpeta
# organizarlos en el mismo orden en que se encontraban en la carpeta
# En el caso de que todos los archivos esten organizados iniciando su nombre con 01, 02, 03 omitilos
# Por cada elemento del arreglo, asignarle el valor de "nombre_nuevo" con el nombre del archivo eliminando los numeros que contenga al principio antes de la primera letra.
# Luego añadirle el consecutivo de la posición en la que se encuentran en el arreglo iniciando con 1 y añadiendole el 0 para los números entre 1 y 9, ejm 01, 02, 03
# Quedando el campo "nombre_nuevo" del ejemplo 01prueba1.pdf
# Luego iterar el arreglo de diccionarios y modificar el nombre de cada archivo llamado por el campo "nombre_actual" por el nombre del campo "nombre_nuevo"
# Creando a su vez un archivo excel con la siguiente información: NOMBRE_ANTERIOR, NOMBRE_NUEVO, ESTADO, RUTA
# La columna NOMBRE_ANTERIOR contiene el nombre original del archivo
# La columna NOMBRE_NUEVO contiene el nombre procesado
# La columna ESTADO contiene los posibles valores: RENOMBRADO, OMITIDO
# La columna RUTA contiene la ruta absoluta del archivo

import re
import os
import pandas as pd


def obtener_archivos(directorio):
    archivos = []  # Lista para almacenar los archivos encontrados
    for root, _, files in os.walk(directorio):
        for file in files:
            # Excluir archivos que contengan 'zcontroldepagos' o '00indiceelectronico'
            if (
                "zcontroldepagos" in file.lower()
                or "00indiceelectronico" in file.lower()
            ):
                continue

            archivos.append(os.path.join(root, file))
    return archivos


def procesar_archivos(archivos):
    carpeta_actual = ""
    contador = 1  # Inicializa el contador
    datos_archivos = []  # Lista para almacenar los datos procesados

    for archivo in archivos:
        ruta_actual = os.path.dirname(archivo)
        nombre_actual = os.path.basename(archivo)
        nombre_sin_extension, extension = os.path.splitext(
            nombre_actual
        )  # Separar nombre y extensión

        # Reinicia el contador si cambia de carpeta
        if carpeta_actual != ruta_actual:
            carpeta_actual = ruta_actual
            contador = 1  # Reinicia la numeración para la nueva carpeta

        # Verificar si el nombre está compuesto solo de números
        if nombre_sin_extension.isdigit():
            # Si es solo números, renombrar a "digitalizado" manteniendo la extensión
            nuevo_nombre = f"{contador:02}Digitalizado{extension}"
        else:
            # Eliminar números al principio del nombre del archivo
            nombre_sin_numeros = re.sub(r"^\d+", "", nombre_actual).lstrip(".")
            nuevo_nombre = f"{contador:02}{nombre_sin_numeros}"  # Crea el nuevo nombre

        # Verificar si el archivo ya existe y generar un nuevo nombre si es necesario
        base_nuevo_nombre = nuevo_nombre  # Guarda la base del nuevo nombre
        consecutivo = 1  # Inicializa el contador para los nombres duplicados

        # Bucle para verificar la existencia del archivo
        while os.path.exists(os.path.join(ruta_actual, nuevo_nombre)):
            nuevo_nombre = f"{base_nuevo_nombre[:-len(extension)]}{consecutivo}{extension}"  # Añadir consecutivo antes de la extensión
            consecutivo += 1  # Incrementar el contador

        # Agregar información del archivo a la lista
        datos_archivos.append(
            {
                "nombre_actual": nombre_actual,
                "nombre_nuevo": nuevo_nombre,
                "estado": "RENOMBRADO",  # Por defecto, consideramos que será renombrado
                "ruta": archivo,
            }
        )

        contador += 1  # Incrementa el contador para el próximo archivo

    return datos_archivos


def renombrar_archivos(datos_archivos):
    for archivo in datos_archivos:
        ruta_actual = archivo["ruta"]
        nuevo_nombre = archivo["nombre_nuevo"]
        nueva_ruta = os.path.join(os.path.dirname(ruta_actual), nuevo_nombre)

        # Renombrar el archivo
        os.rename(ruta_actual, nueva_ruta)
        archivo["ruta"] = nueva_ruta  # Actualiza la ruta en el diccionario


def generar_excel(datos_archivos, directorio):
    # Crea el DataFrame y exporta a Excel
    df = pd.DataFrame(datos_archivos)
    archivo_excel = os.path.join("./reports/reporte_archivos.xlsx")
    df.to_excel(archivo_excel, index=False)


def main(directorio):
    archivos = obtener_archivos(directorio)
    if not archivos:
        print("No se encontraron archivos para procesar.")
        return

    datos_archivos = procesar_archivos(archivos)
    renombrar_archivos(datos_archivos)
    generar_excel(datos_archivos, directorio)


# Llama a la función principal con el directorio base
directorio_base = r"D:\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES"
# directorio_base = './origin'
main(directorio_base)
