from hashlib import sha256
from flask import Flask, render_template, request, flash, session, url_for, redirect
from flaskr.models.user import User
from flaskr.db.db_user import DBUser

def create_app():
    app = Flask(__name__)
    app.secret_key = "1234"

    @app.route("/")
    def home():
        if 'user' in session:
            return render_template('home.html', user = session['user'])
        
        return redirect(url_for('login'))
    

    @app.route("/login", methods=('GET', 'POST'))
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            error = None
            if not username:
                error = "Username is empty!"
            elif not password:
                error = "Password is empty!"

            if error is not None:
                flash(error, 'error')
            else:
                user = DBUser.get_for_username(username)
                if user is not None:
                    hash_pass = sha256(password.encode('utf-8')).hexdigest()
                    if user.password != hash_pass:
                        flash("Username/Password not valid!", 'error')
                    else:
                        session['user'] = user.__dict__
                        return redirect(url_for('home'))

        return render_template('login.html')
    
    @app.route("/logout")
    def logout():
        if 'user' in session:
            session.pop('user', None)
            return redirect(url_for('login'))
        else:
            flash("User alredy logged out", 'error')
            return redirect(url_for('home'))

    @app.route("/register", methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_pass = request.form.get('conf_pass')
            error = None
            if not username:
                error = "Empty username!"
            elif not password:
                error = "Empty password!"
            elif password != confirm_pass:
                error = "Password didn't match!"

            if error is not None:
                flash(error, 'error')
            else:
                user = User(username, password)
                if DBUser.get_for_username(user.username) is None:
                    try:
                        DBUser.save(user)
                        flash("Registrstion was successful!", 'success')
                    except Exception as ex:
                        print(ex)
                        flash("Error!", 'error')
                else:
                    flash("User alredy exists!", 'error')
        return render_template('register.html')

    return app
