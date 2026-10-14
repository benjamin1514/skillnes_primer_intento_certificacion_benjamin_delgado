from flask_app.config.mysqlconnection import connectToMySQL

# se crea la clase Pelicula
class Pelicula:

    def __init__(self, data):
        self.id_pelicula = data["id_pelicula"]
        self.titulo = data["titulo"]
        self.director = data["director"]
        self.fecha_estreno = data["fecha_estreno"]
        self.sinopsis = data["sinopsis"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.id_usuario = data["id_usuario"]

    # guarda las peliculas en la base de datos 
    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, id_usuario)
            VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(id_usuario)s);
        """
        return connectToMySQL("CinePedia").query_db(query, data)

    # obtiene todas las peliculas de la base de datos
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM peliculas;"
        results = connectToMySQL("CinePedia").query_db(query)
        peliculas = []
        if results:
            for row in results:
                peliculas.append(cls(row))
        return peliculas

    # obtiene una pelicula por su id y el nombre del usuario que la creo
    @classmethod
    def get_by_id(cls, id):
        query = """
            SELECT peliculas.*, usuarios.nombre AS usuario_nombre 
            FROM peliculas 
            JOIN usuarios ON peliculas.id_usuario = usuarios.id_usuario 
            WHERE id_pelicula = %(id_pelicula)s;
        """
        result = connectToMySQL("CinePedia").query_db(
            query, {"id_pelicula": id}
        )
        if result:
            pelicula = cls(result[0])
            pelicula.usuario_nombre = result[0]["usuario_nombre"]
            return pelicula
        return None

    # permite actualizar la pelicula, solo si es el creador de la misma
    @classmethod
    def update(cls, data):
        query = """
            UPDATE peliculas 
            SET titulo = %(titulo)s, director = %(director)s, fecha_estreno = %(fecha_estreno)s, sinopsis = %(sinopsis)s
            WHERE id_pelicula = %(id_pelicula)s AND id_usuario = %(id_usuario)s;
        """
        return connectToMySQL("CinePedia").query_db(query, data)

    # permite eliminar peliculas, solo si es el creador de la misma
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM peliculas WHERE id_pelicula = %(id_pelicula)s;"
        return connectToMySQL("CinePedia").query_db(query, {"id_pelicula": id})