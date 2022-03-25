import os
from flask import Flask, flash, render_template, request, session, redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient

app = Flask(__name__)
# session and uploaded folder
app.secret_key = 'W8wfyR2ERM'
app.config['SESSION_TYPE'] = 'filesystem'

# for db and connection
client  = MongoClient('localhost',27017)
db = client.db1


# just for testing purpose
@app.route('/hello')
def hello_world():
    return "Hello world!"


@app.route('/')
def home():
    return redirect(url_for(".login"))



@app.route('/profile')
def profile():
    if session['username']:
        username = session['username']
        return render_template("profile.html",username=username)
    else:
        return redirect(url_for('.login'))  


# render login form
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = db.users.find_one({"username":username})
        if user and check_password_hash(user.get('password'),password):
            session['username'] = user.get('username')
            return redirect(url_for('.profile')) 
        else:   
            flash('Username or password incorrect!')
            return redirect(request.url)
    else:
        if session.get('username'):
            return redirect(url_for('.profile'))
        else:
            return render_template("login.html")


# render signup form
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name", "")
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = db.users.find_one({"username":username})
        if user:
            flash('Username already exist!')
            return redirect(request.url)
        else:
            db.users.insert_one({
                "name":name,
                "username":username,
                "password":generate_password_hash(password)
            })
            flash('Account created! Please login')
            return redirect(url_for(".login"))   
    else:
        if session.get('username'):
            return redirect(url_for('.profile'))
        else:
            return render_template("signup.html")



# handle logout
@app.route("/logout", methods=["POST"])
def logout():
    session['username'] = None
    return redirect('/');  


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)