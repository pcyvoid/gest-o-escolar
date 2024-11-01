from flask import Flask, redirect, render_template, request
import bd

app = Flask(__name__)
user = {}
bd_instance = bd.BD()

@app.route("/")
def index():
    if isinstance(bd_instance.connection, dict) and "error" in bd_instance.connection:
        return render_template("errorConnection.html", errorBD=bd_instance.connection["error"])
    else:
        return render_template("login.html", error=False)

@app.route("/logar", methods=["POST"])
def logar():
    global user

    nomeUsuario = request.form["nomeUsuario"]
    senhaUsuario = request.form["senhaUsuario"]

    print(nomeUsuario, senhaUsuario)
    user = bd_instance.login(nomeUsuario, senhaUsuario)

    if "error" in user:
        return render_template("login.html", error=True)
    else:
        return redirect("/principal")
    
@app.route("/principal")
def escola():
    turmas = bd_instance.buscarTurmas() 
    return render_template("principal.html", user=user, turmas=turmas)

@app.route("/principal/excluir/<int:codigo>")
def excluirTurma(codigo):
    excluir = bd_instance.excluirTurma(codigo) 
    
    if excluir is True:
        return render_template("principal.html", excluir=True)
    else:
        return render_template("principal.html", excluir=False)

if __name__ == "__main__":
    app.run(debug=True)
