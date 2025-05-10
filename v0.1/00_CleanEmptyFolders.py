import os


def eliminar_carpetas_vacias_01PrimeraInstancia(ruta):
    """Elimina carpetas vacías llamadas '01PrimeraInstancia' en la ruta dada."""
    if not os.path.exists(ruta):
        print(f"La ruta {ruta} no existe o no es accesible.")
        return

    # Recorrer todas las carpetas y subcarpetas de abajo hacia arriba
    for dirpath, dirnames, filenames in os.walk(ruta, topdown=False):
        # Obtener el nombre de la carpeta actual
        nombre_carpeta = os.path.basename(dirpath)

        # Verificar si la carpeta es vacía y se llama '01PrimeraInstancia'
        if not dirnames and not filenames and nombre_carpeta == "01PrimeraInstancia":
            try:
                os.rmdir(dirpath)
                print(f"Carpeta eliminada: {dirpath}")
            except PermissionError:
                print(f"Acceso denegado para eliminar: {dirpath}")
            except OSError as e:
                print(f"No se pudo eliminar {dirpath}: {e}")


# Ejemplo de uso
ruta_principal = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DE PROCESOS JUDICIALES\CONTENCIOSOS DE MINIMA Y MENOR CUANTIA CIVIL\VIGENTES'  # Cambia esta ruta por la que quieras analizar
eliminar_carpetas_vacias_01PrimeraInstancia(ruta_principal)
