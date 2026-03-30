import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "eduplace_secret_key_2026"

# ==========================================================
# 🟢 COLLE TON LIEN NEON CI-DESSOUS ENTRE LES GUILLEMETS 🟢
# ==========================================================
DATABASE_URL = "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require" 
# ==========================================================

def get_db_connection():
    try:
        # Connexion sécurisée à Neon
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion à Neon : {e}")
        return None

# --- ROUTE ACCUEIL ---
@app.route('/')
def index():
    return render_template('index.html')

# --- ROUTE INSCRIPTION ---
@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # On récupère les données de ton formulaire
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        promotion = request.form.get('promotion')
        matricule = request.form.get('matricule')

        # Enregistrement dans la base Neon
        conn = get_db_connection()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO utilisateurs (nom, email, password, role, promotion, matricule) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (nom, email, password, role, promotion, matricule))
                conn.commit()
                cur.close()
                conn.close()
                # Une fois fini, on va vers la plateforme
                return redirect(url_for('plateforme'))
            except Exception as e:
                print(f"❌ Erreur SQL : {e}")
                return redirect(url_for('plateforme')) # Redirige quand même pour tester le design
        else:
            # Si la DB ne marche pas, on accède quand même à la plateforme pour le test
            return redirect(url_for('plateforme'))
            
    return render_template('inscription.html')

# --- ROUTE LOGIN ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('plateforme'))
    return render_template('login.html')

# --- ROUTE PLATEFORME (Celle avec l'image) ---
@app.route('/plateforme')
def plateforme():
    return render_template('plateforme.html')

if __name__ == '__main__':
    # Configuration pour Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
