import os
from flask import Flask, render_template, request, redirect, url_for, flash

# 1. INITIALISATION (OBLIGATOIRE AU DÉBUT)
app = Flask(__name__)
app.secret_key = 'une_cle_secrete_au_choix' # Nécessaire pour les messages flash

# 2. LES ROUTES
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Ici, tu pourras ajouter ta logique de connexion plus tard
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == "admin" and password == "1234":
            return f"Bienvenue {username} ! Connexion réussie."
        else:
            return "Identifiants incorrects", 401
            
    return render_template('login.html')

# 3. CONFIGURATION POUR LE DÉPLOIEMENT (RENDER / GUNICORN)
if __name__ == '__main__':
    # On récupère le port défini par Render, sinon 5000 par défaut
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
