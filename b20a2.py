from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
from sqlalchemy.sql import text
app.secret_key='topsecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
db = SQLAlchemy(app)



@app.route('/')
def index():
    if 'username' not in session:
        return redirect("/login.html")

@app.route('/login',methods=['GET','POST'])
def login():
    # pulls all the relevant info(username, password) from the login table
    if request.method=='POST':
        sql = """
            SELECT username, password
            FROM Login
            """
        # executes the sql
        results = db.engine.execute(text(sql))
        # will attempt to find a matching username/password combo
        for result in results:
            if result['username']==request.form['username']:
                if result['password']==request.form['password']:
                    # sets the session['username'] to the successful username and redirects the user to index.html
                    session['username']=request.form['username']
                    return redirect("index.html")
        # no matching pair was found, tell them to try again
        return '''<h1>Incorrect UserName/Password</h1>
                  <a href= "login.html">Please try again</a>
                '''
    # user is already logged in so redirect them to index.html
    elif 'username' in session:
        return redirect("index.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/login.html")

@app.route('/add_user', methods=['POST'])
def add_user ():
    # pulls all created usernames from the server
    if request.method=='POST':
        sql = """
        SELECT username
        FROM login
        """
    results = db.engine.execute(text(sql))
    # boolean to check if the username is unique
    new_user = True
    # attempts to see if the username already exists by searching the created usernames
    for result in results:
            if result['username']==request.form['N_username']:
                new_user = False
    # assuming no identical usernames were found, add_user will now add them to the database
    if new_user:
        # inserts the new username info into both tables
        sql = """
        INSERT INTO Login
        VALUES ( """+"\""+str(request.form['N_username'])+"\""+", "+ "\""+ str(request.form['N_password']) +"\"" +", "+"\""+str(request.form['Occupation'])+"\"" + ");"
        db.engine.execute(text(sql))
        # me being thankful pep8 isn't required
        if str(request.form['Occupation']) == "instructor":
            sql = """
            INSERT INTO Instructor_info(username, type, feedback1, feedback2, feedback3, feedback4)
            VALUES ( """+"\""+str(request.form['N_username'])+"\""+", "+"\""+str(request.form['Occupation'])+"\"" +", Null" +", Null" +", Null" +", Null );"
            db.engine.execute(text(sql))
        else:
            sql = """
            INSERT INTO Student_info(username, type, midterm, midtermRemark, exam, examRemark, q1, q1Remark, q2, q2Remark, q3, q3Remark, q4, q4Remark, a1, a1Remark , a2, a2Remark, a3, a3Remark)
            VALUES ( """+"\""+str(request.form['N_username'])+"\""+", "+"\""+str(request.form['Occupation'])+"\"" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +", Null" +");"
            db.engine.execute(text(sql))
        # with the username being added it will launch the user to the home page
        session['username']=request.form['N_username']
        return render_template("index.html", user_name = str(session['username']))
    else:
        # username already exists so it sends them to a temp page to ask them to try again
        return '''<h1>Username already exists</h1>
                  <a href= "login.html">Please try again</a>'''

# all these check if there's a logged in user, if they're not loggin in they'll be redirected to the login page
@app.route("/index.html")
def home():
    if 'username' in session:
        return render_template("index.html", user_name = str(session['username']))
    else:
        return redirect("/login.html")

@app.route("/calendar.html")
def calendar():
    if 'username' not in session:
        return render_template("login.html")
    else:
        return render_template('calendar.html', user_name = str(session['username']))

@app.route("/login.html")
def login_html():
    if 'username' not in session:
        return render_template('login.html')
    else:
        return render_template("index.html", user_name = str(session['username']))

@app.route("/resources.html")
def resources():
    if 'username' not in session:
        return render_template("login.html")
    else:
        return render_template('resources.html', user_name = str(session['username']))
    

@app.route("/news.html")
def news():
    if 'username' not in session:
        return render_template("login.html")
    else:
         return render_template('news.html', user_name = str(session['username']))

@app.route("/assignments.html")
def assignments():
    if 'username' not in session:
        return render_template("login.html", user_name = str(session['username']))
    else:
         return render_template('assignments.html', user_name = str(session['username']))

@app.route("/lectures.html")
def lectures():
    if 'username' not in session:
        return render_template("login.html")
    else:
         return render_template('lectures.html', user_name = str(session['username']))
   

@app.route("/labs.html")
def labs():
    if 'username' not in session:
        return render_template("login.html")
    else:
         return render_template('labs.html', user_name = str(session['username']))

