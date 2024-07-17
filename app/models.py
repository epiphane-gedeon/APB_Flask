from app import db
import datetime
from flask_login import UserMixin

class Utilisateur(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom= db.Column(db.String(50),unique=False,nullable=False)
    prenom= db.Column(db.String(50),unique=False,nullable=False)
    email= db.Column(db.String(50),unique=True,nullable=False)
    mot_pass= db.Column(db.String(50),unique=False,nullable=False)
    image=db.Column(db.String(50),unique=False,nullable=False)
    admin =db.Column(db.Boolean,unique=False,nullable=False,default=False)
    created_at=db.Column(db.Date,default=datetime.datetime.today())
    produit=db.relationship('Produit',backref='Utilisateur')
    contact=db.relationship('Categorie',backref='Utilisateur')
    
class Produit(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    image=db.Column(db.String(50),unique=False,nullable=False)
    nom= db.Column(db.String(50),unique=False,nullable=False)
    description= db.Column(db.String,unique=False,nullable=False)
    prix=db.Column(db.Integer,unique=False,nullable=False)
    created_at=db.Column(db.Date,default=datetime.datetime.today())
    user_id=db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    categorie=db.Column(db.Integer, db.ForeignKey('categorie.id'))

class Categorie(db.Model,UserMixin):
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom=db.Column(db.String(50),unique=True,nullable=False)
    description=db.Column(db.String,unique=False,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    produit=db.relationship('Produit',backref='Categorie')
