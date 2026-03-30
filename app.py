import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "cle_secrete_upl_2026")

# Lien Neon (Remplace par le tien si tu ne l'as pas mis dans Render)
DATABASE_URL = os.environ.get("DATABASE_URL", "TON_LIEN_NEON_ICI")

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        print(f"Erreur DB: {e}")
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
        # Logique d'inscription simplifiée
        return redirect(url_for('login'))
    return render_template('inscription.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
