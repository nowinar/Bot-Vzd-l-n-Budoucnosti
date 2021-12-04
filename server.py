from flask import *
from config import CLIENT_SECRET, TOKEN, REDIRECT_URI, OAUTH_URL
from zenora import APIClient
app = Flask(__name__)
app.jinja_env.filters['zip'] = zip
client = APIClient(TOKEN, client_secret=CLIENT_SECRET)
import random
import string
def random_string(pocet):
    heslo = ""
    for i in range(pocet):
        znak = random.choice(string.ascii_letters + string.digits)
        heslo = heslo + znak
    return heslo
app.secret_key = random_string(100)
def nacti_sproste(uzivatel):
    with open("users.json", "r") as f:
        adminem = []
        data = f.read()
        data = json.loads(data)
        sproste_slova = {}
        for server, uzivatele in data.items():
            for jeden_uzivatel in uzivatele:
                if uzivatel == jeden_uzivatel:
                    adminem.append(server)
                    try:
                        with open("config.json", mode="r") as f:
                            data = json.loads(f.read())
                            sproste_slova[server] = data[server]
                            if sproste_slova[server] == []:
                                sproste_slova[server] = ["Pro tento server není definováno žádné sprosté slovo"]
                    except:
                        sproste_slova[server] = ["Pro tento server není definováno žádné sprosté slovo"]
    with open("zpravy.json", mode="r") as a:
        zpravy = json.loads(a.read())
    return [sproste_slova, adminem, zpravy]
@app.route("/admin")
def admin():
    if "uzivatel" in session:
        uzivatel = session["uzivatel"]
    else:
        return redirect(url_for("home"))
    data = nacti_sproste(uzivatel)
    print(data[0])
    return render_template("admin.html", user=uzivatel, adminem=data[1], sproste=data[0], zpravy=data[2])
@app.route("/")
def home():
    if "uzivatel" in session:
        return redirect(url_for("admin"))
    return render_template("index.html", oauth_uri=OAUTH_URL)
@app.route("/zpravy")
def zpravy():
    if "uzivatel" in session:
        uzivatel = session["uzivatel"]
    else:
        return redirect(url_for("home"))
    server = request.args["server"]
    data = nacti_sproste(uzivatel)
    return render_template("zpravy.html", server=server, zpravy=data[2])
@app.route("/oauth/callback")
async def callback():
    code = request.args["code"]
    acces_token = client.oauth.get_access_token(code, REDIRECT_URI).access_token
    bearer_client = APIClient(acces_token, bearer=True)
    session["uzivatel"] = bearer_client.users.get_current_user().username
    return redirect(url_for("admin"))
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
@app.route("/pridat")
def pridat():
    if "uzivatel" in session:
        uzivatel = session["uzivatel"]
    else:
        return redirect(url_for("home"))
    data = nacti_sproste(uzivatel)
    nazev = request.args["server"]
    print(nazev)
    print(data[0][nazev])
    return render_template("pridat.html", server=nazev, sproste=data[0][nazev])
@app.route("/add")
def add():
    if "uzivatel" in session:
        uzivatel = session["uzivatel"]
    else:
        return redirect(url_for("home"))
    mezi_gulema = {}
    server = request.args["server"]
    sproste = request.args["sproste"]
    data = nacti_sproste(uzivatel)
    print(data[1])
    if not str(server) in data[1]:
        print("zastaveno")
        return redirect(url_for("home"))
    try:
        with open("config.json", mode="r") as a:
            mezi_gulema = json.loads(a.read())
            if sproste in mezi_gulema[server]:
                return redirect(url_for("admin"))
            with open("config.json", mode="w") as f:
                mezi_gulema[server].append(sproste)
                f.write(json.dumps(mezi_gulema))
    except:
        with open("config.json", mode="w") as f:
            mezi_gulema[server] = [sproste]
            f.write(json.dumps(mezi_gulema))
    return redirect(url_for("admin"))
@app.route("/smazat/<int:idslova>/<server>")
def smazat(idslova, server):
    if "uzivatel" in session:
        uzivatel = session["uzivatel"]
    else:
        return redirect(url_for("home"))
    data = nacti_sproste(uzivatel)
    print(data[1])
    if not str(server) in data[1]:
        print("zastaveno")
        return redirect(url_for("home"))
    with open("config.json", mode="r") as a:
        mezi_gulema = json.loads(a.read())
        del mezi_gulema[server][idslova]
        print(mezi_gulema)
        with open("config.json", mode="w") as f:
            f.write(json.dumps(mezi_gulema))
    return redirect(url_for("admin"))
if __name__ == "__main__":
    app.run(debug = True)