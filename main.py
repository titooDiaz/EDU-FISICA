from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'
app.template_folder = 'templates'
app = Flask(__name__, static_folder='static')


# Ruta principal
@app.route('/')
def home():
    # Verificar si hay un nombre de usuario almacenado en la sesión
    if 'username' in session:
        username = session['username']
        #return f'Bienvenido, {username}'
        return render_template('index.html')
    else:
        #return f'Bienvenido'
        return render_template('index.html')
    

@app.route('/tienda/')
def tienda():
    # Verificar si hay un nombre de usuario almacenado en la sesión
    if 'username' in session:
        username = session['username']
        #return f'Bienvenido, {username}'
        return render_template('tienda.html')
    else:
        #return f'Bienvenido'
        return render_template('tienda.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Conexión a la base de datos
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Verificar si el usuario ya existe en la base de datos
        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()

        if existing_user:
            return 'El nombre de usuario ya está en uso'
        else:
            # Insertar el nuevo usuario en la base de datos
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()

            # Almacenar el nombre de usuario en la sesión
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('register.html')




# Ruta para el formulario de inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Conexión a la base de datos
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        # Verificar si el usuario existe en la base de datos
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()

        if user:
            # Almacenar el nombre de usuario en la sesión
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Nombre de usuario o contraseña incorrectos'

    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    # Remover el nombre de usuario de la sesión
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    # Crear la tabla de usuarios en la base de datos (si no existe)
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

    app.run(debug=True)
