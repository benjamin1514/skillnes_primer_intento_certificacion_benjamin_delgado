from flask_app.config.mysqlconnection import connectToMySQL

class Comentario:
    def __init__(self, data):
        self.id_comentario = data['id_comentario']
        self.comentario = data['comentario']
        self.id_usuario = data['id_usuario']
        self.id_pelicula = data['id_pelicula']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO comentarios (comentario, id_usuario, id_pelicula)
            VALUES (%(comentario)s, %(id_usuario)s, %(id_pelicula)s);
        """
        return connectToMySQL('CinePedia').query_db(query, data)

    @classmethod
    def get_by_pelicula_id(cls, pelicula_id):
        query = "SELECT * FROM comentarios WHERE id_pelicula = %(id_pelicula)s;"
        results = connectToMySQL('CinePedia').query_db(query, {'id_pelicula': pelicula_id})
        comentarios = []
        for row in results:
            comentarios.append(cls(row))
        return comentarios