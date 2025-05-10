import os
import pandas as pd
from datetime import datetime

# Función para crear la carpeta 01PrimeraInstancia
def crear_carpeta_principal(ruta_base, archivo_excel, solo_reporte=False):
    datos_carpetas = []

    # Iterar recursivamente por todas las carpetas en el directorio base
    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            # Ruta completa de la carpeta actual
            ruta_carpeta = os.path.join(root, dir_name)

            # Verificar si el nombre de la carpeta comienza con "053804"
            if dir_name.startswith("053804"):
                # Verificar si no existe 01PrimeraInstancia o 01UnicaInstancia
                if not os.path.exists(os.path.join(ruta_carpeta, '01PrimeraInstancia')) and not os.path.exists(os.path.join(ruta_carpeta, '01UnicaInstancia')):
                    nueva_carpeta = "01PrimeraInstancia"
                    nueva_ruta = os.path.join(ruta_carpeta, nueva_carpeta)

                    if not solo_reporte:
                        # Crear la carpeta 01PrimeraInstancia si no existe
                        os.mkdir(nueva_ruta)
                        estado = 'CREADA'
                        print(f"Carpeta 01PrimeraInstancia creada en: {nueva_ruta}")
                    else:
                        estado = 'A CREAR'

                    # Registrar la acción en los datos
                    datos_carpetas.append({
                        'Estado': estado,
                        'Ruta': nueva_ruta
                    })

    # Crear un DataFrame con los datos recolectados
    df = pd.DataFrame(datos_carpetas, columns=['Estado', 'Ruta'])

    # Guardar los datos en un archivo Excel
    df.to_excel(archivo_excel, index=False)
    print(f"Datos guardados en {archivo_excel}")


# Función para renombrar las carpetas
def renombrar_carpetas(ruta_base, archivo_excel, solo_reporte=False):
    # Palabras clave para identificar las carpetas
    palabras_principal = ['principal', 'Principal', 'ppal', 'PPAL', 'Ppal', 'PRINCIPAL', 'CuadernoUnico', '01.Expediente Restitutucion 056314089001201800150  ST', '01 Unica Instancia']
    palabras_medidas = ['medida', 'Medida', 'MEDIDA', 'M.C', 'M. Cautelar', 'Media Cautelar', 'MS', 'Medias Cautelares', 'MEDIDA CAUTELAR']
    palabras_acumulacion = ['acumulacion', 'ACUMULACION', 'Acumulacion']
    palabras_titulos = ['deposito', 'titulo', 'TITULO', 'Deposito', 'DEPOSITOS', 'Titulo', 'DJ04']
    palabras_incidentes = ['indidente', 'incidentes', 'INCIDENTE', ' Incidente', 'Incidentes', 'INCIDENTES']

    # Lista para almacenar la información que se escribirá en el Excel
    datos_renombrados = []
    
    # Iterar recursivamente por las carpetas
    for root, dirs, files in os.walk(ruta_base):
        for dir_name in dirs:
            nuevo_nombre = None
            estado = ""

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

            elif any(palabra in dir_name for palabra in palabras_incidentes):
                nuevo_nombre = 'C02Incidentes'

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
                        if not solo_reporte:
                            os.rename(ruta_antigua, ruta_nueva)
                            estado = "RENOMBRADA"
                            print(f"Carpeta renombrada: {dir_name} a {nuevo_nombre}")
                        else:
                            estado = "A RENOMBRAR"
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

# Función para añadir la fecha y hora al nombre del archivo
def añadir_fecha_y_hora_al_nombre(archivo):
    fecha_hora_actual = datetime.now().strftime('%d-%m-%Y_%H-%M')
    nombre, extension = os.path.splitext(archivo)
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    return nuevo_nombre

# Ruta base y archivo para reporte
ruta_directorio = r'C:\Users\Usuario\Downloads\Proyectos\J1'
archivo_creacion = "./reports/01_" + añadir_fecha_y_hora_al_nombre("Reporte_Creacion_Carpeta.xlsx")
archivo_renombrado = "./reports/02_" + añadir_fecha_y_hora_al_nombre("Reporte_Renombrado_Carpeta.xlsx")

# Llamada a las funciones
# Para solo generar reporte de la primera parte (creación de carpetas)
crear_carpeta_principal(ruta_directorio, archivo_creacion, solo_reporte=True)

# Para solo generar reporte de las carpetas que se renombrarían sin aplicar cambios
renombrar_carpetas(ruta_directorio, archivo_renombrado, solo_reporte=True)

