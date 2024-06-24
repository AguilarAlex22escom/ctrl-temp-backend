from config import *

# from circuit import get_temperature, set_temperature

"""
logged_user = (
    session["names"],
    session["email"],
)
"""


@app.route("/", methods=["GET", "POST"])
def get_index():
    if "names" in session:
        return render_template(
            "index.html",
            names=session["names"],
            email_address=session["email"],
            # sensor_data=get_temperature(),
            sensor_data=session["temperature"],
        )
    else:
        return render_template("index.html")


@app.route("/temperature_modes", methods=["GET", "POST"])
def get_temperature_modes():
    if request.method == "POST":
        state_user = session["id"]
        temperature_previous = session["temperature_previous"]
        temperature_data = request.form.get("temperature")
        params = (
            state_user,
            temperature_previous,
            temperature_data,
        )
        query = """INSERT INTO states (state_user, state_date, state_previous, state_modified) VALUES (%s, NOW(), %s, %s);"""
        cursor = mysql.connection.cursor()
        cursor.execute(query, params)
        mysql.connection.commit()
        cursor.close()
        session["temperature_modified"] = temperature_data
        session["temperature_previous"] = session["temperature_modified"]
        # set_temperature(session["temperature"])
        return render_template(
            "temperature_modes.html",
            names=session["names"],
            email_address=session["email"],
            actived_mode=session["temperature_modified"],
        )

    return render_template(
        "temperature_modes.html",
        names=session["names"],
        email_address=session["email"],
    )


@app.route("/modes_info")
def get_modes_info():
    print(session["temperature"])
    return render_template(
        "modes_info.html",
        names=session["names"],
        email_address=session["email"],
    )


@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        user_email = request.form.get("user_email")
        query = """SELECT (user_email) FROM users WHERE user_email=%s;"""
        params = (user_email,)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        temporary_user = cursor.fetchone()
        cursor.close()
        if temporary_user:
            session["email"] = temporary_user["user_email"]
            message = Message(
                f"Se ha enviado un correo electrónico a la cuenta {temporary_user['user_email']}",
                sender=app.config["MAIL_USERNAME"],
                recipients=[user_email],
            )
            message.html = render_template("email.html")
            email.send(message)
            return render_template(
                "auth/reset_password.html",
                sent_email=f"Se ha enviado un correo electrónico a la cuenta {temporary_user['user_email']}",
            )
        else:
            invalid_email = "No se encuentra el correo registrado. Ingresa un correo valido o registra el correo que ingresaste."
            return render_template(
                "auth/reset_password.html", invalid_email=invalid_email
            )
    else:
        return render_template("auth/reset_password.html")


@app.route("/save_new_password", methods=["GET", "POST"])
def put_new_saved_password():
    if request.method == "POST":
        user_temporaly_email = session["email"]
        user_new_password = request.form.get("new-password")
        user_confirm_new_password = request.form.get("confirm-new-password")
        user_hashed_new_password = generate_password_hash(user_new_password)
        params = (user_hashed_new_password, user_temporaly_email)
        query = """UPDATE users SET user_password = %s WHERE user_email = %s;"""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, params)
        cursor.close()
        if user_new_password == user_confirm_new_password:
            return redirect(url_for("get_user"))
        else:
            return render_template(
                "save_new_password.html",
                email_address=session["email"],
                error="Las contraseñas no son idénticas.",
            )

    return render_template("save_new_password.html", email_address=session["email"])


@app.route("/settings", methods=["GET", "POST"])
def get_settings():
    if "names" in session:
        return render_template(
            "settings.html", names=session["names"], email_address=session["email"]
        )


@app.route("/settings/account", methods=["GET", "POST"])
def get_account_settings():
    if "names" in session:
        return render_template(
            "account_settings.html",
            names=session["names"],
            email_address=session["email"],
            password=session["temporaly_psw"],
        )
    else:
        return render_template(
            "account_settings.html",
            email_address="No tienes acceso a esta ruta. Inicia sesión antes.",
            password="*************************",
        )


@app.route("/help")
def get_help():
    if "names" in session:
        return render_template(
            "help.html", names=session["names"], email_address=session["email"]
        )
    else:
        return render_template("help.html")


@app.route("/statistics")
def get_statistics():
    if "names" in session:
        query = """SELECT state_date, state_previous FROM states;"""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query)
        states = cursor.fetchall()
        cursor.close()
        if states:
            temperatures = pd.DataFrame(states)
            temperatures["state_date"] = pd.to_datetime(temperatures["state_date"])
            temperatures["date"] = temperatures["state_date"].dt.date
            daily_average = (
                temperatures.groupby("date")["state_previous"].mean().reset_index()
            )
            daily_average.columns = ["date", "daily_average"]
            daily_average["date"] = pd.to_datetime(daily_average["date"])
            daily_average["date"] = daily_average["date"].dt.strftime(
                "%Y-%m-%dT%H:%M:%S-06:00"
            )
            print(daily_average)
            return render_template(
                "statistics.html",
                names=session["names"],
                email_address=session["email"],
                temperatures=daily_average.to_dict("records"),
                # temperatures=temperatures["state_previous"].tolist(),
                # dates=temperatures["state_date"].tolist(),
            )
