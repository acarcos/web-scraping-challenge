# === MongoDB and Flask Application ===
# Call the scrape file and its functions

# Libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__, static_folder='/web/static')

# PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Get data from database connection
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_data = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Get info from scrape() function
@app.route("/scrape")
def scrape():
    # Run scrape function (.py code and function)
    mars_data_info = scrape_mars.scrape()

    # Save the return dict from Python in Mongo
    mongo.db.collection.update({}, mars_data_info, upsert=True) 

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)

