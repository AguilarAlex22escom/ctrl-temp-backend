from settings import *

# Register new users in the app.
@app.route("/signin", methods=["GET", "POST"])
def post_user():
    if request.method == "POST":
        user_names = request.form["user_names"]
        user_email = request.form["user_email"]
        user_type = "patient"
        user_password = request.form["user_password"]
        user_hashed_password = generate_password_hash(user_password)
        # params = (user_names, user_email, user_type, user_hashed_password)
        # params = (user_names, user_email, user_type, user_password)
        existing_user = mongo.db.users.find_one({'user_email': user_email})
        if not existing_user:
            mongo.db.users.insert_one({
                'user_names': user_names,
                'user_email': user_email,
                'user_type': user_type,
                'user_password': user_hashed_password
            })
            return redirect("/login", code=302)
        else:
            flash('User already exists.')
            return redirect(url_for('post_user'))
    return render_template("auth/signin.html")


# Login users already created in the app.
@app.route("/login", methods=["GET", "POST"])
def get_user():
    message = ""
    if request.method == "POST":
        user_email = request.form.get("user_email", "johndoe@gmail.com")
        user_password = request.form.get("user_password", "-----")
        user = mongo.db.users.find_one({'user_email': user_email})
        if user and check_password_hash(user["user_password"], user_password):
            # if user and user["user_password"] == user_password:
            session["loggedin"] = True
            session["id"] = user["user_id"]
            session["names"] = user["user_names"]
            session["email"] = user["user_email"]
            session["type"] = user["user_type"]
            session["password"] = user["user_password"]
            session["temporaly_psw"] = user_password
            session["pressure"] = 27
            message = "Logged in successfully!"
            return redirect(url_for("get_index"))
        else:
            return render_template(
                "auth/login.html",
                error="Error de inicio de sesión. El correo o la contraseña son incorrectos.",
            )
    return render_template("auth/login.html", message=message)


@app.route("/logout")
def logout_user():
    session.pop("names", None)
    return redirect(url_for("get_index"))


@app.route("/settings/change_user_password", methods=["GET", "POST"])
def put_user_password():
    if "names" in session:
        wrong_password = ""
        if request.method == "POST":
            user_email = session["email"]
            user_old_password = request.form.get("old-password")
            user_new_password = request.form.get("new-password")
            user_confirm_password = request.form.get("confirm-password")
            user_hashed_new_password = generate_password_hash(user_new_password)
            if user_new_password == user_confirm_password and check_password_hash(
                session["password"], user_old_password
            ):
                mongo.db.users.update_one(
                    {'user_email': user_email},
                    {"$set": {'user_password': user_hashed_new_password}}
                )
                session["temporaly_psw"] = user_new_password
                session["password"] = user_hashed_new_password
                return redirect(url_for("get_account_settings"))
            else:
                return render_template(
                    "change_user_password.html",
                    wrong_password="Ingresaste una contraseña que no es de la cuenta. Ingresa la correcta.",
                    names=session["names"],
                    email_address=session["email"],
                )

        return render_template(
            "change_user_password.html",
            names=session["names"],
            email_address=session["email"],
        )


"""
Resources:
GET & POST HTTP methods: https://www.geeksforgeeks.org/flask-http-method/
MySQL DB connection: https://hevodata.com/learn/flask-mysql/#Flask_MySQL_Step_1_Connecting_a_Flask_Application_to_a_MySQL_Database
Encrypt passwords: https://www.solingest.com/almacenar-contrasenas-en-mysql
User's variables: https://forums.mysql.com/read.php?71,353592,353616
Previous register in database: https://parzibyte.me/blog/2018/08/17/obtener-siguiente-y-anterior-registro-o-fila-en-mysql/
"""
