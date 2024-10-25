# config.py

# Importar el módulo 'os' para interactuar con el sistema operativo.
import os

# Definir una clase llamada Config que contendrá la configuración de la aplicación.
class Config:
    # Establecer la clave secreta de la aplicación. Si no se encuentra en las variables de entorno, se usará una clave por defecto.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # Configuración del host de la base de datos.
    DATABASE_HOST = 'localhost'
    
    # Configuración del usuario de la base de datos.
    DATABASE_USER = 'root'
    
    # Configuración de la contraseña de la base de datos. En este caso, se deja vacío.
    DATABASE_PASSWORD = ''
    
    # Configuración del nombre de la base de datos que se utilizará en la aplicación.
    DATABASE_NAME = 'gerencia'
