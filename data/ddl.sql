CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    birth_date DATE NOT NULL,           
    tipo VARCHAR(10) CHECK (tipo IN ('CEDULA', 'NIT', 'PASAPORTE')) NOT NULL, 
    cc VARCHAR(20) UNIQUE NOT NULL,     
    correo VARCHAR(100) UNIQUE NOT NULL, 
    contraseña VARCHAR(255) NOT NULL     
)