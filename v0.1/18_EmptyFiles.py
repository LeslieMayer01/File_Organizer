import os
from datetime import datetime
import pandas as pd


def find_empty_files(directory):
    empty_files = []

    # Recorre todos los archivos y carpetas en el directorio de manera recursiva
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Verifica si el archivo está vacío
            if os.path.getsize(file_path) == 0:
                empty_files.append({"File Name": file, "File Path": file_path})

    return empty_files


def generate_excel_report(empty_files, output_path):
    # Crea un DataFrame de pandas y lo exporta a un archivo Excel
    df = pd.DataFrame(empty_files)
    df.to_excel(output_path, index=False)


def añadir_fecha_y_hora_al_nombre(archivo):
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombre, extension = os.path.splitext(archivo)
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    return nuevo_nombre


def main():
    # Especifica la ruta del directorio que deseas revisar
    directory = r"D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS"  # Cambia esta línea con la ruta deseada
    output_excel = "./reports/18_" + añadir_fecha_y_hora_al_nombre("_Empty_Files.xlsx")

    empty_files = find_empty_files(directory)

    if empty_files:
        generate_excel_report(empty_files, output_excel)
        print(f"Reporte generado: {output_excel}")
    else:
        print("No se encontraron archivos vacíos.")


if __name__ == "__main__":
    main()
