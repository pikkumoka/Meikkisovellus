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

def add_look(title, description, user_id, image, classes) :
	sql = """INSERT INTO looks (title, description, user_id, image)
			VALUES (?, ?, ?, ?)"""
	db.execute(sql, [title, description, user_id, image])

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
	sql = """SELECT l.id, l.title, u.id user_id, u.username
			FROM looks l, users u
			WHERE l.user_id = u.id
			ORDER BY l.id DESC"""
	return db.query(sql)

def get_look(look_id) :
	sql = """SELECT l.id, l.title, l.description, l.image, u.id user_id, u.username
			FROM looks l, users u
			WHERE l.user_id = u.id AND
				l.id = ?"""
	result =  db.query(sql, [look_id])
	return result[0] if result else None

def update_look(look_id, title, description, image, classes) :
	sql = """UPDATE looks SET title = ?, description = ?, image = ?
			WHERE id = ?"""
	db.execute(sql, [title, description, image, look_id])

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

def get_image(look_id) :
	sql = "SELECT image FROM looks WHERE id = ?"
	result = db.query(sql, [look_id])
	return result[0][0] if result else None

def add_comment(content, user_id, look_id) :
	sql = """INSERT INTO comments (look_id, user_id, content, sent_at)
			VALUES (?, ?, ?, datetime('now'))"""
	db.execute(sql, [look_id, user_id, content])

def get_comments(look_id) :
	sql = """SELECT c.id, c.content, c.sent_at, c.user_id, u.username
			FROM comments c, users u
			WHERE c.user_id = u.id AND c.look_id = ?
			ORDER BY c.id"""
	return db.query(sql, [look_id])