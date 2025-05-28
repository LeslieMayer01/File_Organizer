import os

from dotenv import load_dotenv

load_dotenv()
# Parámetros de configuración para el entorno de desarrollo
FOLDER_TO_ORGANIZE = os.getenv("FOLDER_TO_ORGANIZE")

# Ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_FILE = BASE_DIR + "/data/ElectronicIndexTemplate.xlsm"

# Rutas de directorios relativos al directorio base
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_DIR = os.path.join(BASE_DIR, "data")
