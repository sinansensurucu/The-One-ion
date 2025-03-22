from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Backend.DatabaseLogic import ExecutionAbort, signInUser, createUser, deleteUser, getArticleToSolve, getUserEmail, getUserTotalScore, getUserBestScore, getUserStreak, getLeaderboard, getStatisticToSolve

app = Flask(
    __name__,
    template_folder="Frontend/templates",
    static_folder="Frontend/static"
    )
app.secret_key = 'some-key-change-later'

Article = None
Statistic = None
user = None
button_pressed = False
id_of_button_pressed = None

@app.route('/', methods=['GET', 'POST'])
def index():
    global logged_in, Article, Statistic, user
    if not session.get("user_id"):
        logged_in = False
    else:
        logged_in = True
        #updateInfo()
        #Article = ("title", "bla bla bla", "www.youtube.com", "Fake")   ##temp values
        #user = getUserEmail(session["user_id"])
        #user = ("bloop", 1200, 13200, 7, [(1,"b@gmail.com", 23000), (2, "c@gmail.com", 4500), (3, "a@gmail.com", 4500)])

    
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
    
    return render_template("index.html", article=Article, User=user, logged_in=logged_in)
    #return render_template("index.html", article=Article, statistic=Statistic,User=user, logged_in=logged_in)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global Article, Statistic, user, logged_in
    if session.get("user_id"):
        Article = getArticleToSolve(session["user_id"]) 
        #Statistic = getStatisticToSolve(session["user_id"])
        user = (getUserEmail(session["user_id"]), getUserTotalScore(session["user_id"]), getUserBestScore(session["user_id"]), getUserStreak(session["user_id"]), getLeaderboard())

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
    
    return render_template("signin.html", article=Article, User=user, logged_in=logged_in)
    #return render_template("signin.html", article=Article, statistic=Statistic, User=user, logged_in = True)


@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    
    button_pressed = True 

    id_of_button_pressed = request.form['button_id']
    if Article[2] == id_of_button_pressed:
        return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "True"})
        
        ##game win
    else:
        return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "False"})
        ##game lose


if __name__ == '__main__':
    app.run(debug=True)
    session["user_id"] = None
    