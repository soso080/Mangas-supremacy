from flask import Flask, request, render_template, redirect, url_for, session
from pymongo import MongoClient


client = MongoClient("mongodb+srv://soso:soso@cluster0.ggd13ry.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
app = Flask(__name__)
app.secret_key = "097ec46a5ccd5edb58047f4c2597d402b9ce3d4495e74d2ebadf15dfe1cc69d4"
db = client['mangas_supremacy_db']
user = db['user']
contacts = db['contact']


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/connexion")
def connexion():
    return render_template("connexion.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact_co")
def contact_co():
    nom = session['nom']
    prenom = session['prenom']
    
    return render_template("contact_co.html",nom=nom,prenom=prenom)

@app.route("/inscription")
def inscription():
    return render_template("inscription.html")

@app.route("/manwha")
def manwha():
    nom = session['nom']
    prenom = session['prenom']
    return render_template("manwha.html",nom=nom,prenom=prenom)

@app.route("/manhua")
def manhua():
    nom = session['nom']
    prenom = session['prenom']
    return render_template("manhua.html",nom=nom,prenom=prenom)

@app.route("/mangas")
def mangas():
    nom = session['nom']
    prenom = session['prenom']
    return render_template("mangas.html",nom=nom,prenom=prenom)

@app.route("/index_co")
def index_co():
    nom = session['nom']
    prenom = session['prenom']
    return render_template("index_co.html",nom=nom,prenom=prenom)

@app.route("/jeux")
def jeux():
    nom = session['nom']
    prenom = session['prenom']
    return render_template("jeux.html",nom=nom,prenom=prenom)


@app.route("/register",methods=['POST'])
def register():
    data = request.form

    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    password = data.get('password')
    session['nom'] = nom
    session['prenom'] = prenom

    existing_user = user.find_one({"email": email})
    if existing_user:
        return redirect(url_for('inscription'))

    new_user = {
        "nom":nom,
        "prenom":prenom,
        "email":email,
        "password":password
    }

    user.insert_one(new_user)
    return render_template("index_co.html",nom=nom,prenom=prenom,email=email)



@app.route("/login", methods=['POST'])
def login():
    data = request.form

    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    password = data.get('password')
    session['nom'] = nom
    session['prenom'] = prenom

    existing_email = user.find_one({"email": email})
    existing_account = user.find_one({"email": email, "password":password})

    if existing_account:
        nom = existing_account.get("nom")
        prenom = existing_account.get("prenom")
        session['nom'] = nom
        session['prenom'] = prenom
        return render_template("index_co.html",nom=nom, prenom=prenom)
    elif not existing_account or not existing_email:
        return redirect(url_for('connexion'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/contact", methods=['POST'])
def Contact():

    data = request.form

    nom = data.get('nom')
    email = data.get('email')
    phone = data.get('tel')
    message = data.get('tel')



    contact_form = {
        "nom":nom,
        "email":email,
        "phone":phone,
        "message":message
    }


    contacts.insert_one(contact_form)
    return redirect(url_for('contact'))

@app.route("/delete_all_account")
def delete_all_account():
    user.delete_many()
    return "tous les comptes ont ete supprimer"


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)

