import os
import csv
from collections import defaultdict

def obtener_todas_las_carpetas(ruta_base):
    """Incluye todas las carpetas, incluso las que inician por '202'."""
    carpetas = []
    for dirpath, dirnames, _ in os.walk(ruta_base):
        for dirname in dirnames:
            ruta_completa = os.path.join(dirpath, dirname)
            carpetas.append((dirname, ruta_completa))
    return carpetas

def obtener_nombres_unicos_excluyendo_202(ruta_base):
    """Incluye solo nombres únicos de carpeta, excluyendo las que empiezan por '202'."""
    nombres_unicos = {}
    for dirpath, dirnames, _ in os.walk(ruta_base):
        for dirname in dirnames:
            if dirname.startswith("202"):
                continue
            if dirname not in nombres_unicos:
                ruta_completa = os.path.join(dirpath, dirname)
                nombres_unicos[dirname] = ruta_completa
    return nombres_unicos

def contar_extensiones_archivos(ruta_base):
    """Cuenta archivos por extensión (sin importar mayúsculas/minúsculas)."""
    conteo_ext = defaultdict(int)
    for dirpath, _, filenames in os.walk(ruta_base):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            ext = ext.lstrip(".").lower() or "sin_extension"
            conteo_ext[ext] += 1
    return conteo_ext

def guardar_csv(nombre_archivo, datos, encabezados):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        for fila in datos:
            escritor.writerow(fila)

def main():
    ruta_objetivo = r'D:\OneDrive - Consejo Superior de la Judicatura\Expedientes'

    # Reporte 1: Todas las carpetas
    carpetas_todas = obtener_todas_las_carpetas(ruta_objetivo)
    guardar_csv('reporte_todas_carpetas.csv', carpetas_todas, ["nombre carpeta", "ruta"])

    # Reporte 2: Nombres únicos sin carpetas '202*'
    carpetas_unicas = obtener_nombres_unicos_excluyendo_202(ruta_objetivo)
    guardar_csv('reporte_nombres_unicos.csv', carpetas_unicas.items(), ["nombre carpeta", "ruta"])

    # Reporte 3: Extensiones de archivos
    extensiones = contar_extensiones_archivos(ruta_objetivo)
    guardar_csv('reporte_extensiones.csv', extensiones.items(), ["extension_archivo", "cantidad"])

    print("✅ Reportes generados correctamente:")
    print("- reporte_todas_carpetas.csv")
    print("- reporte_nombres_unicos.csv")
    print("- reporte_extensiones.csv")

if __name__ == "__main__":
    main()





