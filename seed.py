import random
import sqlite3
import string

import recipe_book
import db
data = sqlite3.connect("database.db")

data.execute("DELETE FROM users")
data.execute("DELETE FROM recipes")
data.execute("DELETE FROM ratings")
data.execute("DELETE FROM recipe_classes")

user_count = 1000
recipe_count = 10**5
rating_count = 10**6
classes = ["appetizer", "entree", "dessert", "vegan", "meat", "chinese"] #mexican tag is purposefully missing so you can check if search works
#so after this data-set mexican tag should get no results
for i in range(1, user_count + 1):
    data.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, recipe_count + 1):
    user_id = random.randint(1, user_count)
    data.execute("INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)",
               ["recipe" + str(i), random.choice(string.ascii_letters), user_id])
    
    class_indices = list(set([random.randint(0, 5) for i in range(0, random.randint(0, 3))]))
    for indice in class_indices:
        sql = "INSERT INTO recipe_classes (recipe_id, title) VALUES (?, ?)"
        data.execute(sql, [i, classes[indice]])
#rating
for i in range(1, rating_count + 1):
    user_id = random.randint(1, user_count)
    thread_id = random.randint(1, recipe_count)
    rating = random.randint(1, 10)
    data.execute("""INSERT INTO ratings (content, rating, user_id, recipe_id)
                  VALUES (?, ?, ?, ?)""",
               ["message" + str(i), rating,  user_id, thread_id])


data.commit()
data.close()

