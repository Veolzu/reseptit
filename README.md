# Shavor & Share
The only online recipe book you will ever need.

Functionality:

- The user can make an account and log in.
- The user can add, edit and remove their recipes.
- Each recipe will have the required ingredients and the recipe.
- The user will be able to see other users' recipes and search for different recipes with either keywords or tags.
- The user's profile page has a list of their recipes and a count for how many recipes in total they have added.
- The user will be able to add one or more classification (vegan, dessert etc.)
- The user will be able to leave a comment and a rating for the recipe. While viewing the recipe, the user will be able to see the comments & the average rating.


# Installation Guide:

1. Clone the repository
2. Make an virtual environment by opening the console in the same directory and using the following command
```
python3 -m venv venv
```
3. Activate said virtual environment with the following command
- For windows:
```
\venv\Scripts\activate
```
- For linux:
```
source venv/bin/activate
```
4. In the virtual environment install flask with the following command:
```
pip install flask
```
5. Create the database with the following commands (if you do not have sqlite3, you might need to install it):
```
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
```    
6. After all that the website can be started up with the command:
```
flask run
```

# Testing large amounts of data:

seed.py is a script that generates a 1000 users and a million recipes. Each recipe has a random letter from the alphabet as the content. Each recipe also has a random amount (between 0 and 101) of generated reviews. Each recipe is assigned at random 0-3 classes. However purposefully the mexican tag is left out of the generated data, so testing the search function is easier (when selecting the mexican tag with the generated data, no results should ever appear).

Note: running the seed.py file with a 1000 users and a million recipes will take long, with my school laptop it took around 11 minutes. However with a 1000 users and only a 100 000 recipes, the script took around a minute. 

Results with a thousand users, million recipes (each recipe has a random number of 0-101 ratings generated) as per seed.py file:
without any indexes:
```
1. loading the front page: roughly 0.10 - 0.3s
2. loading a recipe: 3.7s-4s
3. loading a user's profile: 0.1s
4. search: 1-2s
```
the biggest problem with loading the recipe is searching the ratings belonging to the recipe. This can be improved with a index on ratings by recipe_id. After that loading a recipe's page is reduced to rougly 0.1s.

As per my current testing, the search function is unlikely to be largely speeded up by indexes (the for-loops are likely to be the problem, not the sql queries)

