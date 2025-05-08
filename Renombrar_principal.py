import os

# Define el prefijo y los strings a buscar
prefijo = "056314"
strings_a_buscar = ["escaneado", "digital", "expediente" "C01Prin"]
nuevo_nombre = "C01Principal"

# Función para buscar y renombrar carpetas
def buscar_y_renombrar(base_dir):
    for root, dirs, files in os.walk(base_dir):
        for dir_name in dirs:
            if dir_name.startswith(prefijo):
                # Carpeta encontrada que comienza con 056314
                carpeta_actual = os.path.join(root, dir_name)
                # Llamada recursiva para buscar en subcarpetas
                renombrar_subcarpetas(carpeta_actual)

def renombrar_subcarpetas(carpeta):
    for sub_dir in os.listdir(carpeta):
        ruta_subcarpeta = os.path.join(carpeta, sub_dir)
        if os.path.isdir(ruta_subcarpeta):
            # Verifica si el nombre de la subcarpeta contiene alguno de los strings buscados
            if any(string.lower() in sub_dir.lower() for string in strings_a_buscar):
                nueva_ruta = os.path.join(carpeta, nuevo_nombre)
                print("#### NUEVA RUTA")
                print(nueva_ruta)
                # Verifica si ya existe una carpeta con el nuevo nombre
                if not os.path.exists(nueva_ruta):
                    os.rename(ruta_subcarpeta, nueva_ruta)
                    ruta_subcarpeta = nueva_ruta
                    print(f"Renombrada: {ruta_subcarpeta} a {nueva_ruta}")
                else:
                    print(f"Omitida: {ruta_subcarpeta} porque {nuevo_nombre} ya existe.")
            # Llamada recursiva para buscar en subcarpetas
            renombrar_subcarpetas(ruta_subcarpeta)


# Cambia 'ruta/base/del/directorio' por la ruta que quieras analizar
buscar_y_renombrar(r'C:\Users\LESLIE CRUZ\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DIGITALIZADOS DESDE JUNIO 2020')
