# Import Dependencies 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")

@app.route("/")
def home(): 

    mars_info = mongo.db.mars_info.find_one()

    return render_template("index.html", mars_info=mars_info)

# Route for scrape function
@app.route("/scrape")
def scrape(): 

    # Scrape data
    mars_info = mongo.db.mars_info
    data = scrape_mars.scrape_mars_news()
    data = scrape_mars.scrape_mars_image()
    data = scrape_mars.scrape_mars_facts()
    data = scrape_mars.scrape_mars_hemispheres()
    mars_info.update({}, data, upsert=True)

    return redirect("/")

if __name__ == "__main__": 
    app.run(debug= True)
