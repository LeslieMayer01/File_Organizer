import os

# Parámetros de configuración para el entorno de desarrollo
FOLDER_TO_ORGANIZE = "/path/to/folder"

# Ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Rutas de directorios relativos al directorio base
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_DIR = os.path.join(BASE_DIR, "data")
