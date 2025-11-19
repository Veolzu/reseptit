# reseptit
A website where users can share their recipes and discover new ones.

Functionality:

- The user can make an account and log in.
- The user can add, edit and remove their recipes.
- Each recipe will have the required ingredients and the recipe.
- The user will be able to see other users' recipes and search for different recipes with either keywords or tags.
- The user's profile page has a list of their recipes and a count for how many recipes in total they have added.
- The user will be able to add one or more classification (vegan, dessert etc.)
- The user will be able to leave a comment and a rating for the recipe. While viewing the recipe, the user will be able to see the comments & the average rating.


Installation Guide:

1. Clone the repository
2. Make an virtual environment by opening the console in the same directory and using the following command
   
  python3 -m venv venv

3. Activate said virtual environment with the following command
     - For windows:
       \venv\Scripts\activate
     - For linux:
       source venv/bin/activate

4. In the virtual environment install flask with the following command:
     pip install flask

5. Create the database with the following command (if you do not have sqlite3, you might need to install it):
     sqlite3 database.db < schema.sql
       
6. After all that the website can be started up with the command:
     flask run


Testing:

testing.py is a script that generates a 1000 users, 10 000 recipes and 100 000 ratings generated at random. Each recipe has a random letter from the alphabet as the content. Each recipe is assigned at random 0-3 classes. However purposefully the mexican tag is left out of the generated data, so testing the search function is easier (when selecting the mexican tag with the generated data, no results should ever appear).

