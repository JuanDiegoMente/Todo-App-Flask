""" Seremos mejores que los que estan codiando esto! """

# 7/6/21
# Muchas gracias por tomarte el tiempo de ver esto <3 :D
import random
from flask import Flask, render_template, redirect, url_for
from flask import request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.security import generate_password_hash, check_password_hash
from sugerencias import create_sugerencia_username
import threading
from flask_mail import Mail
from flask_mail import Message
from val_password import validarPassword
from datetime import date


# --> Configuracion basica
rutaDB = "sqlite:///" + os.path.abspath(os.getcwd()) + "/basedatos.db"
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = rutaDB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'aunnada'

# --> Configuracion correos
app.config['DEBUG'] = True
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
# El correo que ponga aca debe tener permisos
app.config['MAIL_USERNAME'] = "correo"
app.config['MAIL_PASSWORD'] = "password"
app.config['MAIL_DEFAULT_SENDER'] = 'juandiegop.m554@gmail.com'
app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_ASCII_ATTACHMENTS'] = True

# --> Variables globales para el programa
mail = Mail(app)
codigo = 0
se_incio_sesion = False
db = SQLAlchemy(app)


def emails(info_for_html: dict, template: str, repectores: list, title: str) -> None:
    """ Basicamente una funcion para enviar correos con plantilla HTML """
    msg = Message(title, recipients=repectores)
    msg.html = render_template(template, data=info_for_html)
    mail.send(msg)



# --> Bases de datos
class BaseDatos_Usurios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    happyBirthDay = db.Column(db.String(25), unique=False, nullable=False)

class BaseDatos_Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(600), nullable=False)
    start_date = db.Column(db.String(20), nullable=False)
    end_date = db.Column(db.String(20), nullable=False)
    # Estas columnas son para saber si el usurio esta interesado
    # en recibir y que lo alertemos sobre que su tarea esta a punto
    # de vencer etc...
    important = db.Column(db.Integer, nullable=False)

# INSERT INTO base_datos__tasks VALUES (1, "Prueba", "Es un aprueba", "hoy", "hoy", 0, 1, 1);


# Ruta principales INDEX ---------------------------------------------------------------->
@app.route("/")
def index():
    return render_template('index.html')


# Ruta crear cuenta ------------------------------------------------------------------>
@app.route("/crear_cuenta", methods=['GET', 'POST'])
def create_account():

    if request.method == 'POST':
        """ Encriptando contraseña """
        password_encrypted = generate_password_hash(request.form['password'], method='sha256')

        """ Verificamos que no haya un usurio con los mismos datos """
        consultaDB = BaseDatos_Usurios.query.filter_by(username=request.form['username']).first()
        if consultaDB:
            """ Le damos algunas suguerencias al usuario """
            sug = []
            for i in range(5):
                sug.append(create_sugerencia_username(request.form['username']))
            data = {
                "nameDefault" : request.form['username'],
                "sug" : sug,
                "correo" : request.form['email'] == consultaDB.email
            }
            return render_template('user_exist.html', datos=data)

        else:
            newUser = BaseDatos_Usurios(
                username=request.form['username'],
                email=request.form['email'],
                password=password_encrypted,
                happyBirthDay=request.form['date_happy']
            )
            db.session.add(newUser)
            db.session.commit()

            return redirect(url_for("inicio_sesion"))


    return render_template('crear_cuenta.html')

@app.route('/borrar/<int:id>/accountask/<string:user>')
def borrar_task(id, user):
    try:
        db.session.query(BaseDatos_Tasks).filter(BaseDatos_Tasks.id == id).delete()
        db.session.commit()
        return redirect(url_for('home', user=user))
    except:
        return redirect(url_for('error404'))

