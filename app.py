from flask import Flask, render_template, request, redirect, url_for, flash, session
from Backend.DatabaseLogic import ExecutionAbort, signInUser, createUser, deleteUser

app = Flask(
    __name__,
    template_folder="Frontend/templates",
    static_folder="Frontend/static"
    )
app.secret_key = 'some-key-change-later'

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if session.get("user_id"):
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        action = request.form.get("action")
        email = request.form.get("username")
        password = request.form.get("password")
        
        try:
            if action == "login":
                user_id = signInUser(email, password)
                session['user_id'] = user_id
                flash("Login successful!", "success")
            elif action == "create account":
                user_id = createUser(email, password)
                session['user_id'] = user_id
                flash("Registration and login successful!", "success")
        except ExecutionAbort as e:
            flash(str(e), "error")
            return redirect(url_for('signin'))
        
        return redirect(url_for('index'))
    
    return render_template("signin.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    if not session.get("user_id"):
        flash("Please sign in first.", "error")
        return redirect(url_for('signin'))
    
    if request.method == 'POST':
        action = request.form.get("action")
        
        try:
            if action == "logout":
                session["user_id"] = None
                flash("User logged out.", "success")
            elif action == "delete account":
                deleteUser(session["user_id"])
                session["user_id"] = None
                flash("User account deleted.", "success")
        except ExecutionAbort as e:
            flash(str(e), "error")

        return redirect(url_for('index'))

    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)