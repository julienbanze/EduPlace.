import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "eduplace_secret_123")

# Remplace par ton vrai lien Neon (URI) récupéré sur ton dashboard
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"Erreur de connexion : {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Ici on redirige vers l'accueil après connexion
        flash("Connexion réussie !", "success")
        return redirect(url_for('index'))
            
    return render_template('login.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # On récupère les données avec les "name" du HTML
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        promotion = request.form.get('promotion')
        matricule = request.form.get('matricule')

        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                # Assure-toi d'avoir créé cette table sur Neon
                cur.execute("""
                    INSERT INTO utilisateurs (nom, email, password, role, promotion, matricule) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nom, email, password, role, promotion, matricule))
                conn.commit()
                flash("Inscription réussie ! Connectez-vous.", "success")
                return redirect(url_for('login'))
            except Exception as e:
                conn.rollback()
                flash(f"Erreur : {e}", "danger")
            finally:
                cur.close()
                conn.close()
        else:
            flash("Erreur de base de données", "danger")

    return render_template('inscription.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
