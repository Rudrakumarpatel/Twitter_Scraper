from flask import Flask, render_template
import twitter_scraper

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/run-script")
def run_script():
    data = twitter_scraper.fetch_trending_topics()
    return render_template("result.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
