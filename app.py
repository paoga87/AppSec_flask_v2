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
    return render_template("login.html")

@app.route('/spell_check')
def spell():
    return "Spell checker page"


if __name__ == '__main__':
    app.run(debug=True)