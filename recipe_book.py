import db

def get_recipes():
    sql = """SELECT t.id, t.title, t.user_id, u.username
             FROM recipes t, users u
             WHERE u.id = t.user_id
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)


def add_recipe(title, content, user_id):
    sql = "INSERT INTO threads (title, user_id) VALUES (?, ?)"
    db.execute(sql, [title, user_id])
    recipe_id = db.last_insert_id()
    add_rating(content, user_id, recipe_id)
    return recipe_id
    
def add_rating(content, user_id, recipe_id):
    sql = """INSERT INTO messages (content, sent_at, user_id, recipe_id)
             VALUES (?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, recipe_id])


def get_recipe(recipe_id):
    sql = "SELECT id, title FROM threads WHERE id = ?"
    return db.query(sql, [recipe_id])[0]

def get_ratings(recipe_id):
    sql = """SELECT m.id, m.content, m.sent_at, m.user_id, u.username
             FROM messages m, users u
             WHERE m.user_id = u.id AND m.recipe_id = ?
             ORDER BY m.id"""
    return db.query(sql, [recipe_id])
