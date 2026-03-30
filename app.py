import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "eduplace_ia_2026_key"

DATABASE_URL = "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_db_connection():
    try:
        return psycopg2.connect(DATABASE_URL, sslmode='require')
    except:
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        classe = request.form.get('classe')
        matiere = request.form.get('matiere')
        
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO utilisateurs (nom, email, password, role, classe, matiere) VALUES (%s, %s, %s, %s, %s, %s)",
                        (nom, email, password, role, classe, matiere))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('login'))
    return render_template('inscription.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            cur.execute("SELECT id, nom, role, classe, matiere FROM utilisateurs WHERE email=%s AND password=%s", (email, password))
            user = cur.fetchone()
            cur.close()
            conn.close()
            if user:
                session.update({'user_id': user[0], 'nom': user[1], 'role': user[2], 'classe': user[3], 'matiere': user[4]})
                return redirect(url_for('plateforme'))
    return render_template('login.html')

@app.route('/plateforme')
def plateforme():
    if 'user_id' not in session: return redirect(url_for('login'))
    if session['role'] == 'Enseignant':
        return render_template('dashboard_enseignant.html', user=session)
    else:
        return render_template('dashbord_eleve.html', user=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
