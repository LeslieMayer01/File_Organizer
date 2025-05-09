# Buscar las carpetas que empiecen por 056314
# Valida si existe una carpeta que se llame 01UnicaInstancia, y en caso de que si, renombrarla a 01PrimeraInstancia
# En caso de que no exista una carpeta llamada 01PrimeraInstancia crear una carpeta que se llame 01PrimeraInstancia

import os
import pandas as pd
from datetime import datetime

def procesar_carpeta_instancia(ruta_base, archivo_excel):
    datos_carpetas = []

    # Iterar recursivamente por todas las carpetas en el directorio base
    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            if dir_name.startswith('056314'):
                ruta_carpeta = os.path.join(root, dir_name)
                ruta_unica_instancia = os.path.join(ruta_carpeta, '01UnicaInstancia')
                ruta_primera_instancia = os.path.join(ruta_carpeta, '01PrimeraInstancia')
                
                if os.path.exists(ruta_unica_instancia):
                    # Si existe 01UnicaInstancia, renombrarla a 01PrimeraInstancia
                    if not os.path.exists(ruta_primera_instancia):
                        os.rename(ruta_unica_instancia, ruta_primera_instancia)
                        estado = 'RENOMBRADA'
                        nombre_previo = '01UnicaInstancia'
                        nombre_nuevo = '01PrimeraInstancia'
                        print(f"Carpeta renombrada: {ruta_unica_instancia} a {ruta_primera_instancia}")
                    else:
                        # Si 01PrimeraInstancia ya existe, no se puede renombrar
                        estado = 'OMITIDA'
                        nombre_previo = '01UnicaInstancia'
                        nombre_nuevo = '01PrimeraInstancia'
                        print(f"No se pudo renombrar {ruta_unica_instancia}, ya existe {ruta_primera_instancia}")
                else:
                    # Si no existe 01PrimeraInstancia, crearla
                    if not os.path.exists(ruta_primera_instancia):
                        os.mkdir(ruta_primera_instancia)
                        estado = 'CREADA'
                        nombre_previo = 'NO-EXISTIA'
                        nombre_nuevo = '01PrimeraInstancia'
                        print(f"Carpeta creada: {ruta_primera_instancia}")
                    else:
                        estado = 'OMITIDA'
                        nombre_previo = 'NO-EXISTIA'
                        nombre_nuevo = '01PrimeraInstancia'
                        print(f"La carpeta {ruta_primera_instancia} ya existía, no fue necesario crearla.")
                
                # Añadir la información al registro
                datos_carpetas.append({
                    'Nombre Previo': nombre_previo,
                    'Nombre Nuevo': nombre_nuevo,
                    'Estado': estado,
                    'Ruta': ruta_primera_instancia if estado in ['CREADA', 'RENOMBRADA'] else ruta_carpeta
                })

    # Crear un DataFrame con los datos recolectados
    df = pd.DataFrame(datos_carpetas, columns=['Nombre Previo', 'Nombre Nuevo', 'Estado', 'Ruta'])

    # Guardar los datos en un archivo Excel
    df.to_excel(archivo_excel, index=False)
    print(f"Datos guardados en {archivo_excel}")


def añadir_fecha_y_hora_al_nombre(archivo):
    # Obtiene la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime('%d-%m-%Y_%H-%M')
    
    # Separa el nombre del archivo y la extensión
    nombre, extension = os.path.splitext(archivo)
    
    # Crea el nuevo nombre con la fecha y hora al inicio
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    
    return nuevo_nombre

# Uso de la función
ruta_directorio = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES'
archivo_excel = "./reports/06_"+ añadir_fecha_y_hora_al_nombre("Rename_01UnicaInstancia_Report.xlsx")
procesar_carpeta_instancia(ruta_directorio, archivo_excel)
