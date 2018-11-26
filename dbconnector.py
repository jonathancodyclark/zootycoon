import pymysql
from flask import Flask, render_template, request, redirect, url_for, make_response, flash

app = Flask(__name__)

def execute_query(query):
    db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                         user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def concat_errors(error, new_error):
    if error == '':
        return new_error
    return error + " & " + new_error


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['username']
    resp = make_response('Setting cookie')
    resp.set_cookie('userID', user)
    return resp


    return render_template('test.html', getcookiefunction=getcookie)

@app.route('/getcookie', methods=['GET', 'POST'])
def getcookie():
    return request.cookies.get('userID')

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route("/login/result", methods=['GET', 'POST'])
def login_result():
    error = ''
    if request.method == "POST":
        attempted_username = request.form['username']
        attempted_password = request.form['password']
        if attempted_username == "admin" and attempted_password == "password":


            #first, set the cookie for user role so later html templates can read and render different views
            #url = 'http://localhost:5000/setcookie'
            #headers = {'Content-type': 'text/html; charset=UTF-8'}
            #response = requests.post(url, data=data, headers=headers)


            #then render next page
            return redirect(url_for('exhibits'))
        else:
            error = "Invalid credentials. Try again."
    return render_template('login.html', error=error)

@app.route("/register", methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route("/register/result", methods=['GET', 'POST'])
def register_result():
    error = ''
    if request.method == 'POST':
        attempted_username = request.form['username']
        attempted_email = request.form['email']
        attempted_pwd = request.form['password']
        attempted_pwd2 = request.form['confirmPassword']
        #CHECK IF USERNAME AND EMAIL UNIQUE
        query_result = execute_query("select * from users where username='" + attempted_username + "'")
        if bool(query_result) == True: #empty dictionaries evaluate to False
            error = concat_errors(error, 'username already exists')
        query_result = execute_query("select * from users where email='" + attempted_email + "'")
        if bool(query_result) == True:  # empty dictionaries evaluate to False
            error = concat_errors(error, 'email already exists')
        #PASSWORD CHECKS
        if len(attempted_pwd) < 8:
            error = concat_errors(error, 'password is fewer than 8 characters')
        if attempted_pwd != attempted_pwd2:
            error = concat_errors(error, 'passwords do not match')

        if error == '':
            #also need to insert into database here, remember to hash the password, also create this same value in either staff or visitors as well
            #also need to set cookie and log them in
            return redirect(url_for('exhibits'))
    return render_template('register.html', error=error)

@app.route("/exhibits", methods=['GET', 'POST'])
def exhibits():
    return render_template('exhibits.html', zoo_exhibits=execute_query("select * from exhibits"), title="Exhibits")

@app.route("/exhibits/details")
def exhibits_details():
    return render_template('exhibits_details.html')
