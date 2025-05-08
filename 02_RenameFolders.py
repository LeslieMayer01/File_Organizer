import os
import shutil
import re


def needs_processing(folder_name):
    # Eliminar todos los caracteres no alfanuméricos
    processed_name = re.sub(r'[^A-Za-z0-9]', '', folder_name)

    # Extraer los números del nombre
    numbers = re.findall(r'\d+', processed_name)

    # Si no hay números o el total de dígitos numéricos no es 23, necesita procesamiento
    if not numbers or len(numbers[0]) != 23:
        return True  # Necesita ser procesada

    # Verificar si hay caracteres especiales en el nombre original
    if re.search(r'[^A-Za-z0-9\s]', folder_name):
        return True  # Tiene caracteres especiales, necesita ser procesada
    
    # Verificar si hay al menos 24 caracteres en total
    if len(processed_name) > 23:
        # Extraer la letra que sigue después de los 23 números
        letra_despues_de_numeros = processed_name[23]

        # Verificar si la letra es minúscula
        if letra_despues_de_numeros.islower():
            return True  # Necesita ser procesada porque la letra es minúscula

    # Si cumple las condiciones, devolver False
    return False


# Función para borrar el contenido de la carpeta result_01 recursivamente
def clear_target_folder(target_folder):
    if os.path.exists(target_folder):
        shutil.rmtree(target_folder)  # Borrar la carpeta completa
    os.makedirs(target_folder)  # Crear nuevamente la carpeta vacía

def restringir_cadena(texto, max_longitud=40):
    if len(texto) > max_longitud:
        return texto[:max_longitud]
    return texto

# Función para procesar el nombre de la carpeta
def process_folder_name(folder_name):
    # Eliminar caracteres especiales (dejar solo letras y números)
    processed_name = re.sub(r'[^A-Za-z0-9]', '', folder_name)

    # Separar números del nombre
    numbers = re.findall(r'\d+', processed_name)
    rest = re.sub(r'\d+', '', processed_name)

    if numbers:
        numbers = numbers[0]  # Tomar la primera secuencia de números
    else:
        numbers = ''

    # Completar los números a 23 dígitos con ceros
    if len(numbers) < 23:
        numbers = numbers.ljust(23, '0')

    # Añadir un espacio después de los números
    new_folder_name = numbers + ' ' + rest.capitalize()

    return restringir_cadena(new_folder_name)

def process_origin_folder(origin_folder, target_folder, prefix="056314"):
    for root, dirs, files in os.walk(origin_folder):
        for dir_name in dirs:
            # Si el nombre de la subcarpeta comienza con el prefijo especificado
            if dir_name.startswith(prefix) and needs_processing(dir_name):
                new_dir_name = process_folder_name(dir_name)
                os.rename(os.path.join(root, dir_name), os.path.join(root, new_dir_name))
                print("CARPETA RENOMBRADA = " + dir_name + " ===> "+ new_dir_name)
            elif dir_name.startswith(prefix):
                print("CARPETA OMITIDA = " + dir_name)


def añadir_doble_barra_invertida(texto):
    return texto.replace('\\', '\\\\')

# Ejemplo de uso
string = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES'
origin_folder = añadir_doble_barra_invertida(string)
print(origin_folder)

# Parámetros
target_folder = 'reports'  # Carpeta de destino

# Ejecutar las funciones
#clear_target_folder(target_folder)
process_origin_folder(origin_folder, target_folder)
