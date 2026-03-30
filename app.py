import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cle_secrete_upl_2026")

# Configuration Neon
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        print(f"Erreur de connexion DB: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # Logique d'inscription ici
        flash("Inscription réussie !", "success")
        return redirect(url_for('login'))
    return render_template('inscription.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
