import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "eduplace_secret_2026"

# Remplace par ton lien Neon
DATABASE_URL = "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        # (Logique d'inscription ici...)
        return redirect(url_for('plateforme'))
    return render_template('inscription.html')

@app.route('/plateforme')
def plateforme():
    # Simulation de cours avec des images cool
    cours_disponibles = [
        {"titre": "Intelligence Artificielle", "img": "https://images.unsplash.com/photo-1677442136019-21780ecad995"},
        {"titre": "Développement Web", "img": "https://images.unsplash.com/photo-1498050108023-c5249f4df085"},
        {"titre": "Base de Données SQL", "img": "https://images.unsplash.com/photo-1544383835-bda2bc66a55d"}
    ]
    return render_template('plateforme.html', cours=cours_disponibles)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
