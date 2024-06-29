import os
from datetime import datetime
import subprocess
from config.general import ConfigDesarrollo 

def realizar_backup_mysql():
    destino = 'database/backups/'
    
    # Asegúrate de que la ruta de destino exista
    if not os.path.exists(destino):
        os.makedirs(destino)

    # Ruta completa al ejecutable mysqldump
    mysqldump_path = r'C:\xampp\mysql\bin\mysqldump.exe'  # Cambia esta ruta según tu instalación

    # Construye el comando mysqldump
    comando = [
        mysqldump_path,
        '-h', ConfigDesarrollo.MYSQL_HOST,
        '-u', ConfigDesarrollo.MYSQL_USER,
        '-p' + ConfigDesarrollo.MYSQL_PASSWORD,
        ConfigDesarrollo.MYSQL_DB
    ]
    
    # Genera un nombre de archivo con la fecha y hora actual
    fecha_hora = datetime.now().strftime("%d%m%Y_%H%M")
    archivo_backup = f"{ConfigDesarrollo.MYSQL_DB}_backup_{fecha_hora}.sql"

    # Ruta completa donde se guardará el archivo de backup
    ruta_backup = os.path.join(destino, archivo_backup)

    try:
        # Ejecuta el comando mysqldump y guarda la salida en el archivo de backup
        with open(ruta_backup, 'w') as archivo:
            subprocess.check_call(comando, stdout=archivo)
        print(f"Backup de MySQL exitoso. Archivo de backup: {ruta_backup}")
    except subprocess.CalledProcessError as e:
        print(f"Error durante el backup de MySQL: {e}")
    except FileNotFoundError as e:
        print(f"El archivo mysqldump no se encontró: {e}")