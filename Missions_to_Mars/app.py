
# declare environment
from flask import Flask, render_template, redirect
import pymongo
import scrape_mars


###################################################################
#
# Web Scraping Challenge      due 27-Feb-2021
#       Kate Spitzer
#
# This project scrapes several Mars-related web pages and displays
# the scraped elements on a web page.
#
# This script uses flask.  It reads saved data from a mongo 
# database, and displays the page.  Upon button click, it calls a
# scraping function to refresh the database and display the new
# data on the page.
#
#
##################################################################


# initialize flask
app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mars database and set tablename
db = client.mars_db
mars_info = db.mars_info


# route to render index.html template using data from Mongo
@app.route("/")
def index():

    # find one record of data from the mongo database
    mars_data = mars_info.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_data)


# route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # run the scrape function
    mars_data = scrape_mars.scrape()

    # update the Mongo database using update and upsert=True
    mars_info.update({}, mars_data, upsert=True)

    # redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