@app.route("/tests.html")
def tests():
    if 'username' not in session:
        return render_template("login.html")
    else:
         return render_template('tests.html', user_name = str(session['username']))
    


@app.route('/contact_instructor', methods=['POST', 'GET'])
def contact_instructor():
    if request.method == 'POST': 
        # for question 1 
        sql = """
        UPDATE instructor_info
        SET feedback1 = """+"\""+str(request.form['feedback1'])+"\""+"""
        WHERE username = """+"\""+str(request.form['who'])+"\""+"""
        """
        db.engine.execute(text(sql))
        # for question 2
        sql = """
        UPDATE instructor_info
        SET feedback2 = """+"\""+str(request.form['feedback2'])+"\""+"""
        WHERE username = """+"\""+str(request.form['who'])+"\""+"""
        """
        db.engine.execute(text(sql))
        # for question 3 
        sql = """
        UPDATE instructor_info
        SET feedback3 = """+"\""+str(request.form['feedback3'])+"\""+"""
        WHERE username = """+"\""+str(request.form['who'])+"\""+"""
        """
        db.engine.execute(text(sql))
        # for question 4
        sql = """
        UPDATE instructor_info
        SET feedback4 = """+"\""+str(request.form['feedback4'])+"\""+"""
        WHERE username = """+"\""+str(request.form['who'])+"\""+"""
        """
        db.engine.execute(text(sql))
        return redirect("/contact.html")


@app.route("/contact.html")
def contact():
    # gets the user's type from the database as a resultproxy object
    user_type = db.engine.execute("SELECT type FROM Login WHERE username = " +"\""+ session['username']+"\"")
    # dummmy variable to turn it into a string
    userType = ""
    # usernames are unique so this only runs once
    for u_t in user_type:
        userType = u_t
    # 3 if statements, two for a logged in student or instructor with the last being there for a logged out user attempting to access the page
    if 'username' in session and str(userType) == "('student',)":
        # sql command to get all usernames of instructors
        sql = """
        SELECT username
        FROM Login
        WHERE type = "instructor"
        """
        #get all of the usernames of instructors
        instructor_info = db.engine.execute(text(sql))
        # gets rid of the (##,) leftover from resultproxy to just ##
        instructor_info_str = list()
        for temp in instructor_info:
            instructor_info_str.append((str(temp.username)))
        return render_template('contact.html', instructor_info_str=instructor_info_str, user_name= str(session['username']))
    elif 'username' in session and str(userType) == "('instructor',)":
        # a instructor user is attempting to access a contact page. Refuses to load and tells the instructor user it doesn't have permission and should leave
        return """
        <header>
        <h2 class = "pagetitle">Contact Page</h2>  
        </header>
        <div class = "Core">
        <h1> You don't have permission to access this, please go back or click this link </h1>
        <a href = "index.html"> Click this </a></div>
        """
    else:
        # prompts a login since this request is from someone not loggin in
        return render_template("login.html")

@app.route("/videos.html")
def videos():
    if 'username' not in session:
        return render_template("login.html")
    else:
         return render_template('videos.html', user_name = str(session['username']))

@app.route('/remark_request', methods=['POST'])
def remark_request():
    # sets the remark columns to the students requested grade where an instructor can then see it and choose to change it
    if str(request.form['grade_type']) == "q1":
        sql = """
        UPDATE Student_info
        SET q1Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "q2":
        sql = """
        UPDATE Student_info
        SET q2Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "q2":
        sql = """
        UPDATE Student_info
        SET q2Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "q3":
        sql = """
        UPDATE Student_info
        SET q3Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "q4":
        sql = """
        UPDATE Student_info
        SET q4Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "a1":
        sql = """
        UPDATE Student_info
        SET a1Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "a2":
        sql = """
        UPDATE Student_info
        SET a2Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "a3":
        sql = """
        UPDATE Student_info
        SET a3Remark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "midterm":
        sql = """
        UPDATE Student_info
        SET midtermRemark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    elif str(request.form['grade_type']) == "exam":
        sql = """
        UPDATE Student_info
        SET examRemark = """+"\""+str(request.form['remark_request'])+"\""+"""
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        db.engine.execute(text(sql))
    return redirect("/student.html")

