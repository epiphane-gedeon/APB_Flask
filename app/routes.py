from app import app,db,bcrypt,login_manager,mail,ALLOWED_EXTENSIONS
from flask import render_template,flash,redirect,url_for,request
from app.forms import LoginForm,RegisterForm,ProductForm,ContactForm,CategorieForm
from app.models import Utilisateur,Produit,Categorie
from flask_login import login_user,current_user,login_required, logout_user
from flask_mail import Message
from flask_login import login_required
import urllib.request
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@login_manager.user_loader
def load_user(user_id):
    return Utilisateur.query.get(user_id)
@app.route("/",methods=["POST","GET"])
# @app.route("/index",methods=["POST","GET"])
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        email=form.email.data
        password=form.password.data
        #remember=form.remember_me.data
        user=Utilisateur.query.filter_by(email=email).first()
        user_admin=Utilisateur.query.filter_by(email=email,admin=True).first()
        print(user)

        if not user:
            flash("Email ou mot de passe incorrect")
            return redirect(url_for('login'))
        pswd_unhashed=bcrypt.check_password_hash(user.mot_pass,password)

        if not pswd_unhashed:
            flash("Email ou mot de passe incorrect")
            return redirect(url_for('login'))

        if user_admin:
            login_user(user_admin)
            flash("Vous êtes bien connecté")
            return redirect(url_for('admin'))
        login_user(user)
        return redirect(url_for('index'))
    
    return render_template("login.html",form=form)

