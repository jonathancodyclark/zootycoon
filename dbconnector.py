import pymysql
from flask import Flask, render_template, request, redirect, url_for, make_response, flash

app = Flask(__name__)

db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                         user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14',
                         cursorclass=pymysql.cursors.DictCursor)

cursor = db.cursor()
cursor.execute("select * from exhibits")
zoo_exhibits = cursor.fetchall()


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

@app.route("/exhibits", methods=['GET', 'POST'])
def exhibits():
    return render_template('exhibits.html', zoo_exhibits=zoo_exhibits, title="Exhibits")

@app.route("/exhibits/details")
def exhibits_details():
    return render_template('exhibits_details.html')
