from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario:
    def __init__(self, data):
        self.id_usuario = data['id_usuario']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.email = data['email']
        self.password_hash = data['password_hash']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        if len(usuario['nombre']) < 2:
            flash("El nombre debe tener al menos 2 caracteres.", "error_nombre")
            is_valid = False
        if len(usuario['apellido']) < 2:
            flash("El apellido debe tener al menos 2 caracteres.", "error_apellido")
            is_valid = False
        if not email_regex.match(usuario['email']):
            flash("Correo electrónico inválido.", "error_email")
            is_valid = False
        if len(usuario['password']) < 8:
            flash("La contraseña debe tener al menos 8 caracteres.", "error_password")
            is_valid = False
        if usuario['password'] != usuario['confirm_password']:
            flash("Las contraseñas no coinciden.", "error_confirm_password")
            is_valid = False
        return is_valid

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO usuarios (nombre, apellido, email, password_hash)
            VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s);
        """
        return connectToMySQL('CinePedia').query_db(query, data)

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        result = connectToMySQL('CinePedia').query_db(query, {'email': email})
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM usuarios WHERE id_usuario = %(id_usuario)s;"
        result = connectToMySQL('CinePedia').query_db(query, {'id_usuario': id})
        if result:
            return cls(result[0])
        return None