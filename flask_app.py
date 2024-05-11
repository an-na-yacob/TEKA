# A very simple Flask Hello World app for you to get started with...

from flask import Flask, render_template, url_for, request, redirect, session
from flask_mysqldb import MySQL
import MySQLdb


app = Flask(__name__)
app.secret_key = 'Debugus123'

# Configure MySQL connection
# ...

# Set up static URL path and folder
app.static_url_path = '/static'
app.static_folder = 'static'

# Set up template folder
app.template_folder = 'templates'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Password1!'
app.config['MYSQL_DB'] = 'Debugus'

db = MySQL(app)

app.secret_key = 'Debugus123'


@app.route('/',methods=['POST','GET'])
def homepage():
    return render_template("homepage.html")


@app.route('/login', methods=['POST','GET'])
def login():
    msg=''
    if request.method == 'POST':
        if 'email' in request.form and 'password' in request.form:
            email = request.form['email']
            password = request.form['password']
            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email=%s AND password=%s',(email,password))
            info = cursor.fetchone()
        if info is not None:
            if email == info['email'] and password == info['password']:
                session['logged in'] = True
                session['username'] = info['username']
                session['email'] = info['email']
                session['password'] = info['password']
                return redirect(url_for('profile'))
        else:
            msg="Invalid email/password"

    return render_template("loginpage.html", msg=msg)


@app.route('/signup', methods=['POST','GET'])
def signup(msg=''):
    if request.method == 'POST':
        if 'username' in request.form and 'email' in request.form and 'password' in request.form:
            username=request.form['username']
            email = request.form['email']
            password = request.form['password']

            cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM accounts WHERE email like %s', (email,))
            info = cursor.fetchone()

            if info is not None:
                msg='Account already exists'
            else:
                cursor.execute("INSERT INTO accounts(username,email,password) VALUES (%s,%s,%s)",(username,email,password))
                db.connection.commit()
                return redirect("loginpage.html")

    return render_template("signuppage.html",msg=msg)
    

@app.route('/profile', methods=['POST','GET'])
def profile():
    if session['logged in'] == True:
        return render_template('profilepage.html', username=session['username'], email=session['email'], password=session['password'])


@app.route('/edit', methods=['POST','GET'])
def edit():
    if session['logged in'] == True:
        return render_template('edit.html', username=session['username'], email=session['email'], password=session['password'])


@app.route('/submit', methods=['POST','GET'])
def submit():
    username=request.form['username']
    password = request.form['password']

    cursor = db.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("update accounts set username=%s,password=%s where email=%s",(username,password,session['email']))
    db.connection.commit()
            
    session['username'] = username
    session['password'] = password

    return redirect(url_for('profile'))

@app.route('/logout')
def logout():
    session.pop('logged in',None)
    return redirect("homepage.html")


if __name__ == '__main__':
    app.run(debug=True)

