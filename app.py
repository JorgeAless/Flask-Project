from flask import Flask, redirect, render_template, flash, request, session, url_for
from flask_mysqldb import MySQL


# Configuracion flask
app = Flask('__main__')
app.secret_key = 'mysecretKey'

# Configuración MySQL
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@merica.85'
app.config['MYSQL_DB'] = 'bdo_pec'

# Formulario Index
@app.route('/')
@app.route('/index.html')
def Index():
    return render_template('/index.html')

# Formulario Contacto
@app.route('/contacto')
def contacto():
    usuario_activo = session.get('id_user')  # validar sesión activa
    print('Usuario en sesion ', usuario_activo)
    if usuario_activo is None:  # valida si el usuario está activo
        flash(f"Sesión inactiva, vuelva a iniciar sesión","information")
        return redirect(url_for('Index'))
    return render_template('/contacto.html')

# Funcion usuario
def usuario_active():
    user_active = session.get('id_user')
    if user_active is None:
        flash(f"Sesión inactiva, vuelva a iniciar sesión","information")
        return redirect(url_for('Index'))

# Formulario Login
@app.route('/login', methods=['POST'])
def Login():
    cur = mysql.connection.cursor()  # conexion bdo
    username = request.form['user']
    password = request.form['password']
    print('Usuario: ', username)
    error = None
    cur.execute('SELECT * FROM tb_user WHERE usuario_nombre = %s AND usuario_password = %s',
                (username, password,))  # consulta bdo
    user = cur.fetchone()
    if user is None:
        flash(f"¡Usuario o contraseña incorrecta!", "error")
        return redirect(url_for('Index'))
    # iniciar sesión
    print('Impresion ', user)
    id_user = user[0]
    session['id_user'] = id_user
    session['name_user'] = username
    cur.execute(
        'SELECT * FROM tb_escuelas WHERE id_user = {0}'.format(id_user))
    escuela = cur.fetchall()
    # Dirigir a la plantilla escuelas
    return render_template('/escuelas.html', escuelas=escuela, id_reg=username)

# Logout
@app.route('/logout')
def LogOut():
    session.clear()
    return redirect(url_for('Index'))

# Buscar
@app.route('/search', methods=['POST'])
def Buscar_escuela():
    cct = request.form['cct']
    cur = mysql.connection.cursor()
    escuela = None
    cur.execute('SELECT * FROM tb_escuelas WHERE escuela_cct = %s', (cct,))
    escuela = cur.fetchall()
    print('qUE TRAIIII ', escuela)
    if not escuela:
        flash(f"¡La escuela no está registrada!", "warning")
        return redirect(url_for('recarga'))
    print('Escuela ', escuela)
    return render_template('/escuelas.html', escuelas=escuela)

# Recargar_Escuelas
@app.route('/rescuelas')
def recarga():
    id_usuario = session.get('id_user')
    cur = mysql.connection.cursor()
    cur.execute(
        'SELECT * FROM tb_escuelas WHERE id_user = {0}'.format(id_usuario))
    escuela = cur.fetchall()
    return render_template('/escuelas.html', escuelas=escuela)

# Eliminar registro
@app.route('/delete/<id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tb_escuelas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash(f"Se eliminó la escuela.", "success")
    return redirect(url_for('recarga'))

# Editar registro
@app.route('/edit/<id>')
def editarEscuela(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tb_escuelas WHERE id = {0}'.format(id))
    datos = cur.fetchall()
    return render_template('editarEscuela.html', escuela=datos[0])

# Actualizar datos
@app.route('/update/<id>', methods=['POST'])
def updateEscuela(id):
    if request.method == 'POST':
        cct = request.form['cct']
        nombre = request.form['nombre']
        municipio = request.form['municipio']
        localidad = request.form['localidad']
        cur = mysql.connection.cursor()
        cur.execute(
            'UPDATE tb_escuelas set escuela_cct = %s, escuela_nombre = %s, escuela_municipio = %s, escuela_localidad = %s WHERE id = %s',(cct, nombre,
            municipio, localidad, id))
        mysql.connection.commit()
        flash(f"Datos actualizados correctamente","success")
        return redirect(url_for('recarga'))

#Registrar nueva escuela
@app.route('/register')
def registrarE():
    return render_template('registro.html')
@app.route('/registrar', methods = ['POST'])
def insert():
    if request.method == 'POST':
        id_user = session.get('id_user')
        cctN = request.form['cctN']
        nombreN = request.form['nombreN']
        locN = request.form['locN']
        munN = request.form['munN']
        dirN = request.form['dirN']
        region = request.form['region']
        cur =mysql.connection.cursor()
        cur.execute('INSERT INTO tb_escuelas (escuela_cct, escuela_nombre, escuela_municipio, escuela_localidad, id_user) VALUES(%s, %s, %s, %s, %s)', [cctN, nombreN, locN, munN, id_user])
        mysql.connection.commit()
        flash(f"Se registro la escuela satisfactoriamente.", "success")
        return redirect(url_for('recarga'))


# Iniciar aplicación
if __name__ == '__main__':
    app.run(port=8080, debug=True)
