import psutil
import subprocess
import time
import os

def is_process_running(process_name):
    """
    Revisa si un proceso con el nombre especificado está en ejecución.
    """
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and process_name in cmdline:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def run_process(log_file_path):
    """
    Ejecuta el script 11_Create_Index_File.py y monitorea su salida.
    También guarda el log de la salida en un archivo.
    Si el proceso imprime el texto esperado, detiene la ejecución.
    """
    with open(log_file_path, 'a') as log_file:
        process = subprocess.Popen(
            [r".\env\Scripts\python.exe", ".\\11_Create_Index_File.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # Captura tanto stdout como stderr
            text=True
        )

        # Monitorear la salida del script
        for line in process.stdout:
            log_file.write(line)  # Escribir en el archivo de log
            log_file.flush()  # Asegurarse de que se escriba inmediatamente
            print(line.strip())  # Imprimir la salida en la terminal

            # Verificar si el mensaje esperado está en la salida
            if "Archivo Excel de carpetas no conformes generado en:" in line:
                print("Mensaje encontrado, terminando la ejecución del proceso.")
                process.terminate()  # Terminar el proceso si el mensaje es encontrado
                return

if __name__ == "__main__":
    process_name = "11_Create_Index_File.py"
    log_file_path = "proceso_log.txt"  # Archivo donde se guardará el log
    
    while True:
        # Revisar si el proceso está corriendo
        if not is_process_running(process_name):
            print(f"El proceso '{process_name}' no está corriendo. Iniciando...")
            run_process(log_file_path)
        else:
            print(f"El proceso '{process_name}' ya está corriendo.")
        
        # Esperar 60 segundos antes de volver a verificar
        time.sleep(60)
