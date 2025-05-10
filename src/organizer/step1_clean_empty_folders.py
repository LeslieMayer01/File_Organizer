from datetime import datetime
import os
import csv


def run():
    print("🧹 Step 1: Cleaning empty folders...")
    ruta_a_organizar = r"C:\Users\Usuario\Downloads\Proyectos\J1"
    base_path_reportes = "./reports/"

    # Generación del nombre del archivo CSV con la fecha y hora
    ruta_csv_salida = obtener_nombre_reporte(
        base_path_reportes, "listado_indices_excel"
    )
    reporte_eliminaciones = obtener_nombre_reporte(
        base_path_reportes, "reporte_eliminaciones"
    )

    # Variable de control: Si es True, realiza eliminaciones; si es False,
    # solo genera el reporte.
    ejecutar_eliminaciones = (
        # Cambia esto a False si solo deseas generar el
        # reporte sin eliminar nada
        True
    )

    # Ejecutar las funciones
    listar_indices_excel(ruta_a_organizar, ruta_csv_salida)
    eliminar_indices_electronicos_y_carpetas_vacias(
        ruta_a_organizar, reporte_eliminaciones, ejecutar_eliminaciones
    )


def es_excel(nombre_archivo):
    """
    Verifica si el archivo tiene extensión Excel (.xls, .xlsx).
    """
    data = [".xls", ".xlsx"]
    return any(nombre_archivo.lower().endswith(ext) for ext in data)


def contiene_indice(nombre):
    """
    Verifica si el nombre del archivo o carpeta contiene 'indice'
    (sin importar mayúsculas/minúsculas).
    """
    return "indice" in nombre.lower()


def obtener_nombre_reporte(base_path, prefijo):
    """Genera el nombre del archivo CSV con fecha y hora."""
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return os.path.join(base_path, f"{prefijo}_{fecha_hora}.csv")


def listar_indices_excel(ruta, salida_csv):
    """
    Lista archivos Excel que contienen 'indice' en el nombre y
    los guarda en un CSV.
    """
    resultados = []
    for dirpath, _, filenames in os.walk(ruta):
        for archivo in filenames:
            if es_excel(archivo) and contiene_indice(archivo):
                ruta_completa = os.path.join(dirpath, archivo)
                resultados.append([ruta_completa])

    with open(salida_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Ruta del archivo"])
        writer.writerows(resultados)

    print(f"Se guardaron {len(resultados)} archivos en {salida_csv}")


def eliminar_indices_electronicos_y_carpetas_vacias(
    ruta, reporte_csv, ejecutar_eliminaciones=False
):  # CAMBIAR A TRUE PARA EJECUTAR ELIMINACIÓN
    """
    Elimina archivos Excel con 'indice' en el nombre y carpetas vacías
    en la ruta, o solo genera el reporte si no se ejecutan las eliminaciones.
    """
    eliminados = []

    for dirpath, _, filenames in os.walk(ruta, topdown=False):
        # Eliminar archivos Excel con 'indice' en el nombre
        for archivo in filenames:
            if es_excel(archivo) and contiene_indice(archivo):
                ruta_archivo = os.path.join(dirpath, archivo)
                if ejecutar_eliminaciones:
                    try:
                        os.remove(ruta_archivo)
                        print(f"Archivo Excel eliminado: {ruta_archivo}")
                    except Exception as e:
                        print(f"No se pudo eliminar {ruta_archivo}: {e}")
                eliminados.append(["Archivo", ruta_archivo])

        # Eliminar carpetas vacías
        if not os.listdir(dirpath):  # Si está vacía tras eliminar archivos
            if ejecutar_eliminaciones:
                try:
                    os.rmdir(dirpath)
                    print(f"Carpeta vacía eliminada: {dirpath}")
                except Exception as e:
                    print(f"No se pudo eliminar carpeta {dirpath}: {e}")
            eliminados.append(["Carpeta", dirpath])

    # Guardar el reporte de eliminaciones en un archivo CSV
    with open(reporte_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Tipo de Eliminación", "Ruta"])
        writer.writerows(eliminados)

    print(f"Reporte de eliminaciones guardado en {reporte_csv}")
