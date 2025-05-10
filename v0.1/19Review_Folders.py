import os
import pandas as pd


def contar_y_reportar_carpetas(ruta_base):
    contador_carpetas_0563140 = 0
    reporte_carpetas_no_c0_ni_01p = []

    # Recorrer recursivamente la ruta
    for root, dirs, files in os.walk(ruta_base):
        for carpeta in dirs:
            # Verificar si la carpeta comienza con "0563140"
            if carpeta.startswith("0563140"):
                contador_carpetas_0563140 += 1
            # Verificar si la carpeta NO comienza con "C0" ni "01P"
            elif not (carpeta.startswith("C0") or carpeta.startswith("01P")):
                reporte_carpetas_no_c0_ni_01p.append(
                    {
                        "Nombre de la carpeta": carpeta,
                        "Ruta": os.path.join(root, carpeta),
                    }
                )

    # Crear reporte en archivo Excel
    if reporte_carpetas_no_c0_ni_01p:
        df = pd.DataFrame(reporte_carpetas_no_c0_ni_01p)
        df.to_excel("reporte_carpetas_no_c0_ni_01p.xlsx", index=False)
        print("Reporte generado: reporte_carpetas_no_c0_ni_01p.xlsx")

    # Imprimir el conteo de carpetas que comienzan con "0563140"
    print(f"Total de carpetas que comienzan con '0563140': {contador_carpetas_0563140}")


# Especifica la ruta base que quieres recorrer
ruta_base = r"D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS\03TUTELAS 2020"
contar_y_reportar_carpetas(ruta_base)
