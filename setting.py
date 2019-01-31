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
  prod = []
  for i in inp:
    temp = []
    for j in i:
      temp.append(j)
    prod.append(temp)
  print(prod)
  for i in prod:
    temp = eval(i[-2])
    i[-2] = []
    for j in temp:
      cur.execute("select name from actors where actorID = ?",(int(j),))
      ac = cur.fetchone()
      ac = [i for i in ac]
      i[-2].extend(ac)
  print(prod)
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
    actor = request.form.getlist('actors')
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
    print(name,yor,plot,actor,producers,filename)
    actor = str(actor)
    con=sql.connect("static/imdb.db")
    cur=con.cursor()
    cur.execute("INSERT INTO movies (name,yearofrelease,plot,poster,actors,producers)VALUES (?,?,?,?,?,?)",(name,yor,plot,filename,actor,producers) ) # fetching producers details
    con.commit()
    cur.close()
    con.close()
    return redirect("/addmovie")

@app.route("/addactor", methods = ['POST'])
def addactor():
  if request.method == "POST":
    name = request.form['namea']
    sex = request.form['sexa']
    dob = request.form['doba']
    bio = request.form['bioa']
    con=sql.connect("static/imdb.db")
    cur=con.cursor()
    cur.execute("INSERT INTO actors (name,sex,DOB,Bio)VALUES (?,?,?,?)",(name,sex,dob,bio)) 
    con.commit()
    cur.close()
    con.close()
    return redirect("/")

@app.route("/addproducer", methods = ['POST'])
def addproducer():
  if request.method == "POST":
    name = request.form['namep']
    sex = request.form['sexp']
    dob = request.form['dobp']
    bio = request.form['biop']
    con=sql.connect("static/imdb.db")
    cur=con.cursor()
    cur.execute("INSERT INTO producers (name,sex,DOB,Bio)VALUES (?,?,?,?)",(name,sex,dob,bio)) 
    con.commit()
    cur.close()
    con.close()
    return redirect("/")

if __name__=="__main__":
	app.run(debug=True,port=4000)