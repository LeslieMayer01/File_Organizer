# Iterar recursivamente
# Buscar carpetas que contengan en el nombre alguna de las siguientes palabras: principal | Principal | ppal | PRINCIPAL | Ppal | PPAL
# Renonmbrarla como C01Principal

# Buscar carpetas que contengan en el nombre alguna de las siguientes palabras: medida | Medida | MEDIDA | MC | Mc | mc
# Renombrarla como C05MedidasCautelares

import os
import re
import pandas as pd
from datetime import datetime

def renombrar_carpetas(ruta_base, archivo_excel):
    # Palabras clave para identificar las carpetas "Principal"
    palabras_principal = ['principal', 'Principal', 'ppal', 'PPAL', 'Ppal', 'PRINCIPAL', 'CuadernoUnico', '01.Expediente Restitutucion 056314089001201800150  ST', '01 Unica Instancia']
    
    # Palabras clave para identificar las carpetas "Medidas Cautelares"
    palabras_medidas = ['medida', 'Medida', 'MEDIDA', 'M.C', 'M. Cautelar', 'Media Cautelar', 'MS', 'Medias Cautelares', 'MEDIDA CAUTELAR']

    # Palabras clave para identificar las carpetas "Acumulación"
    palabras_acumulacion = ['acumulacion', 'ACUMULACION', 'Acumulacion']

    # Palabras clave para identificar las carpetas "Depositos"
    palabras_titulos = ['deposito', 'titulo', 'TITULO' 'Deposito' 'DEPOSITOS' 'Titulo', 'DJ04']
    
    # Lista para almacenar la información que se escribirá en el Excel
    datos_renombrados = []
    
    # Iterar recursivamente por las carpetas
    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            nuevo_nombre = None
            estado = ""

            if dir_name.startswith("056314"):
                continue
            
            # Omite las carpetas que ya tienen el nombre correcto
            if dir_name in ['C01Principal', 'C05MedidasCautelares', 'C03AcumulacionProcesos', 'C04DepositosJudiciales']:
                continue
            
            # Verificar si el nombre de la carpeta contiene una palabra clave para "Principal"
            if any(palabra in dir_name for palabra in palabras_principal):
                nuevo_nombre = 'C01Principal'
                
            # Verificar si el nombre de la carpeta contiene una palabra clave para "Medidas Cautelares"
            elif any(palabra in dir_name for palabra in palabras_medidas):
                nuevo_nombre = 'C05MedidasCautelares'

            elif any(palabra in dir_name for palabra in palabras_acumulacion):
                nuevo_nombre = 'C03AcumulacionProcesos'

            elif any(palabra in dir_name for palabra in palabras_titulos):
                nuevo_nombre = 'C04DepositosJudiciales'

            
            # Si se detectó que se debe renombrar
            if nuevo_nombre:
                ruta_antigua = os.path.join(root, dir_name)
                ruta_nueva = os.path.join(root, nuevo_nombre)
                
                # Verificar si ya existe una carpeta con el nuevo nombre
                if os.path.exists(ruta_nueva):
                    estado = "DUPLICADA"
                    print(f"No se renombró {dir_name} porque ya existe {nuevo_nombre}")
                else:
                    try:
                        os.rename(ruta_antigua, ruta_nueva)
                        estado = "RENOMBRADA"
                        print(f"Carpeta renombrada: {dir_name} a {nuevo_nombre}")
                    except Exception as e:
                        estado = f"ERROR: {e}"
            
                # Agregar la información al archivo Excel
                datos_renombrados.append({
                    'Nombre Anterior': dir_name,
                    'Nombre Nuevo': nuevo_nombre,
                    'Estado': estado,
                    'Ruta Absoluta': ruta_antigua if estado == "DUPLICADA" else ruta_nueva
                })
    
    # Crear el DataFrame con los datos recolectados
    df = pd.DataFrame(datos_renombrados, columns=['Nombre Anterior', 'Nombre Nuevo', 'Estado', 'Ruta Absoluta'])
    
    # Guardar los datos en el archivo Excel
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
    # Obtiene la fecha actual
    fecha_actual = datetime.now().strftime('%d-%m-%Y')
    
    # Separa el nombre del archivo y la extensión
    nombre, extension = os.path.splitext(archivo)
    
    # Crea el nuevo nombre con la fecha al inicio
    nuevo_nombre = f"{fecha_actual}-{nombre}{extension}"
    
    return nuevo_nombre

# Uso de la función
#re.search(r'\b' + palabra + r'\b', dir_name)
ruta_directorio = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES'
archivo_excel = "./reports/04_"+ añadir_fecha_y_hora_al_nombre("Create_Folder_Report.xlsx")
renombrar_carpetas(ruta_directorio, archivo_excel)
