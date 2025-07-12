from flask import Flask, redirect, url_for, render_template, request, session, make_response
from datetime import datetime, timedelta
app = Flask(__name__)

app.secret_key = '1234'
# Define o tempo de vida da sessão para 30 minutos
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/login", methods=["GET", "POST"])
def carregarform():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verifica as credenciais
        if username == "Camilo" and password == "1234":
            # Se as credenciais estiverem corretas, define a sessão como permanente
            # e armazena o nome de usuário na sessão.
            session.permanent = True
            session["username"] = username
            return redirect(url_for("carregarhome"))
        else:
            # Se as credenciais estiverem incorretas, renderiza a página de login
            # novamente com uma mensagem de erro.
            return render_template("login.html", error="Usuário ou senha inválidos.")
    else:
        # Se o método for GET, simplesmente renderiza a página de login.
        return render_template("login.html")

   

@app.route("/home", methods=["GET", "POST"])
def carregarhome():
    tema = request.cookies.get("tema", "claro")
    if "username" in session:
        if "views" in session:
            session["views"] += 1
        else:
            session["views"] = 1
        return render_template("home.html", views=session["views"], tema=tema)
    else:
        return redirect(url_for("carregarform"), tema=tema)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("views", None)
    return redirect(url_for("carregarform"))

@app.route("/esportes")
def esportes():
   tema = request.cookies.get("tema", "claro")
   return render_template("esportes.html", tema=tema)

@app.route("/entretenimento")
def entretenimento():
   tema = request.cookies.get("tema", "claro")
   return render_template("entretenimento.html", tema=tema)

@app.route("/lazer")
def lazer():
   tema = request.cookies.get("tema", "claro")
   return render_template("lazer.html", tema=tema)

@app.route("/")
def index():
   return redirect(url_for("carregarform"))

@app.route("/alternar-tema", methods=["POST"])
def alternar_tema():
    tema_atual = request.cookies.get("tema", "claro")
    novo_tema = "escuro" if tema_atual == "claro" else "claro"

    resp = make_response(redirect(url_for("carregarhome")))

    # Opção com max_age (mais simples):
    resp.set_cookie("tema", novo_tema, expires=datetime.utcnow() + timedelta(minutes=30))

    # ou, se quiser usar expires:
    # from datetime import datetime, timedelta
    # resp.set_cookie("tema", novo_tema, expires=datetime.utcnow() + timedelta(minutes=30))

    return resp

if __name__ == "__main__":
    app.run(debug=True)