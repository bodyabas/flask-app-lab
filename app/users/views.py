from . import user_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime

@user_bp.route("/profile") 
def get_profile(): 
    if "username" and "password" in session: 
        username_value = session["username"]
        password_value = session["password"]
        return render_template("profile.html", username=username_value, password=password_value ) 
    flash("Ви вийшли з сесії.", "danger") 
    return redirect(url_for("users.login"))

@user_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form["login"]
        password = request.form["password"]
        if username == "bodya" and password == "1234":
            session["username"] = username
            session["password"] = password
            flash("Ви успішно авторизувалися.", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Неправильний логін або пароль", "danger")
    return render_template("login.html")

@user_bp.route('/logout')
def logout():
    # Видалення користувача із сесії
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('users.get_profile'))

@user_bp.route("/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", 0, int)

    return render_template("hi.html", name = name, age = age)

@user_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)

@user_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    # response.set_cookie('username', 'student', expires=datetime.now()+timedelta(seconds=10))
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response