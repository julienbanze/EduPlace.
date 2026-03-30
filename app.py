import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key_sauvegarde")

# --- CONFIGURATION BASE DE DONNÉES (NEON) ---
# Sur Render, tu devras ajouter une variable d'environnement nommée DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        return None

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Logique de vérification (exemple simplifié)
        if email == "admin@eduplace.com" and password == "1234":
            flash("Connexion réussie !", "success")
            return redirect(url_for('index'))
        else:
            flash("Identifiants incorrects", "danger")
            
    return render_template('login.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')

        # Exemple d'insertion dans Neon (PostgreSQL)
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Assure-toi que ta table 'utilisateurs' existe sur Neon
                cur.execute("INSERT INTO utilisateurs (nom, email, password) VALUES (%s, %s, %s)",
                            (nom, email, password))
                conn.commit()
                flash("Compte créé avec succès !", "success")
                return redirect(url_for('login'))
            except Exception as e:
                conn.rollback()
                flash(f"Erreur lors de l'inscription : {e}", "danger")
            finally:
                cur.close()
                conn.close()
        else:
            flash("Erreur de connexion au serveur de données", "danger")

    return render_template('inscription.html')

# --- LANCEMENT ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
