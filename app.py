import os
import subprocess
import json
from subprocess import Popen, PIPE, check_output
from flask import Flask, render_template, redirect, url_for, session, request


app = Flask(__name__)
app.config['SECRET_KEY'] = 'WxND4o83j4K4iO3762'

#Users file
Users = {}
#user_file = open("./static/users.txt","r")
#Users = eval(user_file.read())
#user_file.close()


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['uname'].lower()
        if (username in Users.keys()):
            success = "failure"
        else:
            password = request.form['pword']
            twofa = request.form['2fa']
            Users[username] = {'password': password, '2fa': twofa}
            success = "success"
            user_file = open("./static/users.txt", "w")
            user_file.write(json.dumps(Users))
            user_file.close()

        return render_template ("register.html", success = success)
    
    if request.method == 'GET':
        success = "Please register to access the site"
        return render_template("register.html", success = success)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['uname'].lower()
        if (username in Users.keys()):
            password = request.form['pword']
            twofa = request.form['2fa']
            if (Users[username]['password'] == password):
                if (Users[username]['2fa'] == twofa):
                    session['logged_in'] = True
                    result = "success"
                else:
                    result = "Two-factor failure"
            else:
                result = "Incorrect password"
        else:
            result = "Incorrect username"
        
        return render_template('login.html', result = result)

    if request.method == 'GET':
        result = "Please login to use the site"
        return render_template("login.html", result = result)

@app.route('/spell_check')
def spell():
    if(session.get('logged_in') == True): 
        #cpath = os.getcwd()
        #if request.method == 'POST':
            #outputtext = request.form ['inputtext']
            #textfile = open("./static.text.tx", "w")
            #textfile.writelines(outputtext)
            #textfile.close()

            #tmp = subprocess.check_output([cpath + '/static/a.out',cpath + '/static/text.text', cpath + '/static/wordlist.txt']).decode('utf-8')
            #mispelled = tmp.replace("\n",", ")[:-2]
            #return render_template("spell_check.html", mispelled = mispelled, outputtext = outputtext)

        return render_template("spell_check.html")
    else:
        return redirect(url_for('login'))
    


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
