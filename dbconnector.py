import pymysql, time, datetime, requests
from flask import Flask, render_template, request, redirect, url_for, make_response, flash
from flask_hashing import Hashing

app = Flask(__name__)
hashing = Hashing(app)
db = pymysql.connect(host='academic-mysql.cc.gatech.edu', port=3306,
                         user='cs4400_group14', passwd='AMEb4bEi', db='cs4400_group14',
                         cursorclass=pymysql.cursors.DictCursor)
cursor = db.cursor()
current_exhibit = ''
current_user = ''

def set_current_exhibit(exhibit):
    current_exhibit = exhibit

def execute_query(query):
    cursor.execute(query)
    db.commit()

def concat_errors(error, new_error):
    if error == '':
        return new_error
    return error + " & " + new_error

'''
@app.route('/setcookie', methods=['POST'])
def setcookie():
    myusername = request.args.get('username')
    print requests.args.get('data')
    print myusername
    print type(myusername)
    resp = make_response('Setting cookie')
    resp.set_cookie('username', myusername)
    return resp
'''

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
        execute_query("SELECT * from users where username='" + attempted_username + "'")
        userTuple = cursor.fetchall() #will get us the one user if it exists
        if len(userTuple) == 0:
            error = "User does not exist"
        else:
            if hashing.check_value(userTuple[0].get("pwd"), attempted_password, salt='abcd'):
                #requests.post("http://localhost:5000/setcookie", data={'username': attempted_username})
                current_user = attempted_username
                #redirect to correct dashboard and check user type
                #STAFF USERS
                execute_query("SELECT * from staff where staff_name='" + attempted_username + "'")
                if len(cursor.fetchall()) != 0:
                    return redirect(url_for('staffFunctions'))
                #ADMIN USERS
                execute_query("SELECT * from admin where admin_name='" + attempted_username + "'")
                if len(cursor.fetchall()) != 0:
                    return redirect(url_for('adminFunctions'))
                #VISITOR USERS
                execute_query("SELECT * from visitors where vis_name='" + attempted_username + "'")
                if len(cursor.fetchall()) != 0:
                    return redirect(url_for('visitorFunctions'))
            else:
                error = "Invalid credentials. Try again."
            #first, set the cookie for user role so later html templates can read and render different views
            #headers = {'Content-type': 'text/html; charset=UTF-8'}
    return render_template('login.html', error=error)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    current_user=''
    return redirect(url_for('login'))

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
        #limit the possible length of the username and shit
        error = register_helper(attempted_username,
                                attempted_email,
                                attempted_pwd,
                                attempted_pwd2)
        if error == '':
            #REGISTER USER
            hashed_pwd = hashing.hash_value(attempted_pwd, salt='abcd')
            users_query = "INSERT INTO users(username, email, pwd) values('"+ attempted_username + "','"+ attempted_email + "','" + hashed_pwd + "')"
            execute_query(users_query)
            print('we get here')

            # REGISTER STAFF
            if request.form['action'] == 'Register Staff':
                staff_query = "INSERT INTO staff(staff_name) values('" + attempted_username + "')"
                execute_query(staff_query)
                return redirect(url_for('login'))
            # REGISTER VISITOR
            if request.form['action'] == 'Register Visitor':
                visitor_query = "INSERT INTO visitor(vis_name) values('" + attempted_username + "')"
                execute_query(visitor_query)
                return redirect(url_for('login'))

            #also need to set cookie and log them in
    return render_template('register.html', error=error)

@app.route("/staffFunctions", methods=['GET', 'POST'])
def staffFunctions():
    return render_template('staffFunctions.html')

@app.route("/visitorFunctions", methods=['GET', 'POST'])
def visitorFunctions():
    return render_template('visitorFunctions.html')

@app.route("/adminFunctions", methods=['GET', 'POST'])
def adminFunctions():
    return render_template('adminFunctions.html')

@app.route("/exhibitSearch", methods=['GET', 'POST'])
def exhibitSearch():
    return render_template('exhibitSearch.html')