@app.route("/register",methods=["POST","GET"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        nom=form.nom.data
        prenom=form.prenom.data
        password=form.password.data
        retypePassword=form.retypePassword.data
        email=form.email.data
        file = request.files['file']
        if file.filename == '':
            imgVide=True
        else:
            imgVide=False
        if file and allowed_file(file.filename):
            filename = 'profil_'+secure_filename(file.filename)

        if retypePassword==password:
            if imgVide:
                psw_hash=bcrypt.generate_password_hash(password).decode("utf8")
                user=Utilisateur(nom=nom,prenom=prenom,email=email,mot_pass=psw_hash,image='profil.png')
            else:
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                psw_hash=bcrypt.generate_password_hash(password).decode("utf8")
                user=Utilisateur(nom=nom,prenom=prenom,email=email,mot_pass=psw_hash,image=filename)
                print(user)
            db.session.add(user)
            db.session.commit()

            flash("Utilisateur enregistré avec succès")
            redirect(url_for('login'))
        else:
            flash("Les mots de passe ne concordent pas")
    return render_template("register.html",form=form)

@app.route("/deleteUser/<int:id>")
def deleteUser(id):
    user= Utilisateur.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('adminUser'))

@app.route("/deleteCategorie/<int:id>")
def deleteCategorie(id):
    cat= Categorie.query.get_or_404(id)
    db.session.delete(cat)
    db.session.commit()
    return redirect(url_for('adminCategorie'))

@app.route("/deleteProduct/<int:id>")
def deleteProduct(id):
    prod= Produit.query.get_or_404(id)
    db.session.delete(prod)
    db.session.commit()
    return redirect(url_for('adminProduits'))

@app.route("/logout/<int:id>")
def logout(id):
    user=Utilisateur.query.filter_by(id=id)
    logout_user()
    return redirect(url_for('login'),flash('Bien déconnectés'))

@app.route("/updateUser/<int:id>",methods=["GET","POST"])
def updateUser(id):
    user= Utilisateur.query.get_or_404(id)
    if request.method=="POST":
        user.nom=request.form["nom"]
        user.prenom=request.form["prenom"]
        user.email=request.form["email"]
        try:
            db.session.commit()
            return redirect(url_for('adminUser'))
        except Exception:
            return "Nous ne pouvons pas modifier l'utilisateur"
    else:
        return render_template("updateUser.html",user=user)
    
@app.route("/updateCategorie/<int:id>",methods=["GET","POST"])
def updateCategorie(id):
    cat= Categorie.query.get_or_404(id)
    if request.method=="POST":
        cat.nom=request.form["nom"]
        cat.description=request.form["description"]
        try:
            db.session.commit()
            return redirect(url_for('adminCategorie'))
        except Exception:
            return "Nous ne pouvons pas modifier la catégorie"
    else:
        return render_template("updateCategorie.html",cat=cat)
    
@app.route("/updateProduct/<int:id>",methods=["GET","POST"])
def updateProduct(id):
    prod= Produit.query.get_or_404(id)
    cat=Categorie.query.all()
    if request.method=="POST":
        prod.nom=request.form["nom"]

        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = 'Produit_'+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
        
        prod.image=filename
        prod.description=request.form["description"]
        prod.categorie=request.form["categorie"]
        prod.prix=request.form["prix"]
        try:
            db.session.commit()
            return redirect(url_for('adminProduits'))
        except Exception:
            return "Nous ne pouvons pas modifier le produit"
    else:
        return render_template("updateProduit.html",produit=prod,categorie=cat)

@app.route("/produits")
def produits():
    categories = Categorie.query.order_by(Categorie.id).all()
    produit=Produit.query.join(Categorie).all()
    print(produit)
    return render_template("produits.html",produits=produit,categories=categories)

@app.route("/ajoutProduit",methods=["POST","GET"])
def ajoutProduit():
    form=ProductForm()
    form.categorie.choices = [(c.id, c.nom) for c in Categorie.query.all()]
    if form.validate_on_submit():
        nom=form.nom.data
        description=form.description.data
        categorie=form.categorie.data
        prix=form.prix.data

        
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = 'Produit_'+secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Image successfully uploaded and displayed below')
        
        if prix<=0:
            flash("Le prix doit être supérieur à 0")
            redirect(url_for(ajoutProduit))
        
        prod=Produit(nom=nom,image=filename,description=description,categorie=categorie,prix=prix)

        db.session.add(prod)
        db.session.commit()
        flash("Produit ajouté")
        redirect(url_for('adminProduits'))
        # print(prod)
    return render_template("ajoutProduit.html",form=form)

@app.route("/panier")
def panier():
    if current_user.is_authenticated:
        return render_template("panier.html")
    else:
        return redirect(url_for('login'))

@app.route("/contact")
def contact():
    form=ContactForm()
    if form.validate_on_submit():
        email=form.email.data
        msg=form.message.data

    return render_template("contact.html",form=form)

@app.route("/apropos")
def apropos():
    return render_template("apropos.html")
# @app.route("/test")
# def test():
#     msg = Message('Hello', sender='egpouli@gmail.com', recipients=['egpouli@gmail.com'])
#     msg.body = "Mail avec Flask."
#     mail.send(msg)
#     return "Message sent!"

@app.route("/admin")
def admin():
    return render_template("admin.html")
# if __name__ == '__main__':
#     app.run(debug=True)

@app.route("/categories",methods=["POST","GET"])
def categories():
    form=CategorieForm()
    if form.validate_on_submit():
        nom=form.nom.data
        description=form.description.data

        cat=Categorie(nom=nom,description=description)
        db.session.add(cat)
        db.session.commit()
        flash("Catégorie créée")
        redirect(url_for('categories'))
    return render_template("ajoutCategorie.html",form=form)

@app.route("/adminProduits")
def adminProduits():
    categories = Categorie.query.order_by(Categorie.id).all()
    produit=Produit.query.join(Categorie).order_by(Produit.created_at)
    return render_template("adminProduits.html",produits=produit,categories=categories)

@app.route("/adminUser",methods=["GET","POST"])
def adminUser():
    user=Utilisateur.query.all()
    return render_template("adminUser.html",users=user)

@app.route("/addAdmin",methods=["POST","GET"])
def addAdmin():
    form=RegisterForm()
    if form.validate_on_submit():
        nom=form.nom.data
        prenom=form.prenom.data
        password=form.password.data
        retypePassword=form.retypePassword.data
        email=form.email.data
        file = request.files['file']
        if file.filename == '':
            filename = 'profil.png'
        if file and allowed_file(file.filename):
            filename = 'profil_'+secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if retypePassword==password:
            psw_hash=bcrypt.generate_password_hash(password).decode("utf8")
            user=Utilisateur(nom=nom,prenom=prenom,email=email,mot_pass=psw_hash,image=filename,admin=True)
            print(user)
            db.session.add(user)
            db.session.commit()
            flash("Utilisateur enregistré avec succès")
            redirect(url_for('login'))
        else:
            flash("Les mots de passe ne concordent pas")
    return render_template("register.html",form=form)

@app.route("/adminCategorie")
def adminCategorie():
    categorie=Categorie.query.all()
    return render_template("adminCategorie.html",categories=categorie)

@app.route("/profil")
def profil():
    if current_user.is_authenticated:
        return render_template("profil.html")
    else:
        return redirect(url_for('login'))