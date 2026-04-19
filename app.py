import secrets
import sqlite3
from flask import Flask
from flask import abort, make_response, redirect, render_template, request, session, flash
import config
import db
import looks
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login() :
	if "user_id" not in session :
		abort(403)

def check_csrf():
	if "csrf_token" not in request.form :
		abort(403)
	if request.form["csrf_token"] != session["csrf_token"]:
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
	comments = looks.get_comments(look_id)

	return render_template("show_look.html", look=look, classes=classes, comments=comments)

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

#Show look image
@app.route("/image/<int:look_id>")
def show_image(look_id):
    image = looks.get_image(look_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpg")
    return response

#Upload new makeuplook
@app.route("/create_look", methods=["POST"])
def create_look() :
	require_login()
	check_csrf()

	title = request.form["title"]
	if not title or len(title) > 50 :
		abort(403)
	description = request.form["description"]
	if len(description) > 1000 :
		abort(403)
	user_id = session["user_id"]

	if "image" not in request.files:
		flash("Kuva puuttuu")
		return redirect("/create_look")
	file = request.files["image"]
	if not file.filename.endswith(".jpg"):
		flash("Tarkistathan, että tiedosto on jpg")

	image = file.read()
	if len(image) > 1000 * 1024:
		flash("Kuvasi on liian suuri")

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

	looks.add_look(title, description, user_id, image, classes)

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
	check_csrf()

	look_id = request.form["look_id"]
	look = looks.get_look(look_id)
	if not look :
		abort(404)
	if look["user_id"] != session["user_id"] :
		abort(403)

	title = request.form["title"]
	if not title or len(title) > 50 :
		abort(403)

	image = look["image"]
	if "image" in request.files:
		file = request.files["image"]
		if file and file.filename :
			if not file.filename.endswith(".jpg"):
				flash(f"Tarkistathan, että tiedosto on jpg, koko = {len(image)}")
				return redirect("/edit_look/" + str(look_id))

			image = file.read()
			if len(image) > 1000 * 1024:
				flash(f"Kuvasi on liian suuri = {len(image)}")
				return redirect("/edit_look/" + str(look_id))

	description = request.form["description"]
	if len(description) > 1000 :
		abort(403)

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

	looks.update_look(look_id, title, description, image, classes)

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
		check_csrf()
		if "remove" in request.form :
			looks.remove_look(look_id)
			return redirect("/")
		else :
			return redirect("/look/" + str(look_id))

#Add comment
@app.route("/new_comment", methods=["POST"])
def new_comment():
	require_login()
	check_csrf()

	content = request.form["content"]
	user_id = session["user_id"]
	look_id = request.form["look_id"]

	looks.add_comment(content, user_id, look_id)
	return redirect("/look/" + str(look_id))

#Delete comment
@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment(comment_id):
	require_login()
	comment = looks.get_comment(comment_id)

	if request.method == "GET":
		return render_template("remove_comment.html", comment=comment)

	if request.method == "POST" :
		check_csrf()
		if "remove" in request.form :
			looks.remove_comment(comment["id"])
		return redirect("/look/" + str(comment["look_id"]))

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

	if len(username) <= 0 or len(username) >= 21 :
		flash("Tunnus pitää olla ainakin yhden mutta alle 20 merkin pituinen")
		return redirect("/register")

	if password1 != password2 :
		flash("Salasanat eivät täsmää, kokeile uudestaan")
		return redirect("/register")

	if len(password1) <= 4 or len(password2) <= 4 :
		flash("Salasanan tulee olla ainakin 5 merkkiä pitkä!")
		return redirect("/register")

	try :
		users.create_user(username, password1)

	except sqlite3.IntegrityError:
		flash("Tunnus on jo varattu, valitse toinen nimi")
		return redirect("/register")

	flash("Tunnus luotu, kirjaudu sisään")
	return redirect("/login")

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
			session["csrf_token"] = secrets.token_hex(16)
			return redirect("/")
		else:
			flash("Väärä tunnus tai salasana, yritä uudestaan")
			return redirect("/login")

#Logout
@app.route("/logout")
def logout() :
	if "user_id" in session :
		del session["user_id"]
		del session["username"]
	return redirect("/")