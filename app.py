from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "seecars_secure_key_2026"

# BASES DE DATOS TEMPORALES
db_usuarios = []
db_vehiculos = []

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        nuevo_usuario = {
            "username": request.form.get('username'),
            "email": request.form.get('email'),
            "password": request.form.get('password'),
            "verificado": False
        }
        db_usuarios.append(nuevo_usuario)
        return redirect(url_for('verificar', email=nuevo_usuario['email']))
    return render_template('signup.html')

@app.route('/verificar/<email>', methods=['GET', 'POST'])
def verificar(email):
    if request.method == 'POST':
        if request.form.get('codigo') == "1234":
            for u in db_usuarios:
                if u['email'] == email:
                    u['verificado'] = True
            flash("Cuenta de SeeCars verificada. ¡Bienvenido!", "success")
            return redirect(url_for('login'))
        flash("Código incorrecto. Usa 1234", "danger")
    return render_template('verificar.html', email=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = next((u for u in db_usuarios if u['email'] == email and u['password'] == password), None)
        if user and user['verificado']:
            flash(f"¡Hola de nuevo en SeeCars, {user['username']}!", "primary")
            return redirect(url_for('index'))
        flash("Datos incorrectos o falta verificación.", "danger")
    return render_template('login.html')

@app.route('/')
def index():
    return render_template('index.html', vehiculos=db_vehiculos)

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nuevo_carro = {
            "id": len(db_vehiculos) + 1,
            "nombre": request.form['nombre'],
            "cedula": request.form['cedula'],
            "marca": request.form['marca'],
            "modelo": request.form['modelo'],
            "año": request.form['año'],
            "precio": request.form['precio'],
            "foto": request.files['foto'].filename
        }
        db_vehiculos.append(nuevo_carro)
        flash("Vehículo publicado exitosamente en SeeCars.ve", "success")
        return redirect(url_for('index'))
    return render_template('registro.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    v = next((item for item in db_vehiculos if item['id'] == id), None)
    if request.method == 'POST':
        v['modelo'] = request.form['modelo']
        v['precio'] = request.form['precio']
        flash("Publicación actualizada", "info")
        return redirect(url_for('index'))
    return render_template('editar.html', v=v)

@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    resultados = []
    if request.method == 'POST':
        mod = request.form.get('modelo', '').lower()
        año = request.form.get('año', '')
        resultados = [v for v in db_vehiculos if mod in v['modelo'].lower() or v['año'] == año]
    return render_template('buscar.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)