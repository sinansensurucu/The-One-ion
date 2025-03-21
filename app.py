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
def index():
    global logged_in, Article, user
    if not session.get("user_id"):
        logged_in = False
    else:
        logged_in = True
        #updateInfo()
        # Article = getArticleToSolve(session["user_id"]) 
        Article = ("title", "bla bla bla", "www.youtube.com", "Fake")   ##temp values
        # user = getUserEmail(session["user_id"])
        user = "bloop"

    
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
            logged_in = False
            
        except ExecutionAbort as e:
            flash(str(e), "error")
        return redirect(url_for('signin'))

    return render_template("index.html", article=Article, Username=user, logged_in=logged_in)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global Article, user, logged_in
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
            logged_in = True
            user = getUserEmail(session["user_id"])
            Article = getArticleToSolve(user) 
            
        except ExecutionAbort as e:
            flash(str(e), "error")
            return redirect(url_for('signin'))
        return redirect(url_for('index'))

    return render_template("signin.html", article=Article, Username=user, logged_in = True)


@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    
    button_pressed = True 
    print(request.form['button_id'])
    print("buttppn pressed")
    id_of_button_pressed = request.form['button_id']
    if Article[3] == id_of_button_pressed:
        return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "True"})
        
        ##game win
    else:
        return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "False"})
        ##game lose


if __name__ == '__main__':
    app.run(debug=True)
    session["user_id"] = None
    