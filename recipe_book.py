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
    return db.query(sql, [recipe_id])[0]

def get_ratings(recipe_id):
    sql = """SELECT r.content, r.rating, r.user_id, r.recipe_id, u.username
             FROM ratings r, users u
             WHERE u.id = r.user_id AND r.recipe_id= ?"""
    return db.query(sql, [recipe_id])

def average_rating(recipe_id):
    ratings = get_ratings(recipe_id)
