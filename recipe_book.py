import db

def get_recipes():
    sql = """SELECT t.id, t.title, t.user_id, u.username, t.avg_rating
             FROM recipes t, users u
             WHERE u.id = t.user_id
             GROUP BY t.id
             ORDER BY t.id DESC"""
    return db.query(sql)

def get_recipes_by_user(user_id):
    sql = """SELECT id, title, user_id, avg_rating
             FROM recipes
             WHERE user_id = ?"""
    print(user_id)
    result = db.query(sql, [user_id])
    print(result)
    return result

def add_recipe(title, content, user_id):
    sql = "INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)"
    db.execute(sql, [title, content, user_id])
    recipe_id = db.last_insert_id()
    return recipe_id
    
def add_rating(content, rating, user_id, recipe_id):
    sql = """INSERT INTO ratings (content, rating, user_id, recipe_id)
             VALUES (?, ?, ?, ?)"""
    db.execute(sql, [content, rating, user_id, recipe_id])
    set_average_rating(recipe_id)



def get_recipe(recipe_id):
    sql = """SELECT t.id, t.title, t.user_id, u.username, t.content, t.avg_rating
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

def set_average_rating(recipe_id):
    ratings = get_ratings(recipe_id)
    sum = 0
    for review in ratings:
        sum += review["rating"]
    average = sum / len(ratings)
    sql = "UPDATE recipes SET avg_rating = ? WHERE id = ?"
    db.execute(sql, [average, recipe_id])

    
def update_recipe(message_id, title, content):
    sql = "UPDATE recipes SET content = ?, title = ? WHERE id = ?"
    db.execute(sql, [content, title, message_id])

def update_rating(rating_id, content, rating):
    sql = "UPDATE ratings SET content = ?, rating = ? WHERE id = ?"
    db.execute(sql, [content, rating, rating_id])
    rating = get_rating(rating_id)
    set_average_rating(rating["recipe_id"])


def remove_recipe(recipe_id):
    sql = """DELETE FROM ratings
             WHERE recipe_id = ?"""
    db.execute(sql, [recipe_id])

    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
    
    sql = "DELETE FROM recipes WHERE id = ?"
    db.execute(sql, [recipe_id])

def remove_rating(rating_id):
    sql = "DELETE FROM ratings WHERE id = ?"
    db.execute(sql, [rating_id])
    rating = get_rating(rating_id)
    set_average_rating(rating["recipe_id"])


def search(query):
    sql = """SELECT r.id, r.user_id, r.title, r.content, u.username, u.id, u.username, r.avg_rating
            FROM recipes r, users u
            WHERE (r.user_id = u.id AND r.content like ?) OR (r.user_id = u.id AND r.title like ?)
            """
    like = "%" + query + "%"
    return db.query(sql, [like, like])


def get_all_classes():
    sql = "SELECT title FROM classes"
    return db.query(sql)

def get_classes_of_recipe(recipe_id):
    sql = "SELECT title FROM recipe_classes WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])

def add_recipe_class(recipe_id, new_class):
    sql = "INSERT INTO recipe_classes (recipe_id, title) VALUES (?, ?)"
    db.execute(sql, [recipe_id, new_class])