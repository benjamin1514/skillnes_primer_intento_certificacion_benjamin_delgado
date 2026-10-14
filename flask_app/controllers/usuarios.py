from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.usuario import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "id_usuario" in session:
        return redirect("/cine")
    return render_template("index.html")


@app.route("/registro", methods=["POST"])
def registro():
    if not Usuario.validar_usuario(request.form):
        return redirect("/")

    usuario_existente = Usuario.get_by_email(request.form["email"])
    if usuario_existente:
        flash("El correo electrónico ya está registrado.", "registro")
        return redirect("/")

    data = {
        "nombre": request.form["nombre"],
        "apellido": request.form["apellido"],
        "email": request.form["email"],
        "password_hash": bcrypt.generate_password_hash(
            request.form["password"]
        ),
    }

    id_usuario = Usuario.save(data)
    session["id_usuario"] = id_usuario
    session["usuario_nombre"] = request.form["nombre"]

    return redirect("/cine")


@app.route("/login", methods=["POST"])
def login():
    usuario = Usuario.get_by_email(request.form["email"])
    if not usuario or not bcrypt.check_password_hash(
        usuario.password_hash, request.form["password"]
    ):
        flash("Credenciales inválidas.", "login")
        return redirect("/")

    session["id_usuario"] = usuario.id_usuario
    session["usuario_nombre"] = usuario.nombre

    return redirect("/cine")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")