import os
import shutil
from datetime import datetime

import pandas as pd

import config


def run():
    print("✏️ Step 5: Sub-folders Organization...")
    print(f"📁 Folder to process: {config.FOLDER_TO_ORGANIZE}")
    print(f"🧪 Simulation mode: {config.SIMULATE_STEP_6}")

    confirm = input("❓ Do you want to continue? [y/N]: ")
    if confirm.strip().lower() != "y":
        print("🚫 Operation cancelled by user.")
        return

    # Ejecutar función
    mover_estructura_judicial(config.FOLDER_TO_ORGANIZE, config.JUDGEMENT_ID)


def mover_estructura_judicial(ruta_base, codigo_despacho):
    datos_cambios = []

    # Iterar recursivamente por todas las carpetas
    for root, dirs, _ in os.walk(ruta_base):
        for dir_name in dirs:
            if dir_name.startswith(codigo_despacho):
                ruta_carpeta = os.path.join(root, dir_name)
                ruta_primera_instancia = os.path.join(
                    ruta_carpeta, "01PrimeraInstancia"
                )
                ruta_c01_principal = os.path.join(
                    ruta_primera_instancia, "C01Principal"
                )

                print(f"\nProcesando: {ruta_carpeta}")

                # Paso 2: Mover carpetas C0* a 01PrimeraInstancia
                if os.path.exists(ruta_primera_instancia):
                    for item in os.listdir(ruta_carpeta):
                        item_path = os.path.join(ruta_carpeta, item)
                        if os.path.isdir(item_path) and item.startswith("C0"):
                            path = os.path.join(ruta_primera_instancia, item)
                            try:
                                if not config.SIMULATE_STEP_6:
                                    shutil.move(item_path, path)
                                    estado = "MOVIDO"
                                else:
                                    estado = "SIMULADO (CARPETA)"
                                print(f"{estado}: {item} -> {path}")
                                datos_cambios.append(
                                    {
                                        "CARPETA": dir_name,
                                        "NOMBRE": item,
                                        "TIPO": "CARPETA",
                                        "ESTADO": estado,
                                        "RUTA": path,
                                    }
                                )
                            except Exception as e:
                                print(f"Error al mover carpeta: {item} -> {e}")

                # Paso 3 y 4: Mover archivos a C01Principal
                if os.path.exists(ruta_c01_principal):
                    for item in os.listdir(ruta_carpeta):
                        item_path = os.path.join(ruta_carpeta, item)
                        if os.path.isfile(item_path):
                            path = os.path.join(ruta_c01_principal, item)
                            try:
                                if not config.SIMULATE_STEP_6:
                                    shutil.move(item_path, path)
                                    estado = "MOVIDO"
                                else:
                                    estado = "SIMULADO (ARCHIVO)"
                                print(f"{estado}: {item} -> {path}")
                                datos_cambios.append(
                                    {
                                        "CARPETA": dir_name,
                                        "NOMBRE": item,
                                        "TIPO": "ARCHIVO",
                                        "ESTADO": estado,
                                        "RUTA": path,
                                    }
                                )
                            except Exception as e:
                                print(f"Error al mover archivo: {item} -> {e}")

    # Crear y guardar reporte
    df = pd.DataFrame(
        datos_cambios, columns=["CARPETA", "NOMBRE", "TIPO", "ESTADO", "RUTA"]
    )

    # Nombre del archivo según si es simulación o ejecución real
    if not config.SIMULATE_STEP_6:
        nombre_reporte = "Movimientos_Reales.xlsx"
    else:
        nombre_reporte = "Simulacion_Organizacion.xlsx"

    archivo_excel_final = os.path.join(
        "./reports", añadir_fecha_y_hora_al_nombre(nombre_reporte)
    )
    df.to_excel(archivo_excel_final, index=False)
    print(f"\n✅ Reporte guardado en: {archivo_excel_final}")


def añadir_fecha_y_hora_al_nombre(nombre_archivo):
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombre, extension = os.path.splitext(nombre_archivo)
    return f"{fecha_hora_actual}-{nombre}{extension}"
