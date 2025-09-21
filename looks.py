import db

def add_look(title, description, makeup, user_id) :
	sql = """INSERT INTO items (title, description, makeup, user_id)
			VALUES (?, ?, ?, ?)"""
	db.execute(sql, [title, description, makeup, user_id])
