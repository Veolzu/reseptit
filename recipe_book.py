import db
def get_recipe_count():
    sql = "SELECT COUNT(id) as count FROM recipes"
    result = db.query(sql)
    return result[0]["count"]



def get_recipes(page, page_size):
    sql = """SELECT t.id, t.title, t.user_id, u.username, t.avg_rating
             FROM recipes t, users u
             WHERE u.id = t.user_id
             GROUP BY t.id
             ORDER BY t.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page - 1)
    return db.query(sql, [limit, offset])

def get_recipes_by_user(user_id):
    sql = """SELECT id, title, user_id, avg_rating
             FROM recipes
             WHERE user_id = ?"""
    result = db.query(sql, [user_id])
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
    sql = """SELECT r.id, r.content, r.rating, r.recipe_id, r.user_id
             FROM ratings r
             WHERE r.id= ?"""
    result = db.query(sql, [rating_id])
    if len(result) == 0:
        return None
    return result[0]

def set_average_rating(recipe_id):
    ratings = get_ratings(recipe_id)
    if len(ratings) > 0:
        the_sum = 0
        for review in ratings:
            the_sum += review["rating"]
        average = round(the_sum / len(ratings), 2)
        sql = "UPDATE recipes SET avg_rating = ? WHERE id = ?"
        db.execute(sql, [average, recipe_id])
    else:
        sql = "UPDATE recipes SET avg_rating = NULL WHERE id = ?"
        db.execute(sql, [recipe_id])

def update_recipe(recipe_id, title, content):
    sql = "UPDATE recipes SET content = ?, title = ? WHERE id = ?"
    db.execute(sql, [content, title, recipe_id])
    sql = "DELETE FROM recipe_classes WHERE recipe_id = ?"
    db.execute(sql, [recipe_id])
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
    recipe_id = get_rating(rating_id)["recipe_id"]
    sql = "DELETE FROM ratings WHERE id = ?"
    db.execute(sql, [rating_id])
    set_average_rating(recipe_id)

def search_with_only_classes(classes, results):
    for tag in classes:
        sql="""
            SElECT c.recipe_id, c.title as class, r.content, r.title, r.user_id, u.username, r.avg_rating, r.id
            FROM recipe_classes c, recipes r, users u
            WHERE c.recipe_id = r.id AND c.title like ? and r.user_id = u.id"""
        promising = db.query(sql, [str(tag)])
        for result in promising:
            if result["recipe_id"] not in results:
                results[result["recipe_id"]] = 0
            results[result["recipe_id"]] += 1
    return promising
def search_with_only_query(query):
    like = "%" + query + "%"
    sql="""
        SElECT  r.content, r.title, r.user_id, u.username, r.avg_rating, r.id
        FROM recipes r, users u
        WHERE r.user_id = u.id AND (r.title LIKE ? OR r.content LIKE ?) """
    true_results = db.query(sql, [like, like])
    return true_results

def search_with_both(query, classes, results):
    like = "%" + query + "%"
    for tag in classes:
        sql="""
            SElECT c.recipe_id, c.title as class, r.content, r.title, r.user_id, u.username, r.avg_rating, r.id
            FROM recipe_classes c, recipes r, users u
            WHERE (c.recipe_id = r.id AND c.title like ? 
            AND r.user_id = u.id AND r.title LIKE ?)
                OR (c.recipe_id = r.id AND c.title like ? 
                AND r.user_id = u.id AND r.content LIKE ?)"""
        promising = db.query(sql, [str(tag), like, str(tag), like])
        for result in promising:
            if result["recipe_id"] not in results:
                results[result["recipe_id"]] = 0
            results[result["recipe_id"]] += 1
    return promising
def search(query, classes, page, page_size):
    true_results = []
    results = {}
    ids = set()
    promising = []
    if query != "" and len(classes) == 0:
        true_results = search_with_only_query(query)

    elif query == "" and len(classes) > 0:
        promising = search_with_only_classes(classes, results)
    else:
        promising = search_with_both(query, classes, results)

    if promising:
        for result in promising:
            if results[result["recipe_id"]] == len(classes):
                if result["recipe_id"] not in ids:
                    ids.add(result["recipe_id"])
                    true_results.append(result)
    try:
        true_results_limited = true_results[(page-1)*page_size:page*page_size]
    except IndexError:
        return (true_results, len(true_results))
    return (true_results_limited, len(true_results))


def get_all_classes():
    sql = "SELECT title FROM classes"
    return db.query(sql)

def get_classes_of_recipe(recipe_id):
    sql = "SELECT title FROM recipe_classes WHERE recipe_id = ?"
    return db.query(sql, [recipe_id])

def add_recipe_class(recipe_id, new_class):
    sql = "INSERT INTO recipe_classes (recipe_id, title) VALUES (?, ?)"
    db.execute(sql, [recipe_id, new_class])
