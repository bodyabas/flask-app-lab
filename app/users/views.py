from . import user_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime

@user_bp.route("/profile") 
def get_profile(): 
    if "username" in session: 
        username_value = session["username"]
        cookies = request.cookies

        return render_template("profile.html", username=username_value, cookies = cookies) 
    
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

@user_bp.route('/set_cookie', methods=["POST"])
def set_cookie():

    key = request.form.get("key")
    value = request.form.get("value")
    duration = int(request.form.get("duration", 0))

    response = make_response(redirect(url_for("users.get_profile")))
    if key and value:
        response.set_cookie(key, value, max_age=timedelta(seconds=duration))
        flash(f"Кука '{key}' успішно додана!", "success")
    else:
        flash("Заповніть усі поля для додавання куки.", "danger")

    return response

@user_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@user_bp.route('/delete_cookie', methods=["POST"])
def delete_cookie():

    key = request.form.get("key")
    response = make_response(redirect(url_for("users.get_profile")))

    if key:
        response.set_cookie(key, '', expires=0)
        flash(f"Кука '{key}' успішно видалена!", "success")

    return response

@user_bp.route('/delete_all_cookies', methods=["POST"])
def delete_all_cookies():

    response = make_response(redirect(url_for("users.get_profile")))

    for cookie_key in request.cookies.keys():
        response.set_cookie(cookie_key, '', expires=0)
    flash("Усі кукі успішно видалені!", "success")

    return response
