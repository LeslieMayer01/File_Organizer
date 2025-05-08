import os
import re
import unicodedata
from datetime import datetime
import csv

def cargar_diccionario_csv(ruta_csv):
    diccionario = set()
    with open(ruta_csv, mode='r', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)  # Omitir el encabezado
        for fila in lector:
            if fila:  # Verifica que la fila no esté vacía
                diccionario.add(fila[0].strip().lower())  # Convertir a minúsculas y agregar al diccionario
    return diccionario

# Un diccionario simple de palabras en español (deberías usar uno más completo en la práctica)
diccionario_palabras = cargar_diccionario_csv('diccionario.csv')

def capitalizar_palabras(texto, diccionario):
    # Utiliza una expresión regular para dividir el texto en posibles palabras
    posibles_palabras = re.findall(r'[a-z]+', texto)
    
    partes = []
    i = 0
    while i < len(texto):
        # Encuentra la primera posible palabra en el texto
        for j in range(i + 1, len(texto) + 1):
            palabra = texto[i:j]
            if palabra in diccionario:
                partes.append(capitalizar_primera_letra(palabra))
                i = j
                break
        else:
            # Si no se encuentra una palabra válida, agrega el carácter y avanza
            partes.append(texto[i])
            i += 1

    # Une las partes en el texto modificado
    texto_modificado = ''.join(partes)
    
    return texto_modificado

def convertir_upper_camel_case(nombre):
    # Convertir a Upper Camel Case (Primera letra de cada palabra en mayúsculas, el resto en minúsculas)
    palabras = nombre.split()
    if len(palabras) == 1:
        return nombre
    return ''.join(capitalizar_primera_letra(palabra) for palabra in palabras)

def eliminar_caracteres_especiales(nombre):
    # Eliminar caracteres especiales y espacios
    nombre = re.sub(r'[^a-zA-Z0-9]', '', nombre)
    return nombre

def reemplazar_vocales_con_tilde(nombre):
    # Reemplazar vocales con tilde por vocales sin tilde
    trans_tabla = str.maketrans("áéíóúÁÉÍÓÚ", "aeiouAEIOU")
    return nombre.translate(trans_tabla)

def recortar_a_40_caracteres(nombre):
    # Recortar el nombre a 40 caracteres si es necesario
    return nombre[:40] if len(nombre) > 40 else nombre

def eliminar_palabras(nombre):
    # Eliminar palabras no deseadas
    palabras_a_eliminar = ['de', 'por', 'para', 'el', 'la', 'los']
    palabras = nombre.split()
    nombre_filtrado = [palabra for palabra in palabras if palabra.lower() not in palabras_a_eliminar]
    return ' '.join(nombre_filtrado)

def agregar_cero_si_digito_simple(nombre):
    # Verifica si el nombre comienza con un solo dígito
    match = re.match(r'^(\d)([a-zA-Z].*)', nombre)
    if match:
        # Si es un dígito simple, añadir un 0 antes
        return f'0{match.group(1)}{match.group(2)}'
    return nombre

def formatear_fechas(nombre):
    # Formatear fechas en formato AAAAMMDD (busca y transforma fechas del estilo DD-MM-AAAA o similares)
    regex_fecha = re.compile(r'(\b\d{1,2})[-/](\d{1,2})[-/](\d{2,4})\b')
    
    def reemplazo_fecha(match):
        dia, mes, año = match.groups()
        if len(año) == 2:
            año = '20' + año  # Asume que las fechas son de este siglo si son de dos dígitos
        dia = dia.zfill(2)
        mes = mes.zfill(2)
        return f'{año}{mes}{dia}'
    
    return regex_fecha.sub(reemplazo_fecha, nombre)

def capitalizar_primera_letra(nombre):
    # Buscar la primera letra que sea alfabética
    match = re.search(r'[a-zA-Z]', nombre)
    
    if match:
        pos = match.start()  # Obtener la posición de la primera letra
        # Si no es mayúscula, convertirla
        if not nombre[pos].isupper():
            # Capitalizar la letra encontrada y reconstruir el string
            nombre = nombre[:pos] + nombre[pos].upper() + nombre[pos+1:]
    
    return nombre

