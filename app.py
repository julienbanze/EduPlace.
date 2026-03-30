import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "cle_secrete_eduplace"

# Remplace par ton lien Neon
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # On simule la connexion pour l'instant pour que tu accèdes à la plateforme
        return redirect(url_for('plateforme'))
    return render_template('login.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # On récupère les infos du formulaire
        nom = request.form.get('nom')
        email = request.form.get('email')
        
        # Enregistrement dans Neon
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO utilisateurs (nom, email) VALUES (%s, %s)", (nom, email))
            conn.commit()
            cur.close()
            conn.close()
            
        # APRES L'INSCRIPTION, ON ACCÈDE À LA PLATEFORME
        return redirect(url_for('plateforme'))
    
    return render_template('inscription.html')

@app.route('/plateforme')
def plateforme():
    # C'est ici que ton application commence vraiment
    return "<h1>Bienvenue sur la plateforme EduPlace !</h1><p>Le système est prêt.</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
