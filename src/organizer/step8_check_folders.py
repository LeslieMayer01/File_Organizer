import os
from datetime import datetime

import pandas as pd

import config

# Prefijos permitidos
prefijos_permitidos = ("05380", "01Primera", "01Unica", "C0")


def run():
    print("✏️ Step 8: Check Folders...")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_8}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return
    # 🔧 Cambia aquí tu ruta base
    listar_carpetas_no_validas(config.FOLDER_TO_ORGANIZE)


def añadir_fecha_y_hora_al_nombre(nombre):
    fecha_hora = datetime.now().strftime("%d-%m-%Y_%H-%M")
    base, ext = os.path.splitext(nombre)
    return f"{fecha_hora}-{base}.xlsx"


def listar_carpetas_no_validas(ruta_base):
    carpetas_no_validas = []

    for root, dirs, _ in os.walk(ruta_base):
        for carpeta in dirs:
            if not carpeta.startswith(prefijos_permitidos):
                ruta_completa = os.path.join(root, carpeta)
                carpetas_no_validas.append(
                    {"NOMBRE_CARPETA": carpeta, "RUTA": ruta_completa}
                )

    # Guardar en Excel
    if carpetas_no_validas:
        df = pd.DataFrame(carpetas_no_validas)
        os.makedirs("./reports", exist_ok=True)
        nombre_archivo = añadir_fecha_y_hora_al_nombre("Carpetas_No_Validas")
        ruta_archivo = os.path.join("reports", nombre_archivo)

        with pd.ExcelWriter(ruta_archivo, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Carpetas")

        print(f"✅ Reporte Excel generado: {ruta_archivo}")
    else:
        print("✅ No se encontraron carpetas no válidas.")
