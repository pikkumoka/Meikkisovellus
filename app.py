import sqlite3
from flask import Flask
from flask import abort, redirect, render_template, request, session
import config
import db
import looks
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login() :
	if "user_id" not in session :
		abort(403)

#Homepage
@app.route("/")
def index() :
	all_looks = looks.get_looks()
	return render_template("index.html", looks=all_looks)

#See user profile
@app.route("/user/<int:user_id>")
def show_user(user_id) :
	user = users.get_user(user_id)
	if not user :
		abort(404)
	looks = users.get_looks(user_id)
	return render_template("show_user.html", user=user, looks=looks)

#See looks
@app.route("/look/<int:look_id>")
def get_look(look_id) :
	look = looks.get_look(look_id)
	if not look :
		abort(404)
	classes = looks.get_classes(look_id)

	return render_template("show_look.html", look=look, classes=classes)
	
#Find looks
@app.route("/find_look")
def find_look() :
    query = request.args.get("query")
    if query:
        results = looks.find_looks(query)
    else:
        query = ""
        results = []
    return render_template("find_look.html", query=query, results=results)

#New look
@app.route("/new_look")
def new_look() :
	require_login()
	classes = looks.get_all_classes()
	return render_template("new_look.html", classes=classes)

#Upload makeuplook
@app.route("/create_look", methods=["POST"])
def create_look() :
	require_login()

	title = request.form["title"]
	if not title or len(title) > 50 :
		abort(403)
	description = request.form["description"]
	if len(description) > 1000 :
		abort(403)
	makeup = request.form["makeup"]
	user_id = session["user_id"]

	all_classes = looks.get_all_classes()
	classes = []
	for entry in request.form.getlist("classes") :
		if entry :
			class_title, class_value = entry.split(":")
			if class_title not in all_classes :
				abort(403)
			if class_value not in all_classes[class_title] :
				abort(403)
			classes.append((class_title, class_value))

	looks.add_look(title, description, makeup, user_id, classes)

	return redirect("/")

#Edit look
@app.route("/edit_look/<int:look_id>")
def edit_look(look_id) :
	require_login()
	look = looks.get_look(look_id)
	if not look :
		abort(404)
	if look["user_id"] != session["user_id"] :
		abort(403)

	all_classes = looks.get_all_classes()
	classes = {}
	for my_class in all_classes :
		classes[my_class] = ""
	for entry in looks.get_classes(look_id) :
		classes[entry["title"]] = entry["value"]

	return render_template("edit_look.html", look=look, classes=classes,
	all_classes=all_classes)

#Upload updated makeuplook
@app.route("/update_look", methods=["POST"])
def update_look() :
	require_login()
	look_id = request.form["look_id"]
	look = looks.get_look(look_id)
	if not look :
		abort(404)
	if look["user_id"] != session["user_id"] :
		abort(403)

	title = request.form["title"]
	if not title or len(title) > 50 :
		abort(403)
	description = request.form["description"]
	if len(description) > 1000 :
		abort(403)
	makeup = request.form["makeup"]

	all_classes = looks.get_all_classes()
	classes = []
	for entry in request.form.getlist("classes") :
		if entry :
			class_title, class_value = entry.split(":")
			if class_title not in all_classes :
				abort(403)
			if class_value not in all_classes[class_title] :
				abort(403)
			classes.append((class_title, class_value))

	looks.update_look(look_id, title, description, makeup, classes)

	return redirect("/look/" + str(look_id))

#Remove look
@app.route("/remove_look/<int:look_id>", methods=["GET", "POST"])
def remove_look(look_id) :
	require_login()
	look = looks.get_look(look_id)
	if not look :
		abort(404)
	if look["user_id"] != session["user_id"] :
		abort(403)
		
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

	try :
		users.create_user(username, password1)
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

		user_id = users.check_login(username, password)
		if user_id :
			session["user_id"] = user_id
			session["username"] = username
			return redirect("/")
		else:
			return "VIRHE: väärä tunnus tai salasana"

#Logout
@app.route("/logout")
def logout() :
	if "user_id" in session :
		del session["user_id"]
		del session["username"]
	return redirect("/")
