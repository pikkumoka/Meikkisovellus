import db

def add_look(title, description, makeup, user_id) :
	sql = """INSERT INTO looks (title, description, makeup, user_id)
			VALUES (?, ?, ?, ?)"""
	db.execute(sql, [title, description, makeup, user_id])

def get_looks() :
	sql = """SELECT id, title
			FROM looks
			ORDER BY id DESC"""
	return db.query(sql)

def get_look(look_id) :
	sql = """SELECT l.title, l.description, l.makeup, u.username
			FROM looks l, users u
			WHERE l.user_id = u.id AND
				l.id = ?"""
	return db.query(sql, [look_id])[0]
