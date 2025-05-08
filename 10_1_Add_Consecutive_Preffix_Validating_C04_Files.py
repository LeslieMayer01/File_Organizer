import os

def buscar_carpetas(base_dir):
    rutas_padre = []

    # Recorrer todas las carpetas y archivos en el directorio base
    for root, dirs, files in os.walk(base_dir):
        # Comprobar si la carpeta empieza con 'C04' y contiene archivos
        if os.path.basename(root).startswith("C04") and files:
            # Añadir la ruta de la carpeta padre al array
            rutas_padre.append(os.path.abspath(os.path.dirname(root)))

    return rutas_padre

# Ejemplo de uso
directorio_base = r'C:\Users\LESLIE CRUZ\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DIGITALIZADOS DESDE JUNIO 2020'
rutas = buscar_carpetas(directorio_base)
print("###################")
print("Finalizo Busqueda")

import re
import os
import pandas as pd
from datetime import datetime

def archivo_existe_y_renombra(ruta_archivo):
    if os.path.isfile(ruta_archivo):
        # Dividir el archivo en nombre y extensión
        nombre, extension = os.path.splitext(ruta_archivo)
        # Crear un nuevo nombre agregando "1" antes de la extensión
        nuevo_nombre = f"{nombre}01{extension}"
        return nuevo_nombre
    return ruta_archivo

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
                nueva_ruta = archivo_existe_y_renombra(os.path.join(root, nombre_nuevo))

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

# Imprimir las rutas encontradas
for ruta in rutas:
    print(ruta)
    procesar_archivos(ruta)


