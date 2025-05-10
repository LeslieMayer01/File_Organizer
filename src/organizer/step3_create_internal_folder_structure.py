import os
import pandas as pd
from datetime import datetime


def añadir_fecha_y_hora_al_nombre(archivo):
    fecha_hora_actual = datetime.now().strftime("%d-%m-%Y_%H-%M")
    nombre, extension = os.path.splitext(archivo)
    nuevo_nombre = f"{fecha_hora_actual}-{nombre}{extension}"
    return nuevo_nombre


# Configuración
ruta_directorio = r"C:\Users\Usuario\Downloads\Proyectos\J1"
archivo_reporte = "./reports/" + añadir_fecha_y_hora_al_nombre(
    "Reporte_Gestion_Carpetas.xlsx"
)


def run():
    print("✏️ Step 3: Renaming folders...")
    create_folders(ruta_directorio, archivo_reporte, solo_reporte=True)


def create_folders(ruta_base, archivo_excel, solo_reporte=False):
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
    }

    reportes = []

    for root, dirs, _ in os.walk(ruta_base):
        for dir_name in dirs:
            ruta_actual = os.path.join(root, dir_name)

            if dir_name.startswith("053804"):
                ruta_053804 = ruta_actual

                # Crear 01PrimeraInstancia si no existen
                # ni 01PrimeraInstancia ni 01UnicaInstancia
                if not any(
                    os.path.isdir(os.path.join(ruta_053804, nombre))
                    for nombre in ["01PrimeraInstancia", "01UnicaInstancia"]
                ):
                    new = os.path.join(ruta_053804, "01PrimeraInstancia")
                    estado = "A CREAR"
                    if not solo_reporte:
                        os.mkdir(new)
                        estado = "CREADA"
                    reportes.append(
                        {
                            "Acción": "Crear Carpeta",
                            "Estado": estado,
                            "Ruta": new,
                        }
                    )

                # Verificar si hay alguna carpeta que comience con C0
                tiene_C0 = any(
                    d.startswith("C0")
                    for d in os.listdir(ruta_053804)
                    if os.path.isdir(os.path.join(ruta_053804, d))
                )
                if not tiene_C0:
                    ruta_C0 = os.path.join(ruta_053804, "C01Principal")
                    estado = "A CREAR"
                    if not solo_reporte:
                        os.mkdir(ruta_C0)
                        estado = "CREADA"
                    reportes.append(
                        {
                            "Acción": "Crear Carpeta",
                            "Estado": estado,
                            "Ruta": ruta_C0,
                        }
                    )

        # Segundo recorrido para renombrar según palabras clave
        for dir_name in dirs:
            ruta_carpeta = os.path.join(root, dir_name)

            # Omitir nombres ya correctos
            if dir_name in palabras_clave.keys():
                continue

            for nuevo_nombre, palabras in palabras_clave.items():
                if any(palabra in dir_name for palabra in palabras):
                    ruta_nueva = os.path.join(root, nuevo_nombre)

                    if os.path.exists(ruta_nueva):
                        estado = "DUPLICADA"
                    else:
                        if not solo_reporte:
                            try:
                                os.rename(ruta_carpeta, ruta_nueva)
                                estado = "RENOMBRADA"
                            except Exception as e:
                                estado = f"ERROR: {e}"
                        else:
                            estado = "A RENOMBRAR"
                    if estado != "DUPLICADA":
                        ruta = ruta_nueva
                    else:
                        ruta = ruta_carpeta
                    reportes.append(
                        {
                            "Acción": "Renombrar Carpeta",
                            "Nombre Anterior": dir_name,
                            "Nombre Nuevo": nuevo_nombre,
                            "Estado": estado,
                            "Ruta": ruta,
                        }
                    )
                    # Evita múltiples renombramientos
                    # para la misma carpeta
                    break

    df = pd.DataFrame(reportes)
    df.to_excel(archivo_excel, index=False)
    print(f"Reporte generado en: {archivo_excel}")
