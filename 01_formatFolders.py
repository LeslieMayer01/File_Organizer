import os

def renombrar_subcarpetas_recursivo(ruta):
    prefijo = "056314089001"
    
    if os.path.exists(ruta):
        for dirpath, dirnames, filenames in os.walk(ruta):  # os.walk permite buscar recursivamente
            for subcarpeta in dirnames:
                #print(subcarpeta)
                subcarpeta_path = os.path.join(dirpath, subcarpeta)
                
                # Comprobar si la subcarpeta empieza por "2020" y no ha sido renombrada aún
                if subcarpeta.startswith("2024") and not subcarpeta.startswith(prefijo):
                    # Crear el nuevo nombre
                    nuevo_nombre = prefijo + subcarpeta
                    nuevo_nombre_path = os.path.join(dirpath, nuevo_nombre)
                    
                    # Renombrar la carpeta
                    os.rename(subcarpeta_path, nuevo_nombre_path)
                    print(f"Renombrada: {subcarpeta_path} -> {nuevo_nombre_path}")
    else:
        print(f"La ruta {ruta} no existe o no es accesible")

# Ejemplo de uso
#rutas_absolutas = r'C:\Users\LESLIE CRUZ\OneDrive - Consejo Superior de la Judicatura\01. EXPEDIENTES DIGITALIZADOS DESDE JUNIO 2020\18-AÑO 2020\7. DEMANDAS DICIEMBRE - 2020-00439 AL 2020-00485'
rutas_absolutas = r'D:\OneDrive\OneDrive - Consejo Superior de la Judicatura\04. EXPEDIENTES DE TUTELAS'
renombrar_subcarpetas_recursivo(rutas_absolutas)
