CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE items (
	id INTEGER PRIMARY  KEY,
	title TEXT,
	description TEXT,
	makeup TEXT,
	user_id INTEGER REFERENCES users
);
