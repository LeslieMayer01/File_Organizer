import csv
import os


# Función para crear un reporte CSV
def create_csv_report(data, headers, output_dir, filename):
    """
    Crea un archivo CSV con los datos proporcionados.

    :param data: List of lists containing the rows of data for the CSV.
    :param headers: List of strings containing the header names.
    :param output_dir: Directory where the CSV file should be saved.
    :param filename: Name of the CSV file to be created.
    """
    # Aseguramos que el directorio de salida exista
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generamos la ruta completa al archivo
    file_path = os.path.join(output_dir, filename)

    try:
        # Escribimos el archivo CSV
        with open(file_path, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Escribimos los encabezados
            writer.writerows(data)  # Escribimos los datos

        print(f"Reporte generado exitosamente: {file_path}")

    except Exception as e:
        print(f"Error al generar el reporte CSV: {e}")
