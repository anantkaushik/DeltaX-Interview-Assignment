from flask import Flask
import os

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
	return ("<h1>Welcome</h1>")

if __name__=="__main__":
	app.run(debug=True,port=4000)