def procesar_nombre_archivo(nombre):
    nombre_sin_extension, extension = os.path.splitext(nombre)  # Separar nombre de archivo y extensión
    nombre_sin_extension = convertir_upper_camel_case(nombre_sin_extension)
    nombre_sin_extension = eliminar_palabras(nombre_sin_extension)
    nombre_sin_extension = reemplazar_vocales_con_tilde(nombre_sin_extension)
    nombre_sin_extension = eliminar_caracteres_especiales(nombre_sin_extension)
    nombre_sin_extension = recortar_a_40_caracteres(nombre_sin_extension)
    nombre_sin_extension = agregar_cero_si_digito_simple(nombre_sin_extension)
    nombre_sin_extension = formatear_fechas(nombre_sin_extension)
    nombre_sin_extension = capitalizar_primera_letra(nombre_sin_extension)
    nombre_sin_extension = capitalizar_palabras(nombre_sin_extension, diccionario_palabras)
    return nombre_sin_extension + extension

def renombrar_archivos_recursivamente(ruta):
    conflictos = []  # Lista para almacenar los conflictos
    
    for dirpath, dirnames, filenames in os.walk(ruta):
        for filename in filenames:
            nombre_procesado = procesar_nombre_archivo(filename)
            origen = os.path.join(dirpath, filename)
            destino = os.path.join(dirpath, nombre_procesado)
            #and os.path.exists(destino) == False
            if filename != nombre_procesado:
                print("Antes: "+ filename)
                print("Despues: "+ nombre_procesado)
                print("--------")
                # Renombrar el archivo si no existe un conflicto
                os.rename(origen, destino)
                print(f"Renombrado Origen: {origen} -> {destino}")
                print(f"Renombrado Destino: {destino}")
                conflictos.append({
                    'Estado': "ACTUALIZADO",
                    'Archivo Original': filename,
                    'Nombre Nuevo': nombre_procesado,
                    'Ruta Original': origen,
                    'Ruta Nuevo': destino
                })                
            else:
                # Agregar a la lista de conflictos si el archivo de destino ya existe
                conflictos.append({
                    'Estado': "CONFLICTO",
                    'Archivo Original': filename,
                    'Nombre Nuevo': nombre_procesado,
                    'Ruta Original': origen,
                    'Ruta Nuevo': destino
                })

    # Escribir los conflictos en el archivo CSV si hay alguno
    if conflictos:
        with open('./reports/03_Manual_Files_To_Check_3.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Estado','Archivo Original', 'Nombre Nuevo', 'Ruta Original', 'Ruta Nuevo']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for conflicto in conflictos:
                writer.writerow(conflicto)
        print("Archivo CSV de conflictos creado: Manual_Files_To_Check.csv")

def agregar_prefijo_si_un_solo_archivo_recursivo(ruta_carpeta):
    for dirpath, dirnames, filenames in os.walk(ruta_carpeta):  # Buscar recursivamente
        archivos = [f for f in filenames if os.path.isfile(os.path.join(dirpath, f))]
        
        # Comprobar si hay solo un archivo en el directorio actual
        if len(archivos) == 1:
            archivo = archivos[0]
            
            # Validar si los dos primeros caracteres no son números
            if not archivo[:2].isdigit():
                nombre_nuevo = '01' + archivo
                ruta_original = os.path.join(dirpath, archivo)
                ruta_nueva = os.path.join(dirpath, nombre_nuevo)
                
                # Renombrar el archivo agregando '01' al principio
                os.rename(ruta_original, ruta_nueva)
                print(f"Archivo renombrado: {ruta_original} -> {ruta_nueva}")
            else:
                print(f"")
        else:
            print(f"")

# Ejemplo de uso:
ruta_principal = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS'
renombrar_archivos_recursivamente(ruta_principal)
#agregar_prefijo_si_un_solo_archivo_recursivo(ruta_principal)
