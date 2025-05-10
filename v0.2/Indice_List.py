import os
import csv


def buscar_archivos_excel_con_indice(ruta_base):
    extensiones_excel = {'.xls', '.xlsx', '.xlsm'}
    archivos_encontrados = []

    for dirpath, _, filenames in os.walk(ruta_base):
        for filename in filenames:
            nombre_normalizado = filename.lower()
            _, ext = os.path.splitext(filename)
            if "indice" in nombre_normalizado and ext.lower() in extensiones_excel:
                ruta_completa = os.path.join(dirpath, filename)
                archivos_encontrados.append((filename, ruta_completa))

    return archivos_encontrados


def guardar_csv(nombre_archivo, datos):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Nombre archivo", "Ruta"])
        for fila in datos:
            escritor.writerow(fila)


def main():
    ruta_objetivo = r'D:\OneDrive - Consejo Superior de la Judicatura\Expedientes'
    resultados = buscar_archivos_excel_con_indice(ruta_objetivo)
    guardar_csv('reporte_excel_indice.csv', resultados)
    print(f"✅ Se generó el archivo 'reporte_excel_indice.csv' con {len(resultados)} resultados.")


if __name__ == "__main__":
    main()
