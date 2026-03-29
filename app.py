import os
from flask import Flask, render_template, session, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from models import db, Utilisateur, Cours, Message

app = Flask(__name__)

# --- CONFIGURATION NEON ---
# Remplace la ligne ci-dessous par ton lien Neon complet
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
app.config['SECRET_KEY'] = 'eduplace_secret_2026'
app.config['UPLOAD_FOLDER'] = 'static/uploads/cours'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)
with app.app_context():
    db.create_all()

# --- ROUTES ---

@app.route('/')
def index():
    return redirect(url_for('inscription'))

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        pw = generate_password_hash(request.form['password'])
        new = Utilisateur(nom=request.form['nom'], email=request.form['email'], 
                          password=pw, role=request.form['role'],
                          classe=request.form.get('classe'), matricule=request.form.get('matricule'))
        db.session.add(new)
        db.session.commit()
        session.update({'u_id': new.id, 'u_role': new.role, 'u_nom': new.nom, 'u_classe': new.classe})
        return redirect(url_for('dashboard'))
    return render_template('inscription.html')

@app.route('/dashboard')
def dashboard():
    if 'u_id' not in session: return redirect(url_for('inscription'))
    u = Utilisateur.query.get(session['u_id'])
    if u.role == 'Enseignant':
        c = Cours.query.filter_by(enseignant_id=u.id).all()
        return render_template('dash_prof.html', user=u, cours=c)
    c = Cours.query.filter_by(classe_cible=u.classe).all()
    return render_template('dash_eleve.html', user=u, cours=c)

@app.route('/publier', methods=['POST'])
def publier():
    f = request.files.get('fichier')
    if f:
        fname = secure_filename(f.filename)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], fname))
        db.session.add(Cours(titre=request.form['titre'], description=request.form['desc'], 
                             fichier=fname, classe_cible=request.form['classe'], enseignant_id=session['u_id']))
        db.session.commit()
    return redirect(url_for('dashboard'))

# ADMIN PANEL
@app.route('/admin=julien', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST' and request.form.get('pw') == 'julien':
        session['is_admin'] = True
    if not session.get('is_admin'): return render_template('admin_lock.html')
    return render_template('admin_master.html', users=Utilisateur.query.all())

if __name__ == '__main__':
    app.run(debug=True)