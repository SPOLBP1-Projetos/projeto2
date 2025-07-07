from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
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
    if "username" in session:
        return render_template("home.html")
    else:
        # Se o usuário não estiver logado, redireciona para a página de login.
        return redirect(url_for("carregarform"))

@app.route("/logout")
def logout():
    session.pop("username", None) # Remove o 'username' da sessão
    return redirect(url_for("carregarform"))

@app.route("/esportes")
def esportes():
   return render_template("esportes.html")

@app.route("/entretenimento")
def entretenimento():
   return render_template("entretenimento.html")

@app.route("/lazer")
def lazer():
   return render_template("lazer.html")

@app.route("/")
def index():
   return redirect(url_for("carregarform"))

if __name__ == "__main__":
    app.run(debug=True)