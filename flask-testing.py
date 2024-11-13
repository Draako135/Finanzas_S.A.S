import pytest
from flask import Flask, request, flash

# Configuración de la aplicación Flask
app = Flask(__name__)
app.secret_key = 'test_secret_key'
usuarios_db = {}

@app.route('/register/sumbit', methods=['POST'])
def create_user():
    document_number = request.form.get('document_number').upper()
    if document_number in usuarios_db:
        flash('Error: El número de documento ya está en uso.', 'error')
        return '', 400  # Código de error
    usuarios_db[document_number] = request.form.to_dict()
    return '', 201  # Usuario creado

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_create_user(client):
    data = {
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'birth_date': '2000-01-01',
        'document_type': 'DNI',
        'document_number': '12345678',
        'email': 'juan@example.com',
        'password': 'password123'
    }
    response = client.post('/register/sumbit', data=data)
    assert response.status_code == 201
    assert '12345678' in usuarios_db

def test_create_user_existing_document(client):
    # Registrar el primer usuario
    data = {
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'birth_date': '2000-01-01',
        'document_type': 'DNI',
        'document_number': '12345678',
        'email': 'juan@example.com',
        'password': 'password123'
    }
    client.post('/register/sumbit', data=data)

    # Intentar registrar un segundo usuario con el mismo documento
    data2 = {
        'first_name': 'María',
        'last_name': 'Gómez',
        'birth_date': '1990-05-15',
        'document_type': 'DNI',
        'document_number': '12345678',
        'email': 'maria@example.com',
        'password': 'password456'
    }
    response = client.post('/register/sumbit', data=data2)
    assert response.status_code == 400  # Código de error para documento existente
