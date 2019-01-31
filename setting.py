from flask import Flask, render_template, request, redirect
import sqlite3 as sql,os

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
	return ("<h1>Welcome</h1>")

@app.route('/movies')
def getmovies():
  con=sql.connect("static/imdb.db")
  cur=con.cursor()
  cur.execute("select * from movies") #fetching movies details
  inp=cur.fetchall()
  inp = [j for i in inp for j in i]
  cur.execute("select name from producers where producerID = ?",(inp[-1],)) #fetching producer name
  p = cur.fetchone()
  p = [i for i in p] 
  print(inp,p)
  cur.close()
  con.close()
  return ("<h1>Welcome</h1>")

@app.route("/addmovie")
def addmovie():
  con=sql.connect("static/imdb.db")
  cur=con.cursor()
  cur.execute("select name,producerID from producers") # fetching producers details
  prod = cur.fetchall()
  prod = [i for i in prod]
  cur.execute("select name,actorID from actors") # fetching actors details
  actor = cur.fetchall()
  actor = [i for i in actor]
  cur.close()
  con.close()
  return render_template("addmovie.html",actor = actor,prod = prod)

@app.route("/addmovietodb", methods = ['POST'])
def addmovietodb():
  if request.method == "POST":
    name = request.form['name']
    yor = request.form['yor']
    plot = request.form['plot']
    actor = request.form['actors']
    producers = request.form['producers']

    target = os.path.join(APP_ROOT, 'static/images')
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    print(request.files.getlist("file"))
    for upload in request.files.getlist("file"):
        print(upload)
        print("{} is the file name".format(upload.filename))
        filename = upload.filename
        # This is to verify files are supported
        ext = os.path.splitext(filename)[1]
        if (ext == ".jpg") or (ext == ".png") or (ext == ".jpeg"):
            print("File supported moving on...")
        else:
            render_template("<h1>File Not Supported</h1>")
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)
    print(name,yor,plot,actor,producers)
    return redirect("/addmovie")

if __name__=="__main__":
	app.run(debug=True,port=4000)