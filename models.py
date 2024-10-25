from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager

app = Flask(__name__)
app.config.from_object('config.Config')

# Comentar o eliminar la conexión a la base de datos
# db = mysql.connector.connect(
#     host=app.config['DATABASE_HOST'],
#     user=app.config['DATABASE_USER'],
#     password=app.config['DATABASE_PASSWORD'],
#     database=app.config['DATABASE_NAME']
# )

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)  # Inicializa el gestor de inicio de sesión
login_manager.login_view = 'login'  # Define la vista de inicio de sesión que se utilizará

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id  # Almacena el ID del usuario
        self.username = username  # Almacena el nombre de usuario
        self.role = role  # Almacena el rol del usuario (ej. admin, usuario regular)

@login_manager.user_loader
def load_user(user_id):
    # Aquí puedes simular la carga de un usuario sin acceder a la base de datos.
    # Por ejemplo, puedes crear un usuario de prueba.
    if user_id == "1":  # Suponiendo que el ID del usuario de prueba es "1"
        return User("1", "testuser", "admin")  # Retorna un usuario de prueba
    return None  # Si no se encontró el usuario, retorna None

# Resto de tu código (rutas, etc.)

if __name__ == '__main__':
    app.run(debug=True)