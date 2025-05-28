import os
import re
from collections import defaultdict
from datetime import datetime

import pandas as pd

import config


def run():
    # Ejecutar
    procesar_directorio(
        config.FOLDER_TO_ORGANIZE,
        simular=True,  # Cambia a False para aplicar cambios reales
    )


def limpiar_nombre(nombre):
    # Eliminar todo lo antes de la primera letra
    nombre = re.sub(r"^[^a-zA-Z]*", "", nombre)
    # Eliminar caracteres especiales y espacios
    nombre = re.sub(r"[^a-zA-Z0-9]", "", nombre)
    # Limitar a 36 caracteres
    return nombre[:36]


def añadir_fecha_y_hora_al_nombre(nombre):
    fecha_hora = datetime.now().strftime("%d-%m-%Y_%H-%M")
    base, ext = os.path.splitext(nombre)
    return f"{fecha_hora}-{base}.xlsx"


def procesar_directorio(base_dir, simular=True):
    registros = []

    for root, _, files in os.walk(base_dir):
        files = [f for f in files if not f.lower().startswith("xcontrol")]
        if not files:
            continue

        todos_tienen_numeros = all(re.match(r"^\d+", f) for f in files)

        if todos_tienen_numeros:
            if len(files) > 100:
                files.sort(
                    key=lambda x: x[:3],
                    reverse=True,
                )
            else:
                files.sort(
                    key=lambda x: x[:2],
                    reverse=True,
                )
        else:
            files.sort(key=lambda x: os.path.getmtime(os.path.join(root, x)))

        nombres_usados = defaultdict(int)

        for i, nombre_original in enumerate(files, 1):
            ruta_original = os.path.join(root, nombre_original)
            nombre_base, ext = os.path.splitext(nombre_original)

            nombre_limpio = limpiar_nombre(nombre_base)

            contador = nombres_usados[nombre_limpio]
            nuevo_nombre = (
                f"{nombre_limpio}{contador:02d}" if contador else nombre_limpio
            )
            nombres_usados[nombre_limpio] += 1

            # SIN espacio entre número y nombre
            nombre_final = f"{i:02d}{nuevo_nombre}{ext}"
            ruta_nueva = os.path.join(root, nombre_final)

            estado = "SIMULADO" if simular else "RENOMBRADO"

            if not simular:
                os.rename(ruta_original, ruta_nueva)

            registros.append(
                {
                    "NOMBRE_ANTERIOR": nombre_original,
                    "NOMBRE_NUEVO": nombre_final,
                    "RUTA_ANTERIOR": ruta_original,
                    "RUTA_NUEVA": ruta_nueva,
                    "ESTADO": estado,
                    "ORDEN": i,
                }
            )

    if registros:
        df = pd.DataFrame(registros)
        df.sort_values(by="ORDEN", inplace=True)
        os.makedirs("./reports", exist_ok=True)
        nombre_archivo = añadir_fecha_y_hora_al_nombre("Reporte_Renombrado")
        ruta_archivo = os.path.join("reports", nombre_archivo)

        with pd.ExcelWriter(ruta_archivo, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Reporte")

        print(f"✅ Reporte Excel generado: {ruta_archivo}")
    else:
        print("⚠️ No se encontraron archivos válidos para procesar.")
