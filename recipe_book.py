import db

def get_recipes():
    sql = """SELECT t.id, t.title, t.user_id, u.username
             FROM recipes t, users u
             WHERE u.id = t.user_id
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)


def add_recipe(title, content, user_id):
    sql = "INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, content, user_id])
    recipe_id = db.last_insert_id()
    return recipe_id
    
def add_rating(content, rating, user_id, recipe_id):
    sql = """INSERT INTO ratings (content, rating, user_id, recipe_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [content, rating, user_id, recipe_id])



def get_recipe(recipe_id):
    sql = """SELECT t.id, t.title, t.user_id, u.username, t.content
             FROM recipes t, users u
             WHERE u.id = t.user_id AND t.id= ?"""
    result = db.query(sql, [recipe_id])
    if len(result) == 0:
        return None
    return result[0]

def get_ratings(recipe_id):
    sql = """SELECT r.id, r.content, r.rating, r.user_id, r.recipe_id, u.username
             FROM ratings r, users u
             WHERE u.id = r.user_id AND r.recipe_id= ?"""
    return db.query(sql, [recipe_id])

def get_rating(rating_id):
    sql = """SELECT r.id, r.content, r.rating, r.recipe_id
             FROM ratings r
             WHERE r.id= ?"""
    result = db.query(sql, [rating_id])
    if len(result) == 0:
        return None
    return result[0]

def average_rating(recipe_id):
    ratings = get_ratings(recipe_id)

def update_recipe(message_id, title, content):
    sql = "UPDATE recipes SET content = ?, title = ? WHERE id = ?"
    db.execute(sql, [content, title, message_id])

def update_rating(rating_id, content, rating):
    sql = "UPDATE ratings SET content = ?, rating = ? WHERE id = ?"
    db.execute(sql, [content, rating, rating_id])


def remove_recipe(recipe_id):
    sql = """DELETE FROM ratings
             WHERE recipe_id = ?"""
    db.execute(sql, [recipe_id])
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def remove_rating(rating_id):
    sql = "DELETE FROM ratings WHERE id = ?"
    db.execute(sql, [rating_id])