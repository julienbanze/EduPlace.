from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'Enseignant' / 'Eleve'
    classe = db.Column(db.String(50))
    matricule = db.Column(db.String(50))
    points = db.Column(db.Integer, default=0) # Système de récompense

class Cours(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    fichier = db.Column(db.String(200))
    classe_cible = db.Column(db.String(50))
    enseignant_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))

class Devoir(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100))
    contenu = db.Column(db.Text)
    date_limite = db.Column(db.DateTime)
    cours_id = db.Column(db.Integer, db.ForeignKey('cours.id'))

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valeur = db.Column(db.Float)
    eleve_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    devoir_id = db.Column(db.Integer, db.ForeignKey('devoir.id'))

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expediteur_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    destinataire_id = db.Column(db.Integer, db.ForeignKey('utilisateur.id'))
    contenu = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)