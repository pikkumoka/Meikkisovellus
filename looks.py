import db

def get_all_classes() :
	sql = "SELECT title, value FROM classes ORDER BY id"
	result = db.query(sql)

	classes = {}
	for title, value in result :
		classes[title] = []
	for title, value in result :
		classes[title].append(value)

	return classes

def add_look(title, description, makeup, user_id, classes) :
	sql = """INSERT INTO looks (title, description, makeup, user_id)
			VALUES (?, ?, ?, ?)"""
	db.execute(sql, [title, description, makeup, user_id])

	look_id = db.last_insert_id()

	sql = """INSERT INTO look_classes (look_id, title, value)
	VALUES(?, ?, ?)"""
	for  title, value in classes :
		db.execute(sql, [look_id, title, value])

def get_classes(look_id) :
	sql = """SELECT title, value
			FROM look_classes
			WHERE look_id = ?"""
	return db.query(sql, [look_id])

def get_looks() :
	sql = """SELECT id, title
			FROM looks
			ORDER BY id DESC"""
	return db.query(sql)

def get_look(look_id) :
	sql = """SELECT l.id, l.title, l.description, l.makeup, u.id user_id, u.username
			FROM looks l, users u
			WHERE l.user_id = u.id AND
				l.id = ?"""
	result =  db.query(sql, [look_id])
	return result[0] if result else None

def update_look(look_id, title, description, makeup, classes) :
	sql = """UPDATE looks SET title = ?, description =?, makeup = ?
			WHERE id = ?"""
	db.execute(sql, [title, description, makeup, look_id])

	sql = "DELETE FROM look_classes WHERE look_id = ?"
	db.execute(sql, [look_id])

	sql = """INSERT INTO look_classes (look_id, title, value)
	VALUES(?, ?, ?)"""
	for  title, value in classes :
		db.execute(sql, [look_id, title, value])

def remove_look(look_id) :
	sql = "DELETE FROM look_classes WHERE look_id = ?"
	db.execute(sql, [look_id])

	sql = "DELETE FROM looks WHERE id = ?"
	db.execute(sql, [look_id])

def find_looks(query) :
	sql = """SELECT id, title
			FROM looks
			WHERE description LIKE ? OR title LIKE ?
			ORDER BY id DESC"""
	like = "%" + query + "%"
	return db.query(sql, [like, like])
