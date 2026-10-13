from flask_app.config.mysqlconnection import connectToMySQL


class Pelicula:
    def __init__(self, data):
        self.id_pelicula = data['id_pelicula']
        self.titulo = data['titulo']
        self.director = data['director']
        self.genero = data['genero']
        self.fecha_estreno = data['fecha_estreno']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = """
            INSERT INTO peliculas (titulo, director, genero, fecha_estreno)
            VALUES (%(titulo)s, %(director)s, %(genero)s, %(fecha_estreno)s);
        """
        return connectToMySQL('CinePedia').query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM peliculas;"
        results = connectToMySQL('CinePedia').query_db(query)
        peliculas = []
        for row in results:
            peliculas.append(cls(row))
        return peliculas

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM peliculas WHERE id_pelicula = %(id_pelicula)s;"
        result = connectToMySQL('CinePedia').query_db(query, {'id_pelicula': id})
        if result:
            return cls(result[0])
        return None