import os

from dotenv import load_dotenv

load_dotenv()
# Parámetros de configuración para el entorno de desarrollo
FOLDER_TO_ORGANIZE = os.getenv("FOLDER_TO_ORGANIZE")

# Ruta base del proyecto
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Rutas de directorios relativos al directorio base
LOGS_DIR = os.path.join(BASE_DIR, "logs")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
DATA_DIR = os.path.join(BASE_DIR, "data")

JUDGEMENT_ID = os.getenv("JUDGEMENT_ID")

TEMPLATE_FILE = BASE_DIR + "/data/ElectronicIndexTemplate.xlsm"
DATABASE_FILE = DATA_DIR + "BaseDatosRadicados.xlsx"
KEYWORDS_JSON = DATA_DIR + "keywords.json"

SIMULATE_STEP_1 = os.getenv("SIMULATE_STEP_1")
SIMULATE_STEP_2 = os.getenv("SIMULATE_STEP_2")
SIMULATE_STEP_3 = os.getenv("SIMULATE_STEP_3")
SIMULATE_STEP_4 = os.getenv("SIMULATE_STEP_4")
SIMULATE_STEP_5 = os.getenv("SIMULATE_STEP_5")
SIMULATE_STEP_6 = os.getenv("SIMULATE_STEP_6")
SIMULATE_STEP_7 = os.getenv("SIMULATE_STEP_7")
SIMULATE_STEP_8 = os.getenv("SIMULATE_STEP_8")
