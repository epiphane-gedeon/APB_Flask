from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField,TextAreaField,FileField,DateField,IntegerField,SelectField,SearchField
from wtforms.validators import DataRequired,Length,Email
from wtforms.widgets import PasswordInput
from app.models import Categorie

from app import app,db,bcrypt,login_manager,mail
from flask import render_template,flash,redirect,url_for
from app.models import Utilisateur,Produit,Categorie
from flask_login import login_user
from flask_mail import Message

class LoginForm(FlaskForm):
    email=EmailField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Mot de passe',widget=PasswordInput(hide_value=False),validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Connexion')

class RegisterForm(FlaskForm):
    nom=StringField('Nom',validators=[DataRequired(),Length(min=2,max=20)])
    prenom=StringField('Prenom',validators=[DataRequired(),Length(min=2,max=20)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Mot de passe',widget=PasswordInput(hide_value=False),validators=[DataRequired()])
    retypePassword=PasswordField('Confirmer mot de passe',widget=PasswordInput(hide_value=False),validators=[DataRequired()])
    image=FileField(name='file',render_kw={'id': 'upload'})
    submit=SubmitField('Inscription')

class ProductForm(FlaskForm):
    file=FileField(validators=[DataRequired()],name='file',render_kw={'id': 'upload'})
    nom=StringField('Nom',validators=[DataRequired()])
    description=StringField('Description',validators=[DataRequired()])
    # categorie=StringField('Categorie',validators=[DataRequired()])
    categorie = SelectField(choices=['Catégotie'])
    prix=IntegerField('Prix',validators=[DataRequired()])

    submit=SubmitField('Ajouter')

class ContactForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    message=TextAreaField('Message',validators=[DataRequired()])
    submit=SubmitField('Envoyer')

class CategorieForm(FlaskForm):
    nom=StringField('Nom',validators=[DataRequired()])
    description=TextAreaField('Description',validators=[DataRequired()])
    submit=SubmitField('Ajouter')

class CartForm(FlaskForm):
    quantite=IntegerField('Quantite',validators=[DataRequired()],render_kw={'value': 1,'min': 1,'class':'quantite'})
    submit=SubmitField('Ajouter au panier',render_kw={'class':'achat'})