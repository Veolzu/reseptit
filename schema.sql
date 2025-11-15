CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT,
    image BLOB
);

CREATE TABLE recipes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT, 
    user_id INTEGER REFERENCES users,
    avg_rating REAL
);

CREATE TABLE ratings (
    id INTEGER PRIMARY KEY,
    content TEXT,
    rating INTEGER,
    user_id INTEGER REFERENCES users,
    recipe_id INTEGER REFERENCES recipes
);