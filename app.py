import sqlite3
from flask import Flask
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import config
import db
import looks

app = Flask(__name__)
app.secret_key = config.secret_key

#Homepage
@app.route("/")
def index() :
	all_looks = looks.get_looks()
	return render_template("index.html", looks=all_looks)

#See looks
@app.route("/look/<int:look_id>")
def get_look(look_id) :
	look = looks.get_look(look_id)
	return render_template("show_look.html", look=look)
	
#Find looks
@app.route("/find_look")
def find_look():
    query = request.args.get("query")
    if query:
        results = looks.find_looks(query)
    else:
        query = ""
        results = []
    return render_template("find_look.html", query=query, results=results)

#New look
@app.route("/new_look")
def new_look():
    return render_template("new_look.html")

#Upload makeuplook
@app.route("/create_look", methods=["POST"])
def create_look():
	title = request.form["title"]
	description = request.form["description"]
	makeup = request.form["makeup"]
	user_id = session["user_id"]

	looks.add_look(title, description, makeup, user_id)

	return redirect("/")

#Edit look
@app.route("/edit_look/<int:look_id>")
def edit_look(look_id) :
	look = looks.get_look(look_id)
	return render_template("edit_look.html", look=look)

#Upload updated makeuplook
@app.route("/update_look", methods=["POST"])
def update_look() :
	look_id = request.form["look_id"]
	title = request.form["title"]
	description = request.form["description"]
	makeup = request.form["makeup"]

	looks.update_look(look_id, title, description, makeup)

	return redirect("/look/" + str(look_id))

#Remove look
@app.route("/remove_look/<int:look_id>", methods=["GET", "POST"])
def remove_look(look_id) :
	if request.method == "GET" :
		look = looks.get_look(look_id)
		return render_template("remove_look.html", look=look)

	if request.method == "POST" :
		if "remove" in request.form :
			looks.remove_look(look_id)
			return redirect("/")
		else :
			return redirect("/look/" + str(look_id))

#Registration
@app.route("/register")
def register() :
    return render_template("register.html")

#Create account
@app.route("/create", methods=["POST"])
def create() :
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"

    return "Tunnus luotu"

#Login
@app.route("/login", methods=["GET", "POST"])
def login() :
	if request.method == "GET" :
		return render_template("login.html")

	if request.method == "POST" :
		username = request.form["username"]
		password = request.form["password"]

		sql = "SELECT id, password_hash FROM users WHERE username = ?"
		result = db.query(sql, [username])[0]
		user_id = result["id"]
		password_hash = result["password_hash"]

		if check_password_hash(password_hash, password):
			session["user_id"] = user_id
			session["username"] = username
			return redirect("/")
		else:
			return "VIRHE: väärä tunnus tai salasana"

#Logout
@app.route("/logout")
def logout() :
    del session["user_id"]
    del session["username"]
    return redirect("/")
