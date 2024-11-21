from flask import Flask, render_template, request, session, redirect, flash
from base import app
from base.com.dao.login_dao import LoginDAO

@app.route('/')
def login():
    return render_template("admin/login.html")

@app.route('/load_login')
def home():
    return render_template("admin/login.html")

@app.route('/admin/load_dashboard', methods=['GET', 'POST'])
def load_dashboard():
    print("in")
    username = request.form.get('login_username')
    password = request.form.get('login_password')
    login_dao=LoginDAO()
    print("username>>>>",username)
    print("username>>>>",password)
    login_vo_list=login_dao.view_login()
    login_list=[i.as_dict() for i in login_vo_list]
    print("login_list>>>",login_list[0]['login_username'])
    print("login_list>>>",login_list[0]['login_password'])
    if request.method=='POST':
        print("in if")
        if(login_list[0]['login_username']==username and login_list[0]['login_password']==password):
            print("hello>>>>>>>>>>>>>>>>>>")
            return render_template('admin/index.html')

        else:
            print("if out")
            error_message = "Invalid username or password"
            flash(error_message)
            return redirect("/load_login")
            # return render_template("admin/login.html")


    else:
         return redirect("/load_login")



