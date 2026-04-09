CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE looks (
	id INTEGER PRIMARY KEY,
	title TEXT,
	description TEXT,
	user_id INTEGER REFERENCES users,
	image BLOB
);

CREATE TABLE classes (
	id INTEGER PRIMARY KEY,
	title TEXT,
	value TEXT
);

CREATE TABLE look_classes (
	id INTEGER PRIMARY KEY,
	look_id INTEGER REFERENCES looks,
	title TEXT,
	value TEXT
);

CREATE TABLE comments (
	id INTEGER PRIMARY KEY,
	look_id INTEGER REFERENCES looks,
	user_id INTEGER REFERENCES users,
	content TEXT,
	sent_at TEXT
);