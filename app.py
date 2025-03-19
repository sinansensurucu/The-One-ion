from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from Backend.DatabaseLogic import ExecutionAbort, signInUser, createUser, deleteUser

app = Flask(
    __name__,
    template_folder="Frontend/templates",
    static_folder="Frontend/static"
    )
app.secret_key = 'some-key-change-later'

        
Articles = [["A", """Apple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. Founded in 1976 as Apple Computer Company by Steve Jobs, Steve Wozniak and Ronald Wayne, the company was incorporated by Jobs and Wozniak as Apple Computer, Inc. the following year. It was renamed Apple Inc. in 2007 as the company had expanded its focus from computers to consumer electronics. Apple is the largest technology company by revenue, with US$391.04 billion in the 2024 fiscal year.

The company was founded to produce and market Wozniak's Apple I personal computer. Its second computer, the Apple II, became a best seller as one of the first mass-produced microcomputers. Apple introduced the Lisa in 1983 and the Macintosh in 1984, as some of the first computers to use a graphical user interface and a mouse. By 1985, internal company problems led to Jobs leaving to form NeXT, Inc., and Wozniak withdrawing to other ventures; John Sculley served as long-time CEO for over a decade. In the 1990s, Apple lost considerable market share in the personal computer industry to the lower-priced Wintel duopoly of the Microsoft Windows operating system on Intel-powered PC clones. In 1997, Apple was weeks away from bankruptcy. To resolve its failed operating system strategy, it bought NeXT, effectively bringing Jobs back to the company, who guided Apple back to profitability over the next decade with the introductions of the iMac, iPod, iPhone, and iPad devices to critical acclaim as well as the iTunes Store, launching the "Think different" advertising campaign, and opening the Apple Store retail chain. These moves elevated Apple to consistently be one of the world's most valuable brands since about 2010. Jobs resigned in 2011 for health reasons, and died two months later; he was succeeded as CEO by Tim Cook.

Apple's product lineup includes portable and home hardware sApple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. Founded in 1976 as Apple Computer Company by Steve Jobs, Steve Wozniak and Ronald Wayne, the company was incorporated by Jobs and Wozniak as Apple Computer, Inc. the following year. It was renamed Apple Inc. in 2007 as the company had expanded its focus from computers to consumer electronics. Apple is the largest technology company by revenue, with US$391.04 billion in the 2024 fiscal year.

The company was founded to produce and market Wozniak's Apple I personal computer. Its second computer, the Apple II, became a best seller as one of the first mass-produced microcomputers. Apple introduced the Lisa in 1983 and the Macintosh in 1984, as some of the first computers to use a graphical user interface and a mouse. By 1985, internal company problems led to Jobs leaving to form NeXT, Inc., and Wozniak withdrawing to other ventures; John Sculley served as long-time CEO for over a decade. In the 1990s, Apple lost considerable market share in the personal computer industry to the lower-priced Wintel duopoly of the Microsoft Windows operating system on Intel-powered PC clones. In 1997, Apple was weeks away from bankruptcy. To resolve its failed operating system strategy, it bought NeXT, effectively bringing Jobs back to the company, who guided Apple back to profitability over the next decade with the introductions of the iMac, iPod, iPhone, and iPad devices to critical acclaim as well as the iTunes Store, launching the "Think different" advertising campaign, and opening the Apple Store retail chain. These moves elevated Apple to consistently be one of the world's most valuable brands since about 2010. Jobs resigned in 2011 for health reasons, and died two months later; he was succeeded as CEO by Tim Cook.

Apple's product lineup includes portable and home hardwareApple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. Founded in 1976 as Apple Computer Company by Steve Jobs, Steve Wozniak and Ronald Wayne, the company was incorporated by Jobs and Wozniak as Apple Computer, Inc. the following year. It was renamed Apple Inc. in 2007 as the company had expanded its focus from computers to consumer electronics. Apple is the largest technology company by revenue, with US$391.04 billion in the 2024 fiscal year.

The company was founded to produce and market Wozniak's Apple I personal computer. Its second computer, the Apple II, became a best seller as one of the first mass-produced microcomputers. Apple introduced the Lisa in 1983 and the Macintosh in 1984, as some of the first computers to use a graphical user interface and a mouse. By 1985, internal company problems led to Jobs leaving to form NeXT, Inc., and Wozniak withdrawing to other ventures; John Sculley served as long-time CEO for over a decade. In the 1990s, Apple lost considerable market share in the personal computer industry to the lower-priced Wintel duopoly of the Microsoft Windows operating system on Intel-powered PC clones. In 1997, Apple was weeks away from bankruptcy. To resolve its failed operating system strategy, it bought NeXT, effectively bringing Jobs back to the company, who guided Apple back to profitability over the next decade with the introductions of the iMac, iPod, iPhone, and iPad devices to critical acclaim as well as the iTunes Store, launching the "Think different" advertising campaign, and opening the Apple Store retail chain. These moves elevated Apple to consistently be one of the world's most valuable brands since about 2010. Jobs resigned in 2011 for health reasons, and died two months later; he was succeeded as CEO by Tim Cook.

Apple's product lineup includes portable and home hardwarApple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. Founded in 1976 as Apple Computer Company by Steve Jobs, Steve Wozniak and Ronald Wayne, the company was incorporated by Jobs and Wozniak as Apple Computer, Inc. the following year. It was renamed Apple Inc. in 2007 as the company had expanded its focus from computers to consumer electronics. Apple is the largest technology company by revenue, with US$391.04 billion in the 2024 fiscal year.

The company was founded to produce and market Wozniak's Apple I personal computer. Its second computer, the Apple II, became a best seller as one of the first mass-produced microcomputers. Apple introduced the Lisa in 1983 and the Macintosh in 1984, as some of the first computers to use a graphical user interface and a mouse. By 1985, internal company problems led to Jobs leaving to form NeXT, Inc., and Wozniak withdrawing to other ventures; John Sculley served as long-time CEO for over a decade. In the 1990s, Apple lost considerable market share in the personal computer industry to the lower-priced Wintel duopoly of the Microsoft Windows operating system on Intel-powered PC clones. In 1997, Apple was weeks away from bankruptcy. To resolve its failed operating system strategy, it bought NeXT, effectively bringing Jobs back to the company, who guided Apple back to profitability over the next decade with the introductions of the iMac, iPod, iPhone, and iPad devices to critical acclaim as well as the iTunes Store, launching the "Think different" advertising campaign, and opening the Apple Store retail chain. These moves elevated Apple to consistently be one of the world's most valuable brands since about 2010. Jobs resigned in 2011 for health reasons, and died two months later; he was succeeded as CEO by Tim Cook.

Apple's product lineup includes portable and home hardware sApple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. Founded in 1976 as Apple Computer Company by Steve Jobs, Steve Wozniak and Ronald Wayne, the company was incorporated by Jobs and Wozniak as Apple Computer, Inc. the following year. It was renamed Apple Inc. in 2007 as the company had expanded its focus from computers to consumer electronics. Apple is the largest technology company by revenue, with US$391.04 billion in the 2024 fiscal year.

The company was founded to produce and market Wozniak's Apple I personal computer. Its second computer, the Apple II, became a best seller as one of the first mass-produced microcomputers. Apple introduced the Lisa in 1983 and the Macintosh in 1984, as some of the first computers to use a graphical user interface and a mouse. By 1985, internal company problems led to Jobs leaving to form NeXT, Inc., and Wozniak withdrawing to other ventures; John Sculley served as long-time CEO for over a decade. In the 1990s, Apple lost considerable market share in the personal computer industry to the lower-priced Wintel duopoly of the Microsoft Windows operating system on Intel-powered PC clones. In 1997, Apple was weeks away from bankruptcy. To resolve its failed operating system strategy, it bought NeXT, effectively bringing Jobs back to the company, who guided Apple back to profitability over the next decade with the introductions of the iMac, iPod, iPhone, and iPad devices to critical acclaim as well as the iTunes Store, launching the "Think different" advertising campaign, and opening the Apple Store retail chain. These moves elevated Apple to consistently be one of the world's most valuable brands since about 2010. Jobs resigned in 2011 for health reasons, and died two months later; he was succeeded as CEO by Tim Cook.

Apple's product lineup includes portable and home hardwareApple Inc. is an American multinational technology company headquartered in Cupertino, California, in Silicon Valley. It is best known for its consumer electronics, software, and services. Founded in 1976 as Apple Computer Company by Steve Jobs, Steve Wozniak and Ronald Wayne, the company was incorporated by Jobs and Wozniak as Apple Computer, Inc. the following year. It was renamed Apple Inc. in 2007 as the company had expanded its focus from computers to consumer electronics. Apple is the largest technology company by revenue, with US$391.04 billion in the 2024 fiscal year.

The company was founded to produce and market Wozniak's Apple I personal computer. Its second computer, the Apple II, became a best seller as one of the first mass-produced microcomputers. Apple introduced the Lisa in 1983 and the Macintosh in 1984, as some of the first computers to use a graphical user interface and a mouse. By 1985, internal company problems led to Jobs leaving to form NeXT, Inc., and Wozniak withdrawing to other ventures; John Sculley served as long-time CEO for over a decade. In the 1990s, Apple lost considerable market share in the personal computer industry to the lower-priced Wintel duopoly of the Microsoft Windows operating system on Intel-powered PC clones. In 1997, Apple was weeks away from bankruptcy. To resolve its failed operating system strategy, it bought NeXT, effectively bringing Jobs back to the company, who guided Apple back to profitability over the next decade with the introductions of the iMac, iPod, iPhone, and iPad devices to critical acclaim as well as the iTunes Store, launching the "Think different" advertising campaign, and opening the Apple Store retail chain. These moves elevated Apple to consistently be one of the world's most valuable brands since about 2010. Jobs resigned in 2011 for health reasons, and died two months later; he was succeeded as CEO by Tim Cook.

Apple's product lineup includes portable and home hardwaree""", "real"] ]   ##needs to connect to backend here 

button_pressed = False
id_of_button_pressed = -1

Username = "Beep"


@app.route('/', methods=['GET', 'POST'])
def signin():
    if session.get("user_id"):
        return redirect(url_for('index'), articles=Articles, Username=Username)
    
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
    
    return render_template("signin.html", articles=Articles, Username=Username)


@app.route('/button_pressed', methods=['POST'])
def button_pressed():
    
    button_pressed = True 
    id_of_button_pressed = request.form['button_id']
    print(id_of_button_pressed)
    ## comparison to actual thing happens here. 

    return jsonify({"status": "success", "id": id_of_button_pressed, "win" : "True"})


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

        return redirect(url_for('index'), articles=Articles, Username=Username)

    return render_template("index.html", articles=Articles, Username=Username)


if __name__ == '__main__':
    app.run(debug=True)
    session["user_id"] = None