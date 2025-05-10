from reporter.reporter import create_csv_report
from datetime import datetime
import config


def run():
    print("🧹 Step 1: Cleaning empty folders...")
    process_data()


def process_data():
    data = [
        ["Juan2", 25, "Desarrollador", 5000],
        ["Ana3", 30, "Diseñadora", 4500],
        ["Pedro4", 35, "Gerente", 7000],
    ]

    # Definimos los encabezados para el reporte
    headers = ["Nombre", "Edad", "Puesto", "Salario"]

    # Nombre del archivo basado en la fecha actual
    filename = f"step1_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    # Generamos el reporte CSV
    create_csv_report(data, headers, config.REPORTS_DIR, filename)
