from flask import Flask, render_template, request, redirect, url_for, flash, session  # Importar las clases y funciones necesarias de Flask
import bcrypt  # Importar bcrypt para el hashing de contraseñas
from config import Config  # Importar la configuración desde el archivo config.py
from models import User  # Asegúrate de que tu clase User esté correctamente definida

app = Flask(__name__)
app.config.from_object(Config)

# Comentar o eliminar la conexión a la base de datos
# db = mysql.connector.connect(
#     host=app.config['DATABASE_HOST'],
#     user=app.config['DATABASE_USER'],
#     password=app.config['DATABASE_PASSWORD'],
#     database=app.config['DATABASE_NAME']
# )

# Simular una base de datos en memoria
usuarios_db = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def registrar():
    return render_template('register.html')

@app.route('/register/sumbit', methods=['POST'])
def create_user():
    print(request.form)  # Para depurar, muestra los datos enviados por el formulario
    first_name = request.form.get('first_name').upper() 
    last_name = request.form.get('last_name').upper() 
    birth_date = request.form.get('birth_date')  # No hacer upper() en la fecha
    document_type = request.form.get('document_type').upper() 
    document_number = request.form.get('document_number').upper() 
    email = request.form.get('email').upper() 
    password = request.form.get('password')  # No hacer upper() en la contraseña

    # Verificar si el número de documento ya existe
    if document_number in usuarios_db:
        flash('Error: El número de documento ya está en uso.', 'error')
        return redirect(url_for('registrar'))

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    usuarios_db[document_number] = {
        'nombre': first_name,
        'apellido': last_name,
        'birth_date': birth_date,
        'tipo': document_type,
        'correo': email,
        'contraseña': hashed_password,
        'id': len(usuarios_db) + 1  # Generar un ID simple
    }
    
    flash('Usuario registrado exitosamente.', 'success')
    return redirect(url_for('login'))  # Redirigir al índice (inicio de sesión)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/sumbit', methods=['POST'])
def login_user():
    email = request.form.get('email').upper()
    password = request.form.get('password')
    print(f"Email ingresado: {email}")

    user = next((u for u in usuarios_db.values() if u['correo'] == email), None)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['contraseña'].encode('utf-8')):
        session['logueado'] = True
        session['id'] = user['id']
        return redirect(url_for('index'))
    else:
        flash('Credenciales no válidas.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['logueado'] = False
    session['id'] = 0
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)