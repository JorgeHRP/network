from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import json
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'netconnect_secret_key_2026'

# Configurações
MOCK_EMAIL = 'Jorge@email.com'
MOCK_PASSWORD = '123456'

# Carregar dados JSON
def load_json(filename):
    with open(f'data/{filename}', 'r', encoding='utf-8') as f:
        return json.load(f)

# Decorator para rotas protegidas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Rotas
@app.route('/')
def index():
    if 'logged_in' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        
        if email == MOCK_EMAIL and password == MOCK_PASSWORD:
            session['logged_in'] = True
            session['user_email'] = email
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Credenciais inválidas'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/membros')
@login_required
def membros():
    return render_template('membros.html')

@app.route('/referencias')
@login_required
def referencias():
    return render_template('referencias.html')

# API Endpoints
@app.route('/api/user-data')
@login_required
def get_user_data():
    return jsonify(load_json('user-data.json'))

@app.route('/api/contacts')
@login_required
def get_contacts():
    search = request.args.get('search', '').lower()
    contacts = load_json('contacts.json')
    
    if search:
        contacts = [c for c in contacts if 
                   search in c['name'].lower() or 
                   search in c['company'].lower() or 
                   search in c['sector'].lower()]
    
    return jsonify(contacts)

@app.route('/api/events')
@login_required
def get_events():
    return jsonify(load_json('events.json'))

@app.route('/api/reference', methods=['POST'])
@login_required
def create_reference():
    data = request.get_json()
    # Aqui você salvaria no banco de dados
    # Por enquanto apenas retorna sucesso
    return jsonify({
        'success': True,
        'message': 'Referência criada com sucesso!',
        'commission': float(data.get('value', 0)) * 0.05
    })

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