@app.route("/home/<string:user>/", methods=['GET', 'POST'])
def home(user):
    if se_incio_sesion:
        if request.method == 'POST':
            title_ = request.form['title']
            desc = request.form['description']
            fechaLim = request.form['fecha-limite']
            importante = 0
            """ Operador ternario no existe en Python """
            if (request.form['important'].lower() == 'yes') :
                importante = 1

            newTask = BaseDatos_Tasks(
                title=title_,
                description=desc,
                start_date=str(date.today()),
                end_date=fechaLim,
                important=importante,
            )

            db.session.add(newTask)
            db.session.commit()

        query = db.session.query(BaseDatos_Tasks).filter(BaseDatos_Tasks.id >= 1).all()

        dataFor_html = {
            "username" : user,
            "tasks" : query
        }

        return render_template('home.html', data=dataFor_html)
    else:
        return redirect(url_for('inicio_sesion'))


# Ruta iniciar sesion ------------------------------------------------------------------>
@app.route("/inicio_sesion", methods=['GET', 'POST'])
def inicio_sesion():
    if request.method == 'POST':
        user_ = BaseDatos_Usurios.query.filter_by(username=request.form['username']).first()
        if user_ and check_password_hash(user_.password, request.form['password']):
            global se_incio_sesion
            se_incio_sesion = True
            return redirect(url_for('home', user=user_.username))

        else:
            """ Mandamos un flash por si el usuario no fue encontrado """
            flash(" El usuario no fue encontrado!!")


    return render_template('iniciar_sesion.html')


@app.route("/iniciar_sesion/olvido", methods=['GET', 'POST'])
def olvido_password():
    if request.method == 'POST':
        correo_dado = request.form['email']
        busquedaCorreo = BaseDatos_Usurios.query.filter_by(email=correo_dado).first()

        if busquedaCorreo:
            """ Generamos el codigo """
            global codigo
            codigo = random.randint(100000, 999999)

            data = {
                "code" : codigo,
                "username" : busquedaCorreo.username
            }

            """ Mandamos el correo """
            correo_th = threading.Thread(
                target=emails,
                args=(data, "email.html", [correo_dado], "Codigo recuperacion - ToDo App Flask")
            )
            correo_th.run()

            return redirect(url_for('ingresarCode', email=correo_dado, username=busquedaCorreo.username))

        else:
            flash(" El correo no esta en la base de datos!")

    return render_template('olvido_password_i.html')



@app.route("/inicio_sesion/olvido/<string:email>/<string:username>/", methods=['GET', 'POST'])
def ingresarCode(email, username):
    if codigo != 0:
        if request.method == 'POST':
            codeInput = request.form['codeInput']
            """ Lo pasamos a entero ya que nos llega de forma str """
            if int(codeInput) == codigo:
                return redirect(url_for('cambiar_password', username=username, code=codeInput))

            else:
                flash(" Los códigos no coinciden, revisa bien!")


        data = {
            "email" : email,
            "name" : username
        }
        return render_template('olvido_password_ii.html', data=data)

    else:
        return render_template('error404.html')


@app.route("/cambiar_password/<string:username>/<int:code>/", methods=['GET', 'POST'])
def cambiar_password(username, code):
    """ Esto porque aun no sabemos como hacer que las url sean mas seguras?
     entonces verificamos para que no simplemente escriba un numero de 6 cifras
     y ya"""
    if code == codigo:
        if request.method == 'POST':
            newPass1 = request.form['passCamp1']
            newPass2 = request.form['passCamp2']

            if ( (newPass1 == newPass2) and (len(newPass2) >= 6) and (validarPassword(newPass1)) ):
                cambioUser = BaseDatos_Usurios.query.filter_by(username=username).first()
                cambioUser.password = generate_password_hash(newPass1, method='sha256')
                db.session.commit()

                return redirect(url_for('index'))

            elif (newPass1 != newPass2):
                flash(" Las contraseñas no coinciden")

            if not validarPassword(newPass1):
                flash(" La contraeña debe ser más segura")


        return render_template('olvido_password_iii.html')

    else:
        return render_template('error404.html')




@app.errorhandler(404)
def error404(e):
    return render_template('error404.html'), 404



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)