@app.route("/student.html")
def student():
    # gets the user's type from the database as a resultproxy object
    user_type = db.engine.execute("SELECT type FROM Login WHERE username = " +"\""+ session['username']+"\"")
    # dummmy variable to turn it into a string
    userType = ""
    # usernames are unique so this only runs once
    for u_t in user_type:
        userType = u_t
    if 'username' in session and str(userType) == "('student',)":
        # user is a valid student so it shows them their grades from the DB
        sql = """
        SELECT midterm
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        midterm = db.engine.execute(text(sql))
        sql = """
        SELECT exam
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        exam = db.engine.execute(text(sql))
        sql = """
        SELECT q1
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        q1 = db.engine.execute(text(sql))
        sql = """
        SELECT q2
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        q2 = db.engine.execute(text(sql))
        sql = """
        SELECT q3
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        q3 = db.engine.execute(text(sql))
        sql = """
        SELECT q4
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        q4 = db.engine.execute(text(sql))
        sql = """
        SELECT a1
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        a1 = db.engine.execute(text(sql))
        sql = """
        SELECT a2
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        a2 = db.engine.execute(text(sql))
        sql = """
        SELECT a3
        FROM Student_info
        WHERE username = """+"\""+str(session['username'])+"\""+"""
        """
        a3 = db.engine.execute(text(sql))
        # sql command to get all usernames of instructors
        sql = """
        SELECT username
        FROM Login
        WHERE type = "student"
        """
        # gets rid of the (##,) leftover from resultproxy to just ##
        for temp in a1:
            a1 = str(temp.a1)

        for temp in a2:
            a2 = str(temp.a2)

        for temp in a3:
            a3 = str(temp.a3)

        for temp in q1:
            q1 = str(temp.q1)

        for temp in q2:
            q2 = str(temp.q2)

        for temp in q3:
            q3 = str(temp.q3)

        for temp in q4:
            q4 = str(temp.q4)

        for temp in midterm:
            midterm = str(temp.midterm)

        for temp in exam:
            exam = str(temp.exam)
        user_name = str(session['username'])
        return render_template('student.html', midterm = midterm, exam = exam, q1 = q1, q2 = q2, q3 = q3, q4 = q4, a1 = a1, a2 = a2, a3 = a3, user_name = user_name)
    elif 'username' in session and str(userType) == "('instructor',)":
        # a instructor user is attempting to access a student page. Refuses to load and tells the instructor user it doesn't have a reason to be here and let's them leave
        return """
        <header>
        <h2 class = "pagetitle">My grades</h2>  
        </header>
        <div class = "Core">
        <h1> You're an instructor you don't have grades... please go back or click this link </h1>
        <a href = "index.html"> Click this to leave </a></div>
        """
    else:
        # prompts a login since this request is from someone not loggin in
        return render_template("login.html")
        
@app.route('/change_mark', methods=['POST'])
def change_mark():
    column = str(request.form['which_mark'])
    new_mark = str(request.form['new_mark'])
    stud_name = str(request.form['which_student'])
    if request.method == 'POST': 
        sql = "UPDATE student_info SET  " + column + " = " + new_mark +  " WHERE username = " + '\'' + stud_name +'\''
        db.engine.execute(text(sql))
    return render_template("instructor.html")

@app.route("/instructor.html")
def instructor():
    # gets the user's type from the database as a resultproxy object
    user_type = db.engine.execute("SELECT type FROM Login WHERE username = " +"\""+ session['username']+"\"")
    # dummmy variable to turn it into a string
    userType = ""
    # usernames are unique so this only runs once
    for u_t in user_type:
        userType = u_t
    # 3 if statements, two for a logged in instructor or student with the last being there for a logged out user attempting to access the page
    if 'username' in session and str(userType) == "('instructor',)":
        # sql command to get all of the students grades
        sql = """
        SELECT username, midterm, exam, q1, q2, q3, q4, a1, a2, a3
        FROM Student_info
        """
        # render the html template while sending all the student grades along with it
        student_info = db.engine.execute(text(sql))
        # sql command to get all of the student usernames
        sql = """
        SELECT username
        FROM Student_info
        """
        # render the html template while sending all the student usernames along with it
        student_name = db.engine.execute(text(sql))
        # gets rid of the (##,) leftover from resultproxy to just ##
        student_name_str = list()
        for temp in student_name:
            student_name_str.append((str(temp.username)))
        return render_template('instructor.html', student_info = student_info, user_name = str(session['username']), student_name_str = student_name_str)
    elif 'username' in session and str(userType) == "('student',)":
        # a student user is attempting to access a instructor page. Refuses to load and tells the student user it doesn't have permission and should leave
        return """
        <header>
        <h2 class = "pagetitle">Student grades, viewing only</h2>  
        </header>
        <div class = "Core">
        <h1> You don't have permission to access this, please go back or click this link </h1>
        <a href = "index.html"> Click this </a></div>
        """
    else:
        # prompts a login since this request is from someone not loggin in
        return render_template("login.html")

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)
