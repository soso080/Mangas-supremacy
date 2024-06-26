from flask import Flask, request, render_template, redirect, url_for, session, jsonify, make_response
from pymongo import MongoClient


client = MongoClient("mongodb+srv://soso:soso@cluster0.ggd13ry.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
app = Flask(__name__)
app.secret_key = "097ec46a5ccd5edb58047f4c2597d402b9ce3d4495e74d2ebadf15dfe1cc69d4"
db = client['mangas_supremacy_db']
user = db['user']
contacts = db['contact']
Nbr_vote = db['vote']



#----------------------------------Page de redirection------------------------------------------------------------------

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

@app.route("/admin")
def admin():
    return render_template("admin.html")



#----------------------------------Formulaire/Connexion------------------------------------------------------------------



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
    return redirect(url_for('contact_co'))

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

    #existing_email = user.find_one({"email": email})
    existing_account = user.find_one({"email": email, "password":password})

    if existing_account:
        nom = existing_account.get("nom")
        prenom = existing_account.get("prenom")
        session['nom'] = nom
        session['prenom'] = prenom
        return render_template("index_co.html",nom=nom, prenom=prenom)
    elif email == "soso@supremacy.com" and password == "admin":
        return render_template("admin.html")
    else:
        return redirect(url_for('connexion'))
    

@app.route("/logout")
def logout():
    session.pop('nom', None)
    session.pop('prenom', None)
    return redirect(url_for('index'))


#----------------------------------vote_mangas--------------------------------------------------------------------------



@app.route("/vote/Dragon-Ball-Z", methods=['POST'])
def vote_dbz():
    if 'deja_voté' in session:
        return render_template("redirect_mangas_2.html")
    else:
        Nbr_vote.find_one_and_update(
            {"titre": "Dragon Ball Z"},
            {"$inc": {"Votes": 1}}  # Incrémente le nombre de votes de 1
        )
        session['deja_voté'] = True

    return render_template("redirect_mangas_1.html")

@app.route("/vote/One_Piece", methods=['POST'])
def vote_op():
    if 'deja_voté' in session:
        return render_template("redirect_mangas_2.html")
    else:
        Nbr_vote.find_one_and_update(
        {"titre": "One Piece"},
        {"$inc": {"Votes": 1}} 
    )
        session['deja_voté'] = True

    

    return render_template("redirect_mangas_1.html")


@app.route("/vote/naruto", methods=['POST'])
def vote_nar():
    if 'deja_voté' in session:
        return render_template("redirect_mangas_2.html")
    else:
        Nbr_vote.find_one_and_update(
            {"titre": "Naruto"},
            {"$inc": {"Votes": 1}}  
        )

    session['deja_voté'] = True

    return render_template("redirect_mangas_1.html")


#----------------------------------vote_manwha--------------------------------------------------------------------------



@app.route("/vote/The-Beginning-After-The-End", methods=['POST'])
def vote_TBATE():
    if 'deja_voté' in session:
        return render_template("redirect_manwha_2.html")
    else:
        Nbr_vote.find_one_and_update(
            {"titre": "The Beginning After The End"},
            {"$inc": {"Votes": 1}}  
        )
        session['deja_voté'] = True

    return render_template("redirect_manwha_1.html")

@app.route("/vote/Solo-Leveling", methods=['POST'])
def vote_soloL():
    if 'deja_voté' in session:
        return render_template("redirect_manwha_2.html")
    else:
        Nbr_vote.find_one_and_update(
        {"titre": "Solo Leveling"},
        {"$inc": {"Votes": 1}} 
    )
        session['deja_voté'] = True

    

    return render_template("redirect_manwha_1.html")


@app.route("/vote/Nano-Machine", methods=['POST'])
def vote_nanoM():
    if 'deja_voté' in session:
        return render_template("redirect_manwha_2.html")
    else:
        Nbr_vote.find_one_and_update(
            {"titre": "Nano Machine"},
            {"$inc": {"Votes": 1}}  
        )

    session['deja_voté'] = True

    return render_template("redirect_manwha_1.html")



#----------------------------------vote_manhua--------------------------------------------------------------------------



@app.route("/vote/Magic-Emperor", methods=['POST'])
def vote_magicE():
    if 'deja_voté' in session:
        return render_template("redirect_manhua_2.html")
    else:
        Nbr_vote.find_one_and_update(
            {"titre": "Magic Emperor"},
            {"$inc": {"Votes": 1}}  
        )
        session['deja_voté'] = True

    return render_template("redirect_manhua_1.html")


@app.route("/vote/Martial-Art-Reigns", methods=['POST'])
def vote_martialR():
    if 'deja_voté' in session:
        return render_template("redirect_manhua_2.html")
    else:
        Nbr_vote.find_one_and_update(
        {"titre": "Martial Art Reigns"},
        {"$inc": {"Votes": 1}} 
    )
        session['deja_voté'] = True

    

    return render_template("redirect_manhua_1.html")


@app.route("/vote/Martial-Peak", methods=['POST'])
def vote_martialP():
    if 'deja_voté' in session:
        return render_template("redirect_manhua_2.html")
    else:
        Nbr_vote.find_one_and_update(
            {"titre": "Martial Peak"},
            {"$inc": {"Votes": 1}}  
        )

    session['deja_voté'] = True

    return render_template("redirect_manhua_1.html")
    
#----------------------------------Admin--------------------------------------------------------------------------


@app.route("/reset/vote")
def reset_vote():
    response = make_response("")

    for cookie in request.cookies:
        response.delete_cookie(cookie)
    
    return render_template("redirect_admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)

