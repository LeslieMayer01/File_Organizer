# Buscar las carpetas que empiecen por 056314 recursivamente
# Validar que la carpeta 01PrimeraInstancia/C01Principal existe adentro
# Si la carpeta 01PrimeraInstancia/C01Principal existe mover todos los archivos que esten en la carpeta llamada 056314 a la subcarpeta 01PrimeraInstancia/C01Principal excluyendo las carpetas
# Si la carpeta 01PrimeraInstancia existe mover todos las subcarpetas que estaban dentro de la carpeta llamada 056314 dentro de la carpeta 01PrimeraInstancia
# Crear un archivo excel con la siguiente información de los cambios que se hicieron: CARPETA, NOMBRE, TIPO, ESTADO, RUTA
# La columna CARPETA contendrá el nombre completo de la carpeta que empieza por 056314
# La columna NOMBRE contendrá el nombre del archivo, o nombre de la carpeta que se movio
# La columna TIPO sera ARCHIVO o CARPETA dependiendo de la accion que se hizo
# La columna ESTADO sera MOVIDO en caso de que se haya hecho el movimiento correctamente
# La columna RUTA sera la ruta absoluta del archivo o carpeta que se movio

import os
import shutil
import pandas as pd
from datetime import datetime

def mover_archivos_carpetas(ruta_base, archivo_excel):
    datos_cambios = []

    # Iterar recursivamente por todas las carpetas en el directorio base
    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            if dir_name.startswith('056314'):
                print("Procesando: " + dir_name)
                ruta_carpeta = os.path.join(root, dir_name)
                ruta_primera_instancia = os.path.join(ruta_carpeta, '01PrimeraInstancia')
                ruta_c01_principal = os.path.join(ruta_primera_instancia, 'C01Principal')
                
                # Si existe 01PrimeraInstancia, mover subcarpetas a esa carpeta
                if os.path.exists(ruta_primera_instancia):
                    for item in os.listdir(ruta_carpeta):
                        item_path = os.path.join(ruta_carpeta, item)
                        if os.path.isdir(item_path) and item != '01PrimeraInstancia':
                            print("Moviendo Archivos")
                            nuevo_path = os.path.join(ruta_primera_instancia, item)
                            shutil.move(item_path, nuevo_path)
                            # Registrar cambio
                            datos_cambios.append({
                                'CARPETA': dir_name,
                                'NOMBRE': item,
                                'TIPO': 'CARPETA',
                                'ESTADO': 'MOVIDO',
                                'RUTA': nuevo_path
                            })
                            
                # Verificar si la carpeta 01PrimeraInstancia/C01Principal existe
                if os.path.exists(ruta_c01_principal):
                    # Mover archivos de la carpeta 056314 a 01PrimeraInstancia/C01Principal
                    print("Moviendo Archivos")
                    for item in os.listdir(ruta_carpeta):                        
                        item_path = os.path.join(ruta_carpeta, item)
                        print(item_path)
                        if os.path.isfile(item_path):
                            print("Moviendo -> "+ item)
                            nuevo_path = os.path.join(ruta_c01_principal, item)
                            shutil.move(item_path, nuevo_path)
                            # Registrar cambio
                            datos_cambios.append({
                                'CARPETA': dir_name,
                                'NOMBRE': item,
                                'TIPO': 'ARCHIVO',
                                'ESTADO': 'MOVIDO',
                                'RUTA': nuevo_path
                            })
                

    # Crear un DataFrame con los datos recolectados
    df = pd.DataFrame(datos_cambios, columns=['CARPETA', 'NOMBRE', 'TIPO', 'ESTADO', 'RUTA'])

    # Guardar los datos en un archivo Excel
    #df.to_excel(archivo_excel, index=False)
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
ruta_directorio = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS'
archivo_excel = "./reports/07_"+ añadir_fecha_y_hora_al_nombre("Moved_Files_Into_01PrimeraInstancia_Folder.xlsx")
mover_archivos_carpetas(ruta_directorio, archivo_excel)

