# ... (Gardez le début du code précédent) ...

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = Utilisateur.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            if user.role == 'Eleve': return redirect(url_for('dashboard_eleve'))
            return redirect(url_for('dashboard_enseignant'))
        
        flash("Email ou mot de passe incorrect", "danger")
    return render_template('login.html')

@app.route('/dashboard_eleve')
def dashboard_eleve():
    if session.get('role') != 'Eleve': return redirect(url_for('login'))
    user = Utilisateur.query.get(session['user_id'])
    return render_template('dashboard_eleve.html', user=user)

@app.route('/dashboard_enseignant')
def dashboard_enseignant():
    if session.get('role') != 'Enseignant': return redirect(url_for('login'))
    user = Utilisateur.query.get(session['user_id'])
    return render_template('dashboard_enseignant.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
