# realiza un script en python, que cumpla las siguientes condiciones:

# Buscar recursivamente todos los archivos
# buscar carpetas que inicien con el string "056314"
# Ingresar verificar si en la carpeta existe un archivos con los siguientes string: "00IndiceElectronicoC01" "00IndiceElectronicoC02" "00IndiceElectronicoC03" "00IndiceElectronicoC04" o "00IndiceElectronicoC05".
# Si existen deberas modificar el archivo excel que inicie con esos string y agregar en la columna B5 los 23 primeros digitos de la carpeta padre que encontraste e inicia con 056314


import os
import re
import win32com.client as win32


# Función para modificar el valor en la celda B5 de un archivo Excel (.xlsm)
def modificar_excel_xlsm(ruta_excel, texto_celda):
    ruta_excel_absoluta = os.path.abspath(ruta_excel)  # Convertir a ruta absoluta

    if not os.path.exists(ruta_excel_absoluta):
        print(f"El archivo no existe: {ruta_excel_absoluta}")
        return  # Si no existe, simplemente retornamos

    excel = win32.Dispatch("Excel.Application")
    excel.Visible = False

    try:
        # Abre el archivo Excel
        wb = excel.Workbooks.Open(ruta_excel_absoluta)
        hoja = wb.Sheets(1)  # Acceder a la primera hoja

        # Asegurar que la celda B5 esté en formato texto
        hoja.Range("B5").NumberFormat = "@"  # El "@" asegura que sea formato texto

        # Modifica la celda B5
        hoja.Range("B5").Value = texto_celda

        # Guarda el archivo (mantiene formato .xlsm)
        wb.Save()
        wb.Close(False)
        print(
            f"Archivo modificado: {ruta_excel_absoluta}, nuevo valor en B5: {texto_celda}"
        )
    except Exception as e:
        print(f"Error al abrir el archivo: {ruta_excel_absoluta} - {e}")
    finally:
        excel.Quit()


# Función para extraer los primeros 23 dígitos de una cadena
def extraer_23_digitos(nombre_carpeta):
    # Buscar solo dígitos en el nombre de la carpeta
    digitos = re.findall(r"\d", nombre_carpeta)

    # Unir los dígitos y tomar los primeros 23
    if len(digitos) >= 23:
        return "".join(digitos[:23])
    # print(f"No se encontraron suficientes dígitos en {nombre_carpeta}")
    return None


# Función para buscar archivos dentro de una carpeta y sus subcarpetas
def buscar_archivos_en_subcarpetas(carpeta, archivos_buscar, digitos_carpeta):
    for carpeta_raiz, subcarpetas, archivos in os.walk(carpeta):
        # print(f"Buscando en la carpeta: {carpeta_raiz}")
        for archivo in archivos:
            # print(f"Archivo encontrado: {archivo}")
            for archivo_buscar in archivos_buscar:
                # Usar comparaciones insensibles a mayúsculas/minúsculas
                if archivo.lower().startswith(
                    archivo_buscar.lower()
                ) and archivo.lower().endswith(".xlsm"):
                    ruta_archivo_excel = os.path.join(carpeta_raiz, archivo)
                    # Modifica el archivo Excel si lo encontramos
                    modificar_excel_xlsm(ruta_archivo_excel, digitos_carpeta)
                    print(
                        f"Archivo Excel (.xlsm) encontrado y modificado: {ruta_archivo_excel}"
                    )


# Función para buscar carpetas y archivos específicos
def buscar_y_modificar_directorios(ruta_base):
    # Recorre recursivamente todas las carpetas y archivos
    for carpeta_raiz, subcarpetas, archivos in os.walk(ruta_base):
        # print(f"Carpeta actual: {carpeta_raiz}")
        # Verifica si el nombre de la carpeta raíz comienza con "056314"
        if os.path.basename(carpeta_raiz).startswith("056314"):
            nombre_carpeta = os.path.basename(carpeta_raiz)
            # Extrae los primeros 23 dígitos
            digitos_carpeta = extraer_23_digitos(nombre_carpeta)
            print(f"Nombre de carpeta válido: {nombre_carpeta}")

            if digitos_carpeta:
                # Lista de archivos que queremos buscar
                archivos_buscar = [
                    "00IndiceElectronicoC01",
                    "00IndiceElectronicoC02",
                    "00IndiceElectronicoC03",
                    "00IndiceElectronicoC04",
                    "00IndiceElectronicoC05",
                ]

                # Llama a la función para buscar los archivos dentro de esta carpeta y sus subcarpetas
                buscar_archivos_en_subcarpetas(
                    carpeta_raiz, archivos_buscar, digitos_carpeta
                )


# Ruta base donde iniciar la búsqueda
ruta_base = r"D:\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL"

# Llamar a la función
buscar_y_modificar_directorios(ruta_base)
