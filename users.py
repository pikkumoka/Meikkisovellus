from werkzeug.security import check_password_hash, generate_password_hash
import db

def get_user(user_id) :
	sql = """SELECT id, username, created_at, profile_picture
			FROM users WHERE id = ?"""
	result =  db.query(sql, [user_id])
	return result[0] if result else None

def get_looks(user_id) :
	sql = """SELECT id, title
			FROM looks
			WHERE user_id = ?
			ORDER BY id DESC
			"""
	return db.query(sql, [user_id])

def get_profile_picture(user_id) :
	sql = "SELECT profile_picture FROM users WHERE id = ?"
	result = db.query(sql, [user_id])
	return result[0][0] if result else None

def create_user(username, password) :
	password_hash = generate_password_hash(password)
	sql = """INSERT INTO users (username, password_hash, created_at)
			VALUES (?, ?, datetime('now'))"""
	db.execute(sql, [username, password_hash])

def update_user(id, picture) :
	sql = "UPDATE users SET profile_picture = ? WHERE id = ?"
	db.execute(sql, [picture, id])

def check_login(username, password) :
	sql = "SELECT id, password_hash FROM users WHERE username = ?"
	result = db.query(sql, [username])
	if not result :
		return None

	user_id = result[0]["id"]
	password_hash = result[0]["password_hash"]

	if check_password_hash(password_hash, password) :
		return user_id
	else :
		return None
