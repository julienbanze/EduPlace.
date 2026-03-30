import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "eduplace_full_v1_2026"

# CONFIGURATION NEON
DATABASE_URL = "postgresql://neondb_owner:npg_TwHBF0davIf2@ep-wispy-union-am1qz45m-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if request.method == 'POST':
        data = request.form
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO utilisateurs (nom, email, password, role, classe, matiere) VALUES (%s,%s,%s,%s,%s,%s)",
                    (data['nom'], data['email'], data['password'], data['role'], data['classe'], data.get('matiere')))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('inscription.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email, pwd = request.form['email'], request.form['password']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, nom, role, classe FROM utilisateurs WHERE email=%s AND password=%s", (email, pwd))
        user = cur.fetchone()
        if user:
            session.update({'id': user[0], 'nom': user[1], 'role': user[2], 'classe': user[3]})
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'id' not in session: return redirect(url_for('login'))
    conn = get_db_connection()
    cur = conn.cursor()
    
    if session['role'] == 'Enseignant':
        cur.execute("SELECT * FROM lecons WHERE enseignant_id=%s", (session['id'],))
        cours = cur.fetchall()
        return render_template('dashboard_enseignant.html', cours=cours)
    else:
        cur.execute("SELECT * FROM lecons WHERE classe_cible=%s", (session['classe'],))
        cours = cur.fetchall()
        return render_template('dashbord_eleve.html', cours=cours)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
