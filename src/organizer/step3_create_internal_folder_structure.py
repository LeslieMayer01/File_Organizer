import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
import pandas as pd
import config

# Variable global para controlar modo simulación
MODO_SIMULACION = True


def añadir_fecha_y_hora_al_nombre(archivo: str) -> str:
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombre, extension = os.path.splitext(archivo)
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    return nuevo_nombre


def mover_carpeta(src: str, dst: str, reportes: list) -> None:
    os.makedirs(dst, exist_ok=True)
    destino_final = os.path.join(dst, os.path.basename(src))
    if not MODO_SIMULACION:
        shutil.move(src, destino_final)
        estado = "MOVIDA"
    else:
        estado = "A MOVER"
    reportes.append(
        {
            "Acción": "Mover Carpeta",
            "Origen": src,
            "Destino": destino_final,
            "Estado": estado,
        }
    )


def reorganizar_instancias_y_etapas(ruta_base: str, reportes: list) -> None:
    instancia_paths = {
        "C01": "01PrimeraInstancia",
        "C02": "01PrimeraInstancia",
        "C03": "01PrimeraInstancia",
        "C04": "01PrimeraInstancia",
        "C05": "01PrimeraInstancia",
        "C06": "02SegundaInstancia",
        "C08": "03RecursosExtraordinarios",
        "C10": "04Ejecucion",
    }

    for carpeta in instancia_paths.values():
        os.makedirs(os.path.join(ruta_base, carpeta), exist_ok=True)

    ppal_dir = os.path.join(ruta_base, "01PrimeraInstancia", "C01Principal")
    os.makedirs(ppal_dir, exist_ok=True)

    for item in os.listdir(ruta_base):
        path_item = os.path.join(ruta_base, item)
        if os.path.isfile(path_item):
            destino = os.path.join(ppal_dir, item)
            if not MODO_SIMULACION:
                shutil.move(path_item, destino)
                estado = "MOVIDO"
            else:
                estado = "A MOVER"
            reportes.append(
                {
                    "Acción": "Mover Archivo",
                    "Origen": path_item,
                    "Destino": destino,
                    "Estado": estado,
                }
            )

    for item in os.listdir(ruta_base):
        path_item = os.path.join(ruta_base, item)
        if os.path.isdir(path_item):
            for prefijo, c_destino in instancia_paths.items():
                if item.startswith(prefijo):
                    mover_carpeta(
                        path_item, os.path.join(ruta_base, c_destino), reportes
                    )
                    break


def create_folders(ruta_base: str, file_excel: str, solo_reporte: bool = True):
    palabras_clave = {
        "C01Principal": [
            "principal",
            "Principal",
            "ppal",
            "PPAL",
            "Ppal",
            "PRINCIPAL",
            "CuadernoUnico",
            "01.Expediente Restitutucion 056314089001201800150  ST",
            "01 Unica Instancia",
        ],
        "C05MedidasCautelares": [
            "medida",
            "Medida",
            "MEDIDA",
            "M.C",
            "M. Cautelar",
            "Media Cautelar",
            "MS",
            "Medias Cautelares",
            "MEDIDA CAUTELAR",
        ],
        "C03AcumulacionProcesos": [
            "acumulacion",
            "ACUMULACION",
            "Acumulacion",
        ],
        "C04DepositosJudiciales": [
            "deposito",
            "titulo",
            "TITULO",
            "Deposito",
            "DEPOSITOS",
            "Titulo",
            "DJ04",
        ],
        "C02Incidentes": [
            "indidente",
            "incidentes",
            "INCIDENTE",
            " Incidente",
            "Incidentes",
            "INCIDENTES",
        ],
        "C06Apelacion": [
            "Apelacion",
            "apelacion",
            "segunda instancia",
            " Segunda Instancia",
        ],
        "C08Recurso": ["tutela", "Tutela", "Recurso", " Extraordinario"],
        "C10EjecucionSentencia": [
            "tramiteposterior",
            "Traite Posterior",
            "Ejecucion",
            " ejecucion",
        ],
    }

    reportes: List[Dict[str, Any]] = []

    for root, dirs, _ in os.walk(ruta_base):
        for dir_name in dirs:
            if dir_name.startswith(
                "053804"
            ):  # CAMBIAR POR NUMERO DE IDENTIFICACION DEL JUZGADO
                ruta_actual = os.path.join(root, dir_name)
                reorganizar_instancias_y_etapas(ruta_actual, reportes)

                if not any(
                    os.path.isdir(os.path.join(ruta_actual, nombre))
                    for nombre in ["01PrimeraInstancia", "01UnicaInstancia"]
                ):
                    new = os.path.join(ruta_actual, "01PrimeraInstancia")
                    estado = "A CREAR"
                    if not solo_reporte and not MODO_SIMULACION:
                        os.mkdir(new)
                        estado = "CREADA"
                    reportes.append(
                        {
                            "Acción": "Crear Carpeta",
                            "Estado": estado,
                            "Ruta": new,
                        }
                    )

                tiene_C0 = any(
                    d.startswith("C0")
                    for d in os.listdir(ruta_actual)
                    if os.path.isdir(os.path.join(ruta_actual, d))
                )
                if not tiene_C0:
                    ruta_C0 = os.path.join(ruta_actual, "C01Principal")
                    estado = "A CREAR"
                    if not solo_reporte and not MODO_SIMULACION:
                        os.mkdir(ruta_C0)
                        estado = "CREADA"
                    reportes.append(
                        {
                            "Acción": "Crear Carpeta",
                            "Estado": estado,
                            "Ruta": ruta_C0,
                        }
                    )

        for dir_name in dirs:
            ruta_carp = os.path.join(root, dir_name)
            if dir_name in palabras_clave.keys():
                continue
            for nuevo_nombre, palabras in palabras_clave.items():
                if any(palabra in dir_name for palabra in palabras):
                    ruta_nueva = os.path.join(root, nuevo_nombre)
                    if os.path.exists(ruta_nueva):
                        estado = "DUPLICADA"
                    else:
                        if not solo_reporte and not MODO_SIMULACION:
                            try:
                                os.rename(ruta_carp, ruta_nueva)
                                estado = "RENOMBRADA"
                            except Exception as e:
                                estado = f"ERROR: {e}"
                        else:
                            estado = "A RENOMBRAR"
                    ruta = ruta_carp if estado == "DUPLICADA" else ruta_nueva
                    reportes.append(
                        {
                            "Acción": "Renombrar Carpeta",
                            "Nombre Anterior": dir_name,
                            "Nombre Nuevo": nuevo_nombre,
                            "Estado": estado,
                            "Ruta": ruta,
                        }
                    )
                    break

    df = pd.DataFrame(reportes)
    df.to_excel(file_excel, index=False)
    print(f"Reporte generado en: {file_excel}")


def run():
    print("✏️ Step 3: Renaming folders...")
    archivo_reporte = "./reports/" + añadir_fecha_y_hora_al_nombre(
        "Reporte_Gestion_Carpetas.xlsx"
    )
    create_folders(
        config.FOLDER_TO_ORGANIZE, archivo_reporte, solo_reporte=True
    )  # Cambiar a False para ejecutar cambios reales"
