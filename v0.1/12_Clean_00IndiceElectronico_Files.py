import os


def delete_files_by_prefix(root_folder, target_prefix):
    """
    Busca recursivamente archivos cuyos nombres empiezan con un prefijo específico y los borra.

    :param root_folder: Ruta raíz donde se iniciará la búsqueda.
    :param target_prefix: Prefijo que deben tener los nombres de los archivos a eliminar.
    """
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.startswith(target_prefix):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Archivo eliminado: {file_path}")
                except Exception as e:
                    print(f"No se pudo eliminar {file_path}. Error: {e}")


if __name__ == "__main__":
    # Especifica la ruta de la carpeta raíz y el prefijo del archivo que deseas eliminar
    folder_path = r"D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS\08 TUTELAS 2025"
    target_prefix = "00IndiceElectronico"

    # Llamar a la función para eliminar los archivos
    delete_files_by_prefix(folder_path, target_prefix)
