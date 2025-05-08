# Buscar recursivamente todos los archivos
# Al entrar a una carpeta que contenga archivos, crear un arreglo con el siguiente diccionaro que contiene 
# la información de cada archivo excluyendo los archivos que se llamen zcontroldepagos:
# {"nombre_actual": prueba1.pdf, "nombre_nuevo": "", "fecha_modificacion": "23/14/2024 4:51 pm"}
# Una vez construido el arreglo con la información de todos los archivos de una carpeta
# organizarlos desde el más antiguo al más reciente por la fecha de modificación
# En el caso de que todos tengan la misma fecha de modificacion omitirlos y marcarlos con estado OMITIDO en el archivo Excel
# Por cada elemento del arreglo, asignarle el valor de "nombre_nuevo" con el nombre del archivo eliminando los numeros que contenga al principio antes de la primera letra.
# Luego añadirle el consecutivo de la posición en la que se encuentan en el arreglo iniciando con 1 y añadiendole el 0 para los números entre 1 y 9, ejm 01, 02, 03
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
from datetime import datetime

def añadir_fecha_y_hora_al_nombre(archivo):
    fecha_hora_actual = datetime.now().strftime('%d-%m-%Y_%H-%M')
    nombre, extension = os.path.splitext(archivo)
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    return nuevo_nombre


def procesar_archivos(base_dir):
    archivos_info = []

    # Buscar recursivamente archivos
    for root, dirs, files in os.walk(base_dir):
        # Filtrar archivos excluyendo "controldepago"
        archivos_validos = [f for f in files if "controldepago" not in f.lower()]

        if archivos_validos:
            # Inicializar índice para cada subcarpeta
            index = 1
            
            for archivo in archivos_validos:
                ruta_archivo = os.path.join(root, archivo)
                fecha_modificacion = os.path.getmtime(ruta_archivo)
                archivos_info.append({
                    "nombre_actual": archivo,
                    "fecha_modificacion": datetime.fromtimestamp(fecha_modificacion),
                    "ruta": ruta_archivo,
                    "estado": "RENOMBRADO"
                })

            # Procesar nombres nuevos por subcarpeta
            for archivo in archivos_info[-len(archivos_validos):]:  # Solo los archivos de esta subcarpeta
                # Eliminar números del principio del nombre actual
                nombre_sin_numeros = re.sub(r'^\d+', '', archivo["nombre_actual"]).lstrip('.')
                
                # Crear nuevo nombre manteniendo la extensión
                nombre_nuevo = f"{index:02d}{nombre_sin_numeros}"
                archivo["nombre_nuevo"] = nombre_nuevo
                
                # Renombrar archivo
                nueva_ruta = os.path.join(root, nombre_nuevo)
                os.rename(archivo["ruta"], nueva_ruta)
                archivo["ruta"] = nueva_ruta
                
                # Incrementar el índice
                index += 1

    # Crear DataFrame para exportar a Excel
    df = pd.DataFrame([
        {
            "NOMBRE_ANTERIOR": archivo["nombre_actual"],
            "NOMBRE_NUEVO": archivo.get("nombre_nuevo", ""),
            "ESTADO": archivo["estado"],
            "RUTA": archivo["ruta"]
        } for archivo in archivos_info
    ])

    reporte_excel = "./reports/10_" + añadir_fecha_y_hora_al_nombre("Add_Consecutive_Preffix.xlsx")
    df.to_excel(reporte_excel, index=False)

# Cambia 'ruta/base/del/directorio' por la ruta que quieras analizar
procesar_archivos('D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES\2018\05631408900120180024100')

