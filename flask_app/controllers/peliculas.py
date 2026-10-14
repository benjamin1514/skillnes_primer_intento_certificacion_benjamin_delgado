from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.pelicula import Pelicula
from flask_app.models.comentario import Comentario


@app.route("/cine")
def dashboard():
    if "id_usuario" not in session:
        return redirect("/")

    peliculas = Pelicula.get_all()
    return render_template("dashboard.html", peliculas=peliculas)


@app.route("/cine/nueva")
def nueva_pelicula_vista():
    if "id_usuario" not in session:
        return redirect("/")

    return render_template("nueva_pelicula.html")


@app.route("/cine/nueva", methods=["POST"])
def crear_pelicula():
    if "id_usuario" not in session:
        return redirect("/")

    if (
        not request.form["titulo"]
        or not request.form["director"]
        or not request.form["fecha_estreno"]
        or not request.form["sinopsis"]
    ):
        flash("Todos los campos son obligatorios.")
        return render_template("nueva_pelicula.html", form_data=request.form)

    data = {
        "titulo": request.form["titulo"],
        "director": request.form["director"],
        "genero": request.form.get("genero", ""),
        "fecha_estreno": request.form["fecha_estreno"],
        "sinopsis": request.form["sinopsis"],
        "id_usuario": session["id_usuario"],
    }

    Pelicula.save(data)
    return redirect("/cine")


@app.route("/cine/<int:id>")
def ver_pelicula(id):
    if "id_usuario" not in session:
        return redirect("/")

    pelicula = Pelicula.get_by_id(id)
    if not pelicula:
        return redirect("/cine")

    comentarios = Comentario.get_by_pelicula_id(id)
    return render_template(
        "ver_pelicula.html", pelicula=pelicula, comentarios=comentarios
    )


@app.route("/cine/editar/<int:id>")
def editar_pelicula_vista(id):
    if "id_usuario" not in session:
        return redirect("/")

    pelicula = Pelicula.get_by_id(id)
    if not pelicula or pelicula.id_usuario != session["id_usuario"]:
        return redirect("/cine")

    return render_template("editar_pelicula.html", pelicula=pelicula)


@app.route("/cine/editar/<int:id>", methods=["POST"])
def actualizar_pelicula(id):
    if "id_usuario" not in session:
        return redirect("/")

    pelicula = Pelicula.get_by_id(id)
    if not pelicula or pelicula.id_usuario != session["id_usuario"]:
        return redirect("/cine")

    if (
        not request.form["titulo"]
        or not request.form["director"]
        or not request.form["fecha_estreno"]
        or not request.form["sinopsis"]
    ):
        flash("Todos los campos son obligatorios.")
        return render_template(
            "editar_pelicula.html", pelicula=pelicula, form_data=request.form
        )

    data = {
        "id_pelicula": id,
        "titulo": request.form["titulo"],
        "director": request.form["director"],
        "genero": request.form.get("genero", ""),
        "fecha_estreno": request.form["fecha_estreno"],
        "sinopsis": request.form["sinopsis"],
        "id_usuario": session["id_usuario"],
    }

    Pelicula.update(data) if hasattr(Pelicula, "update") else None
    return redirect("/cine")


@app.route("/cine/borrar/<int:id>", methods=["POST"])
def eliminar_pelicula(id):
    if "id_usuario" not in session:
        return redirect("/")

    pelicula = Pelicula.get_by_id(id)
    if pelicula and pelicula.id_usuario == session["id_usuario"]:
        Pelicula.delete(id) if hasattr(Pelicula, "delete") else None

    return redirect("/cine")