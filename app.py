import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Utilisateur
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configuration Base de Données (Neon)
uri = os.getenv("DATABASE_URL")
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = uri or 'sqlite:///eduplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'UPL_AI_2026_SECRET'

db.init_app(app)

# Création des tables au lancement
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user_exists = Utilisateur.query.filter_by(email=email).first()
        if user_exists:
            flash('Cet email est déjà utilisé !', 'danger')
            return redirect(url_for('inscription'))

        new_user = Utilisateur(
            nom=nom,
            email=email,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            role=role,
            classe=request.form.get('classe'),
            matiere=request.form.get('matiere'),
            matricule=request.form.get('matricule')
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Compte créé avec succès !', 'success')
        return redirect(url_for('index'))
    
    return render_template('inscription.html')

# --- ACCÈS ADMIN SPÉCIAL ---
@app.route('/admin=julien', methods=['GET', 'POST'])
def admin_panel():
    if request.method == 'POST':
        mdp = request.form.get('admin_password')
        if mdp == "UPL2026": # Ton mot de passe secret
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Accès refusé !', 'danger')
    return render_template('admin_login.html')

@app.route('/dashboard_admin')
def admin_dashboard():
    if not session.get('admin'): return redirect(url_for('admin_panel'))
    utilisateurs = Utilisateur.query.all()
    return render_template('admin_dashboard.html', users=utilisateurs)

if __name__ == '__main__':
    app.run(debug=True)
