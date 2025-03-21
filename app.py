from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Backend.DatabaseLogic import ExecutionAbort, signInUser, createUser, deleteUser, getArticleToSolve, getUserEmail

app = Flask(
    __name__,
    template_folder="Frontend/templates",
    static_folder="Frontend/static"
    )
app.secret_key = 'some-key-change-later'


global Article 
global user 
Article = None
user = None
button_pressed = False
id_of_button_pressed = None



@app.route('/', methods=['GET', 'POST'])
def signin():
    global Article, user
    if session.get("user_id"):
        return redirect(url_for('index'), article= getArticleToSolve(session["user_id"]) , Username=getUserEmail(session["user_id"]))
    
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
            user = getUserEmail(session["user_id"])
            Article = getArticleToSolve(user) 
            
        except ExecutionAbort as e:
            flash(str(e), "error")
            return redirect(url_for('signin'))
        
        return redirect(url_for('index'))
    
    return render_template("signin.html", article=Article, Username=user)


@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    
    button_pressed = True 
    id_of_button_pressed = request.form['button_id']
    if Article[3] == id_of_button_pressed:
        return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "True"})
        ##game win
    else:
        return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "False"})
        ##game lose





@app.route('/index', methods=['GET', 'POST'])
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

        return redirect(url_for('index'), article=Article, Username=user)

    return render_template("index.html", article=Article, Username=user)


if __name__ == '__main__':
    app.run(debug=True)
    session["user_id"] = None
    