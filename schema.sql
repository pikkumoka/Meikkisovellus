CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE looks (
	id INTEGER PRIMARY  KEY,
	title TEXT,
	description TEXT,
	makeup TEXT,
	user_id INTEGER REFERENCES users
);

CREATE TABLE classes (
	id INTEGER PRIMARY KEY,
	title TEXT,
	value TEXT
);

CREATE TABLE look_classes (
	id INTEGER PRIMARY  KEY,
	look_id INTEGER REFERENCES looks,
	title TEXT,
	value TEXT
);
