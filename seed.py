import random
import sqlite3
import string

data = sqlite3.connect("database.db")

data.execute("DELETE FROM users")
data.execute("DELETE FROM recipes")
data.execute("DELETE FROM ratings")
data.execute("DELETE FROM recipe_classes")

USER_COUNT = 1000
RECIPE_COUNT = 10**6
classes = ["appetizer", "entree", "dessert",
            "vegan", "meat", "chinese"] 
#mexican tag is purposefully missing so you can check if search works
#so after this data-set mexican tag should get no results
for i in range(1, USER_COUNT + 1):
    data.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, RECIPE_COUNT + 1):
    user_id = random.randint(1, USER_COUNT)
    data.execute("INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)",
               ["recipe" + str(i), random.choice(string.ascii_letters), user_id])

    class_indices = list({random.randint(0, 5) for i in range(0, random.randint(0, 3))})
    for indice in class_indices:
        sql = "INSERT INTO recipe_classes (recipe_id, title) VALUES (?, ?)"
        data.execute(sql, [i, classes[indice]])
    the_sum = 0
    n=random.randint(0, 101)
    for j in range(0, n):
        user_id = random.randint(1, USER_COUNT)
        recipe_id = i
        rating = random.randint(1, 10)
        data.execute("""INSERT INTO ratings (content, rating, user_id, recipe_id)
                    VALUES (?, ?, ?, ?)""",
                ["message" + str(i), rating,  user_id, recipe_id])
        the_sum += rating
    if n > 0:
        average = round(the_sum/ n, 2)
        sql = "UPDATE recipes SET avg_rating = ? WHERE id = ?"
        data.execute(sql, [average, i])
data.commit()
data.close()
