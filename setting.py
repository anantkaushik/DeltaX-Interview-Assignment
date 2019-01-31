from flask import Flask, render_template, request, redirect
import sqlite3 as sql,os,json

app=Flask(__name__)
app.config["CACHE_TYPE"] = "null"
app.secret_key = os.urandom(24)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
	return redirect("/movies")

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
    pList = eval(i[-1])
    print(pList)
    i[-2],i[-1] = [],[]
    for j in temp:
      cur.execute("select name from actors where actorID = ?",(int(j),))
      ac = cur.fetchone()
      ac = [i for i in ac]
      i[-2].extend(ac)
    cur.execute("select name from producers where producerID = ?",(pList,))
    ac = cur.fetchone()
    ac = [i for i in ac]
    i[-1].extend(ac)
  print(prod)
  cur.close()
  con.close()
  return render_template("movies.html",prod = prod)

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
    return redirect("/movies")

@app.route('/updatemovie', methods = ['GET','POST'])
def updatemovie():
        mov_id = request.form['newid']
        edit = request.form['newn']
        
        conn = sql.connect('static/imdb.db')
        cur = conn.cursor()
        print(edit[1:-2])
        if mov_id[1:-2]=='name':
                cur.execute("UPDATE movies SET name=? WHERE movieID=?",(edit, int(mov_id[-2:]),))
                conn.commit()
        elif mov_id[1:-2]=='yor':
                cur.execute("UPDATE movies SET yearofrelease=? WHERE movieID=?",(edit, int(mov_id[-2:]),))
                conn.commit()
        elif mov_id[1:-2]=='bio':
                cur.execute("UPDATE movies SET plot=? WHERE movieID=?",(edit, int(mov_id[-2:]),))
                conn.commit()
        cur.close()
        conn.close()
        print(edit,mov_id)
        #return json.dumps({'status':200, 'edit':edit, 'movid':mov_id})
        return redirect('/movies')
        
@app.route('/addActor', methods=['POST'])       #background AJAX function
def addActor():
    actorname =  request.form['actorname']
    sex = request.form['sex']
    dob = request.form['dob']
    bio = request.form['bio']
    conn = sql.connect('static/imdb.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO actors (name, sex, DOB, Bio) VALUES (?,?,?,?)",
                (actorname, sex, dob, bio,))
    conn.commit()
    cur.execute("SELECT actorID, name from actors order by actorID desc;")
    res = cur.fetchone()
    arr = []
    for i in res:
      arr.append(i)
    cur.close()
    conn.close()
    
    return json.dumps({'status':200, 'actorID':arr[0], 'actorName':arr[1]})

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
    cur.execute("SELECT producerID, name from producers order by producerID desc;")
    res = cur.fetchone()
    arr = []
    for i in res:
      arr.append(i)
    cur.close()
    con.close()
    return json.dumps({'status':200, 'prodID':arr[0], 'prodName':arr[1]})

if __name__=="__main__":
	app.run(debug=True,port=4000)