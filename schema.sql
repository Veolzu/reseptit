CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT, 
    user_id INTEGER REFERENCES users
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    rating TEXT,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);