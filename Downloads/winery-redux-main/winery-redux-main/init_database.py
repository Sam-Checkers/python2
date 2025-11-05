from flask import Flask
from winery.models import db, Wine
from winery import app

def init_db():
    with app.app_context():
        # Check if we already have wines
        if Wine.query.count() == 0:
            # Import your wine definitions
            from winery.wine_list import (
                red_1, red_2, red_3, red_4, red_5, red_6, red_7,
                white_1, white_2, white_3, white_4,
                lager_1, lager_2, lager_3, lager_4, lager_5
            )
            
            # Add all wines to the database
            wines = [
                red_1, red_2, red_3, red_4, red_5, red_6, red_7,
                white_1, white_2, white_3, white_4,
                lager_1, lager_2, lager_3, lager_4, lager_5
            ]
            
            db.session.add_all(wines)
            db.session.commit()
            print(f"Added {len(wines)} wines to the database")
        else:
            print(f"Database already contains {Wine.query.count()} wines")

# You can call this function from your main application file
if __name__ == "__main__":
    init_db()