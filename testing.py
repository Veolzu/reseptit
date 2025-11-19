import random
import sqlite3
import string
db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM ratings")
db.execute("DELETE FROM recipe_classes")

user_count = 1000
thread_count = 10**5
message_count = 10**6
class_count = 10
classes = ["appetizer", "entree", "dessert", "vegan", "meat", "chinese"] #mexican tag is purposefully missing so you can check if search works
#so after this data-set mexican tag should get no results
for i in range(1, user_count + 1):
    db.execute("INSERT INTO users (username) VALUES (?)",
               ["user" + str(i)])

for i in range(1, thread_count + 1):
    user_id = random.randint(1, user_count)
    db.execute("INSERT INTO recipes (title, content, user_id) VALUES (?, ?, ?)",
               ["recipe" + str(i), random.choice(string.ascii_letters), user_id])
    
    class_indices = list(set([random.randint(0, 5) for i in range(0, random.randint(0, 3))]))
    for indice in class_indices:
        sql = "INSERT INTO recipe_classes (recipe_id, title) VALUES (?, ?)"
        db.execute(sql, [i, classes[indice]])
#rating
for i in range(1, message_count + 1):
    user_id = random.randint(1, user_count)
    thread_id = random.randint(1, thread_count)
    rating = random.randint(1, 10)
    db.execute("""INSERT INTO ratings (content, rating, user_id, recipe_id)
                  VALUES (?, ?, ?, ?)""",
               ["message" + str(i), rating,  user_id, thread_id])
    

db.commit()
db.close()
