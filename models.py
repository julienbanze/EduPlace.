from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Utilisateur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False) # 'Admin', 'Enseignant', 'Eleve'
    
    # Champs spécifiques
    classe = db.Column(db.String(50))      # Pour élèves et profs
    matiere = db.Column(db.String(100))    # Pour profs
    matricule = db.Column(db.String(50))   # Pour élèves
    telephone = db.Column(db.String(20))
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Utilisateur {self.nom}>'
