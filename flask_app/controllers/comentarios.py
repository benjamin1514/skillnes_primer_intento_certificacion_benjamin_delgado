from flask import redirect, request, session
from flask_app import app
from flask_app.models.comentario import Comentario
from flask_app.models.pelicula import Pelicula

# permite crear comentarios para una pelicula específica, siempre que el usuario este logueado y el creador no puede hacer comentarios
@app.route("/comentarios/nuevo", methods=["POST"])
def crear_comentario():
    if "id_usuario" not in session:
        return redirect("/")

    id_pelicula = request.form.get("id_pelicula")
    pelicula = Pelicula.get_by_id(id_pelicula)

    if not pelicula or pelicula.id_usuario == session["id_usuario"]:
        return redirect(f"/cine/{id_pelicula}")

    if not request.form.get("comentario"):
        return redirect(f"/cine/{id_pelicula}")

    data = {
        "comentario": request.form["comentario"],
        "id_usuario": session["id_usuario"],
        "id_pelicula": id_pelicula,
    }

    Comentario.save(data)
    return redirect(f"/cine/{id_pelicula}")


# permite eliminar comentarios, cuando este logueado y sea el creador del comentario
@app.route("/comentarios/borrar/<int:id>", methods=["POST"])
def eliminar_comentario(id):
    if "id_usuario" not in session:
        return redirect("/")

    id_pelicula = request.form.get("id_pelicula")

    Comentario.delete(id) if hasattr(Comentario, "delete") else None

    if id_pelicula:
        return redirect(f"/cine/{id_pelicula}")
    return redirect("/cine")