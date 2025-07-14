from flask import Flask, redirect, url_for, render_template, request, session, make_response
from datetime import datetime, timedelta
app = Flask(__name__)

app.secret_key = '1234'
# Define o tempo de vida da sessão para 30 minutos
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/login", methods=["GET", "POST"])
def carregarform():
    tema = request.cookies.get("tema", "claro")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verifica as credenciais
        if username == "admin" and password == "1234":
            # Se as credenciais estiverem corretas, define a sessão como permanente
            # e armazena o nome de usuário na sessão.
            session.permanent = True
            session["username"] = username
            return redirect(url_for("carregarhome"))
        else:
            # Se as credenciais estiverem incorretas, renderiza a página de login
            # novamente com uma mensagem de erro.
            return render_template("login.html", error="Usuário ou senha inválidos.", tema=tema)
    else:
        # Se o método for GET, simplesmente renderiza a página de login.
        return render_template("login.html", tema=tema)

   

@app.route("/home", methods=["GET", "POST"])
def carregarhome():
    tema = request.cookies.get("tema", "claro")
    if "username" in session:
        if "views" in session:
            session["views"] += 1
        else:
            session["views"] = 1
        resp = make_response(render_template("home.html", views=session["views"], tema=tema))
        resp.set_cookie("ultima_categoria", "home", max_age=1800)
        return resp
    else:
        return redirect(url_for("carregarform"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("views", None)
    return redirect(url_for("carregarform"))

@app.route("/esportes")
def esportes():
   tema = request.cookies.get("tema", "claro")
   resp = make_response(render_template("esportes.html", tema=tema))
   resp.set_cookie("ultima_categoria", "esportes", max_age=1800)
   return resp

@app.route("/entretenimento")
def entretenimento():
   tema = request.cookies.get("tema", "claro")
   resp = make_response(render_template("entretenimento.html", tema=tema))
   resp.set_cookie("ultima_categoria", "entretenimento", max_age=1800)
   return resp

@app.route("/lazer")
def lazer():
   tema = request.cookies.get("tema", "claro")
   resp = make_response(render_template("lazer.html", tema=tema))
   resp.set_cookie("ultima_categoria", "lazer", max_age=1800)
   return resp

@app.route("/")
def index():
    if "username" in session:
        ultima_categoria = request.cookies.get("ultima_categoria", "home")
        if ultima_categoria == "home":
            return redirect(url_for("carregarhome"))
        elif ultima_categoria in ["esportes", "entretenimento", "lazer"]:
            return redirect(url_for(ultima_categoria))
        else:
            return redirect(url_for("carregarhome"))
    else:
        return redirect(url_for("carregarform"))


@app.route("/alternar-tema", methods=["POST"])
def alternar_tema():
    tema_atual = request.cookies.get("tema", "claro")
    novo_tema = "escuro" if tema_atual == "claro" else "claro"

    resp = make_response(redirect(url_for("carregarhome")))

    resp.set_cookie("tema", novo_tema, expires=datetime.utcnow() + timedelta(minutes=30))

    return resp

if __name__ == "__main__":
    app.run(debug=True)