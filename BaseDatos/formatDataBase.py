import pandas as pd
import os

def modificar_columna_b(ruta_excel):
    # Leer el archivo Excel en un DataFrame
    df = pd.read_excel(ruta_excel)
    
    # Verificar si la columna B existe
    if df.columns[1] != 'B':
        print("Modificando la segunda columna (B)")
    
    # Modificar la columna B
    df.iloc[:, 1] = df.iloc[:, 1].astype(str)  # Convertir los datos a string por si acaso
    df.iloc[:, 1] = df.iloc[:, 1].str.replace('-', '')  # Eliminar los guiones medios
    df.iloc[:, 1] = '056314089001' + df.iloc[:, 1] + '00'  # Añadir el prefijo y el sufijo

    # Crear el nombre para la copia
    directorio, nombre_archivo = os.path.split(ruta_excel)
    nombre_copia = 'copia_' + nombre_archivo
    ruta_copia = os.path.join(directorio, nombre_copia)

    # Guardar la copia modificada en un nuevo archivo Excel
    df.to_excel(ruta_copia, index=False, header=False)

    print(f"Copia creada con éxito: {ruta_copia}")

# Ejemplo de uso
ruta_archivo = './Archivo.xlsx'
modificar_columna_b(ruta_archivo)
