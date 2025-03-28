from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Backend.DatabaseLogic import ExecutionAbort, signInUser, createUser, deleteUser, getArticleToSolve, getUserEmail, getUserTotalScore, getUserBestScore, getUserStreak, getLeaderboard, getStatisticToSolve
from Backend.GameLogic import GameLogic

app = Flask(
    __name__,
    template_folder="Frontend/templates",
    static_folder="Frontend/static"
    )

first_request = True

@app.before_request
def clear_session_on_startup():
    global first_request
    if first_request:
        session.clear()
        first_request = False
        session["user_id"] = None

app.secret_key = 'some-key-change-later'
#attributes to send to frontend
Article = None
ArticleD = None
Statistic = None
user = None
button_pressed = False
attempted_log_in = False
id_of_button_pressed = None
attempted_log_in = False
logged_in = None

#maintains game screen
@app.route('/', methods=['GET', 'POST'])
def index():
    global logged_in, Article, ArticleD, Statistic, user, attempted_log_in

    if not session.get("user_id"):
        logged_in = False
        return redirect(url_for('signin'))
    else:
        logged_in = True

    user = (getUserEmail(session["user_id"]), getUserTotalScore(session["user_id"]), getUserBestScore(session["user_id"]), getUserStreak(session["user_id"]), getLeaderboard())
    
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
            attempted_log_in = False
            
        except ExecutionAbort as e:
            flash(str(e), "error")
        return redirect(url_for('signin'))
    
    return render_template("index.html", article=Article, articleD=ArticleD, statistic=Statistic,User=user, logged_in=logged_in, attempted=attempted_log_in)

#maintains signin screen
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    global logged_in, Article, ArticleD, Statistic, user, attempted_log_in
    if session.get("user_id"):
        Article = getArticleToSolve(session["user_id"]) 
        ArticleD = getArticleToSolve(session["user_id"])
        Statistic = getStatisticToSolve(session["user_id"])
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
            attempted_log_in = False
            user = getUserEmail(session["user_id"])
            Article = getArticleToSolve(user) 
            
        except ExecutionAbort as e:
            attempted_log_in = True
            flash(str(e), "error")
            return redirect(url_for('signin'))
        return redirect(url_for('index'))
    
    return render_template("signin.html", article=Article, articleD=ArticleD, statistic=Statistic, User=user, logged_in = logged_in, attempted=attempted_log_in)

#listen to button calls to handel complex buttons
@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    # timeResetButtonIDs = ["standard-mode-btn", "daily-mode-btn", "statistic-mode-btn",]
    # time_taken = -1  ## null value of -1
    if not session.get("user_id"):
        return jsonify({"status": "error", "message": "Not logged in"}), 401
    
    # button_pressed = True 

    id_of_button_pressed = request.form['button_id']
    time_left = int(request.form['time_left'])
    user_id = session["user_id"]
    ### time taken -> access here :>  also set the score there

    time_taken = 100 - time_left
    score = time_taken * 10 #just to make the numbers a bit bigger and nicer

    game = GameLogic(user_id)

    is_correct = False
    if Article[3] == id_of_button_pressed:
        is_correct = True
    elif Statistic and Statistic[1] == id_of_button_pressed:
        is_correct = True
    
    # Update user profile
    try:
        game.update_user_profile(is_correct, score if is_correct else 0)
        
        return jsonify({
            "status": "success",
            "id": id_of_button_pressed,
            "win": "True" if is_correct else "False",
            "score": score if is_correct else 0
        })
        
    except ExecutionAbort as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    
#helper function for game logic
@app.route('/next_article', methods=['POST'])
def next_article():
    
    return jsonify({"status": "success", "url": url_for('signin')})

    
@app.route('/time_over', methods=['POST'])
def time_over():
    if not session.get("user_id"):
        return jsonify({"message": "Please log in first."})
    
    # Handle time-out logic (e.g., end game, reset question, etc.)
    return jsonify({"message": "Time is up! Try again."})


if __name__ == '__main__':
    app.run(debug=True)
    