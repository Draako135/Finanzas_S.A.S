from flask import Flask, render_template, request, redirect, url_for, flash, session
import bcrypt
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Simular una base de datos en memoria
usuarios_db = {}

# Crear un usuario admin al inicio (si no existe)
def create_admin():
    if not any(u['rol'] == 'admin' for u in usuarios_db.values()):
        print("Creando usuario administrador...")
        password = "admin123"
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuarios_db["admin"] = {
            'nombre': "Admin",
            'apellido': "Admin",
            'birth_date': "2000-01-01",
            'tipo': "CEDULA",
            'numero_documento': "123456789",
            'correo': "ADMIN@EXAMPLE.COM",
            'contraseña': hashed_password,
            'id': 1,
            'rol': 'admin'
        }
        print("Usuario administrador creado:", usuarios_db["admin"])
    else:
        print("Usuario administrador ya existe.")

create_admin()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def registrar():
    return render_template('register.html')

@app.route('/register/submit', methods=['POST'])
def create_user():
    first_name = request.form.get('first_name').upper()
    last_name = request.form.get('last_name').upper()
    birth_date = request.form.get('birth_date')
    document_type = request.form.get('document_type').upper()
    document_number = request.form.get('document_number').upper()
    email = request.form.get('email').upper()
    password = request.form.get('password')

    if document_number in usuarios_db:
        flash('Error: El número de documento ya está en uso.', 'error')
        return redirect(url_for('registrar'))

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    usuarios_db[document_number] = {
        'nombre': first_name,
        'apellido': last_name,
        'birth_date': birth_date,
        'tipo': document_type,
        'numero_documento': document_number,  # Asegúrate de que este campo esté correctamente nombrado
        'correo': email,
        'contraseña': hashed_password,
        'id': len(usuarios_db) + 1,
        'rol': 'usuario'
    }

    flash('Usuario registrado exitosamente.', 'success')
    session['logueado'] = True
    session['id'] = usuarios_db[document_number]['id']
    session['rol'] = 'usuario'
    
    return redirect(url_for('perfil'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login/submit', methods=['POST'])
def login_user():
    email = request.form.get('email').upper()
    password = request.form.get('password')

    user = next((u for u in usuarios_db.values() if u['correo'] == email), None)

    if user and bcrypt.checkpw(password.encode('utf-8'), user['contraseña'].encode('utf-8')):
        session['logueado'] = True
        session['id'] = user['id']
        session['rol'] = user['rol']
        return redirect(url_for('perfil'))
    else:
        flash('Credenciales no válidas.', 'error')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()  # Limpiar la sesión
    return redirect(url_for('index'))

@app.route('/perfil')
def perfil():
    if not session.get('logueado'):
        flash('Debes iniciar sesión primero.', 'error')
        return redirect(url_for('login'))

    user = next((u for u in usuarios_db.values() if u['id'] == session['id']), None)

    # Verifica que el usuario exista
    if user is None:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('login'))  # O redirige a otra página como el índice

    return render_template('perfil.html', user=user, rol=session['rol'])

@app.route('/perfil/editar', methods=['GET', 'POST'])
def editar_perfil():
    if not session.get('logueado'):
        flash('Debes iniciar sesión primero.', 'error')
        return redirect(url_for('login'))

    user = next((u for u in usuarios_db.values() if u['id'] == session['id']), None)

    if user is None:
        flash('Usuario no encontrado.', 'error')
        return redirect(url_for('perfil'))

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        birth_date = request.form.get('birth_date')
        document_type = user['tipo']  # Mantener tipo de documento
        numero_documento = user['numero_documento']  # Mantener número de documento
        email = request.form.get('email')
        password = request.form.get('password')

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8') if password else user['contraseña']

        usuarios_db[numero_documento] = {
            'nombre': first_name,
            'apellido': last_name,
            'birth_date': birth_date,
            'tipo': document_type,
            'numero_documento': numero_documento,
            'correo': email,
            'contraseña': hashed_password,
            'id': user['id'],
            'rol': user['rol']
        }

        flash('Información actualizada exitosamente.', 'success')
        return redirect(url_for('perfil'))

    return render_template('edit_usuario.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)