@app.route("/exhibitSearch/result", methods=['GET', 'POST'])
def exhibitSearch_result():
    error = ''
    if request.method == 'POST':
        name = request.form['exhibitName']
        minAnimals = request.form['minAnimals']
        maxAnimals = request.form['maxAnimals']
        minSize = request.form['minSize']
        maxSize = request.form['maxSize']
        water = request.form['waterFeature']
        criteria1 = int(request.form['criteria1'])
        criteria2 = int(request.form['criteria2'])
        criteria3 = int(request.form['criteria3'])
        criteria4 = int(request.form['criteria4'])
        criteriaList = [criteria1, criteria2, criteria3, criteria4]
        base_query = "select * from exhibits AS e "
        finalCriteriaList=list()
        constraintSet=set()
        for cr in criteriaList:
            #for each criteria, add something to the query
            #this something is 1) contributes to the order (so append it into an ordered list) 2) add constraint to the query
            if cr == 0:
                print ("a criteria was ignored")
            if cr == 1:
                #filter by exhibit name
                if 'e.name_exhibit' not in finalCriteriaList:
                    finalCriteriaList.append('e.name_exhibit')
                constraintSet.add("e.name_exhibit = '" + name + "'")
            if cr == 2:
                #filter by num animals
                if 'd.num_animals' not in finalCriteriaList:
                    finalCriteriaList.append('d.num_animals')
                #here we add join table animals as d
                base_query += "RIGHT JOIN(select name_exhibit, COUNT(*) as num_animals from animals GROUP BY name_exhibit HAVING " \
                "count(*) >=" + minAnimals +" AND count(*) <=" + maxAnimals + ") as d on e.name_exhibit = d.name_exhibit"

            if cr == 3:
                #filter by exhibit size
                if 'e.size' not in finalCriteriaList:
                    finalCriteriaList.append('e.size')
                constraintSet.add("e.size <= " + maxSize)
                constraintSet.add("e.size >= " + minSize)
            if cr == 4:
                #filter by water feature
                if 'e.water_feature' not in finalCriteriaList:
                    finalCriteriaList.append('e.water_feature')
                constraintSet.add('water_feature=' + water)
        if 'e.name_exhibit' not in finalCriteriaList: #this column HAS to be added to reference the name of the exhibit for exhibit details page
            finalCriteriaList.append('e.name_exhibit')
        query=add_columns(base_query, finalCriteriaList)
        query=add_where_constraint(query, constraintSet)
        execute_query(query)
        allowedTupleKeys = list()
        for e in finalCriteriaList:
            allowedTupleKeys.append(e.split('.', 1)[1])
            print allowedTupleKeys
        return render_template('exhibitSearch.html', tuples=cursor.fetchall(), allowedTupleKeys=allowedTupleKeys)
    else:
        return render_template('exhibitSearch.html')

def add_where_constraint(base_query, constraintSet):
    if len(constraintSet) != 0:
        constraints = ' where '
        for c in constraintSet:
            constraints += c + ' AND '
        constraints = constraints[0:len(constraints) - 4] #get rid of last AND
        return base_query + constraints
    else:
        return base_query

def add_columns(base_query, columnList):
    if len(columnList) != 0: #if columnSet is not empty
        new_query = "select "
        for c in columnList:
            new_query += c
            new_query += ','
        new_query = new_query[:-1] #get rid of that last comma
        return new_query + base_query[8:len(base_query)] # remove select *
    else:
        return base_query

#def exhibit_table_link_helper(name_exhibit):
    #requests.post('http://127.0.0.1:5000/exhibitDetails', data={'name_exhibit': name_exhibit})

@app.route("/exhibitDetails", methods=['GET', 'POST'])
def exhibitDetails():
    name_exhibit = request.args.get('values', None)
    query = "select e.size,d.num_animals,e.name_exhibit,e.water_feature from exhibits AS e " \
            "RIGHT JOIN(select name_exhibit, COUNT(*) as num_animals from animals " \
            "GROUP BY name_exhibit) as d on e.name_exhibit = d.name_exhibit " \
            "where e.name_exhibit = '" + name_exhibit + "'"
    execute_query(query)
    singleTuple = cursor.fetchall()[0] #will only return the tuple with the name_exhibit which there is only 1
    size = singleTuple.get("size")
    num_animals = singleTuple.get("num_animals")
    water_feature = singleTuple.get("water_feature")
    return render_template('exhibitDetails.html', name_exhibit=name_exhibit, size=size, num_animals=num_animals, water_feature=water_feature)

@app.route("/logExhibitVisit", methods=['GET', 'POST'])
def logExhibitVisit():
    if request.method == 'POST':
        dt = datetime.datetime.now()
        vis_name = "jonathan"
        #r = requests.get(url=URL, params=PARAMS)
        #name_exhibit =
        #query="INSERT INTO "
        #execute_query(query)


def register_helper(username, email, pwd, pwd2):
    error = ''
    # CHECK IF USERNAME AND EMAIL UNIQUE
    query_result = execute_query("select * from users where username='" + username + "'")
    if bool(query_result) == True:  # empty dictionaries evaluate to False
        error = concat_errors(error, 'username already exists')
    query_result = execute_query("select * from users where email='" + email + "'")
    if bool(query_result) == True:  # empty dictionaries evaluate to False
        error = concat_errors(error, 'email already exists')
    # PASSWORD CHECKS
    if len(pwd) < 8:
        error = concat_errors(error, 'password is fewer than 8 characters')
    if pwd != pwd2:
        error = concat_errors(error, 'passwords do not match')
    return error


@app.route("/exhibits", methods=['GET', 'POST'])
def exhibits():
    return render_template('exhibits.html', title="Exhibits")

@app.route("/animalSearch",methods=['GET', 'POST'])
def animalSearch():
    if request.method == 'POST':
        name = request.form['exhibitName']
        minAnimals = request.form['minAnimals']
        maxAnimals = request.form['maxAnimals']
        minSize = request.form['minSize']
        maxSize = request.form['maxSize']
        water = request.form['waterFeature']
        criteria1 = int(request.form['criteria1'])
        criteria2 = int(request.form['criteria2'])
        criteria3 = int(request.form['criteria3'])
        criteria4 = int(request.form['criteria4'])

