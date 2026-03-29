from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Utilisateur

auth = Blueprint('auth', __name__)

@auth.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        email = request.form.get('email')
        if Utilisateur.query.filter_by(email=email).first():
            flash("Email déjà utilisé", "danger")
            return redirect(url_for('auth.inscription'))

        role = request.form.get('role')
        hashed_pw = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256')
        
        if role == 'Enseignant':
            new_user = Utilisateur(nom=request.form.get('nom'), email=email, password=hashed_pw, role=role, matricule=request.form.get('matricule'))
        else:
            new_user = Utilisateur(nom=request.form.get('nom'), email=email, password=hashed_pw, role=role, classe=request.form.get('classe'), niveau=request.form.get('niveau'))

        db.session.add(new_user)
        db.session.commit()

        session.update({'user_id': new_user.id, 'user_nom': new_user.nom, 'user_role': new_user.role, 'user_classe': new_user.classe})
        return redirect(url_for('dashboard'))
    return render_template('inscription.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = Utilisateur.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password, request.form.get('password')):
            session.update({'user_id': user.id, 'user_nom': user.nom, 'user_role': user.role, 'user_classe': user.classe})
            return redirect(url_for('dashboard'))
        flash("Identifiants incorrects", "danger")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))