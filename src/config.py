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
DATABASE_FILE = DATA_DIR + "/BaseDatosRadicados.xlsx"
KEYWORDS_JSON = DATA_DIR + "/keywords.json"
FOLDER_MAPPINGS = DATA_DIR + "/folder_mappings.json"


def parse_bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes", "y")


SIMULATE_STEP_1 = parse_bool(os.getenv("SIMULATE_STEP_1", "false"))
SIMULATE_STEP_2 = parse_bool(os.getenv("SIMULATE_STEP_2", "false"))
SIMULATE_STEP_3 = parse_bool(os.getenv("SIMULATE_STEP_3", "false"))
SIMULATE_STEP_4 = parse_bool(os.getenv("SIMULATE_STEP_4", "false"))
SIMULATE_STEP_5 = parse_bool(os.getenv("SIMULATE_STEP_5", "false"))
SIMULATE_STEP_6 = parse_bool(os.getenv("SIMULATE_STEP_6", "false"))
SIMULATE_STEP_7 = parse_bool(os.getenv("SIMULATE_STEP_7", "false"))
SIMULATE_STEP_8 = parse_bool(os.getenv("SIMULATE_STEP_8", "false"))
SIMULATE_STEP_9 = parse_bool(os.getenv("SIMULATE_STEP_9", "false"))
