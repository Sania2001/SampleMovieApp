import flask
from flask import Flask, request, render_template, redirect, session
import sqlite3
from flask_session import Session
conn = sqlite3.connect("Theatre.db", check_same_thread=False)
cursor = conn.cursor()

listOfTables= conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='owners' ").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE owners(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT, 
                            area TEXT, 
                            city TEXT, 
                            phone INTEGER,
                            email TEXT, 
                            username TEXT, 
                            Password TEXT); ''')
    print("Table has created")

Movies_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='PICTURE'").fetchall()
shows_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='SHOWS'").fetchall()


if Movies_table:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE PICTURE(
                            MOVIEID INTEGER PRIMARY KEY AUTOINCREMENT,
                            MOVIENAME TEXT,
                            LANGUAGE TEXT,
                            MOVIEANIMATION TEXT,
                            SHOWSTART TEXT,
                             SHOWEND TEXT,
                             CITYNAME TEXT); ''')
    print("Table has created...!")


if shows_table:
    print("Table Already Exists ! ")

else:
    conn.execute(''' CREATE TABLE SHOWS(
                            SHOWID INTEGER PRIMARY KEY AUTOINCREMENT,
                            MOVIENAME TEXT,
                            HALLID INTEGER,
                            TIME INTEGER,
                            DATE INTEGER,
                            PRICEID INTEGER,
                            CityName TEXT); ''')
    print("Table has created")

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        getUsername = request.form["username"]
        getppass = request.form["password"]

        if getUsername == "admin":
            if getppass == "12345":
                return redirect("/admin")
    return render_template("login.html")


@app.route("/admin", methods=["GET", "POST"])
def admin():
    return render_template("admin.html")


@app.route("/ownerEntry", methods=["GET", "POST"])
def owner():
    if request.method == "POST":
        getName = request.form["name"]
        getArea = request.form["area"]
        getCity = request.form["city"]
        getPhone = request.form["phone"]
        getEmail = request.form["email"]
        getUsername = request.form["username"]
        getPassword = request.form["password"]

        print(getName)
        print(getArea)
        print(getCity)
        print(getPhone)
        print(getEmail)
        print(getUsername)
        print(getPassword)

        try:
            conn.execute("INSERT INTO owners(name, area, city, phone, email, username, password )VALUES('"+getName+"','"+getArea+"','"+getCity+"','"+getPhone+"','"+getEmail+"','"+getUsername+"','"+getPassword+"')")
            print("Successfully inserted")
            conn.commit()

        except Exception as e:
            print(e)
    return render_template("ownerEntry.html")




@app.route("/view")
def view():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM owners")
    res = cursor.fetchall()
    return render_template("viewall.html", book=res)


@app.route("/cardview")
def cardview():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM owners")
    result = cursor.fetchall()
    return render_template("cardview.html", book = result)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        getName = request.form["name"]
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM owners WHERE name = '"+getName+"' ")
        result = cursor.fetchall()
        return render_template("searchOwner.html", books=result)
    return render_template("search.html")


@app.route("/delete", methods =['GET','POST'])
def delete():
        if request.method == "POST":
            getName = request.form["name"]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM owners WHERE name = '" + getName + "' ")
            conn.commit()
        return render_template("delete.html")

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/login-owner", methods=['GET', 'POST'])
def loginOwner():
    if request.method == "POST":
        getUsername = request.form["username"]
        getPassword = request.form["password"]
        print(getUsername)
        print(getPassword)
        cur2 = conn.cursor()
        cur2.execute(
            "SELECT * FROM owners WHERE username = '" + getUsername + "' AND password = '" + getPassword + "'")
        res2 = cur2.fetchall()
        if len(res2) > 0:
            for i in res2:
                getName = i[1]
                getid = i[0]

            session["name"] = getName
            session["id"] = getid

            return redirect("/ownerdashboard")
    return render_template("owner_login.html")
    # if request.method == 'POST':
    #     getUname = request.form["uname"]
    #     getpass = request.form["pswd"]
    # try:
    #     if getUname == 'owner' and getpass == "12345":
    #         return redirect("/dashboard")
    #     else:
    #         print("Invalid username and password")
    # except Exception as e:
    #     print(e)
    #
    # return render_template("/owner_login.html")





@app.route("/ownerdashboard", methods=["GET", "POST"])
def dashboard():
    if request.method == "POST":
        getMovieName = request.form["moviename"]
        getLanguage = request.form["mlanguage"]
        getAnimation = request.form["manimation"]
        getShow_Start = request.form["showstart"]
        getShow_End = request.form["showend"]
        getCityName = request.form["cityname"]

        print(getMovieName)
        print(getLanguage)
        print(getAnimation)
        print(getShow_Start)
        print(getShow_End)
        print(getCityName)
        try:
            data = (getMovieName, getLanguage, getAnimation, getShow_Start, getShow_End, getCityName)
            insert_query = '''INSERT INTO PICTURE(MOVIENAME, LANGUAGE, MOVIEANIMATION, SHOWSTART, SHOWEND, CITYNAME) 
                                    VALUES (?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Movie added successfully")
            return redirect("/viewall")

        except Exception as e:
            print(e)
    return render_template("dashboard.html")



@app.route("/viewallmovies")
def viewall():
    cur = conn.cursor()
    cur.execute("SELECT * FROM PICTURE")
    res = cur.fetchall()
    return render_template("viewallmovies.html", cinemas=res)

@app.route("/showsDashboard", methods=["GET", "POST"])
def arrangeShows():
    if request.method == "POST":
        getMOvieName = request.form["mname"]
        getHallId = request.form["hid"]
        getTime = request.form["shtime"]
        getDate = request.form["shdate"]
        getPriceId = request.form["prid"]
        getCItyName = request.form["ciname"]

        print(getMOvieName)
        print(getHallId)
        print(getTime)
        print(getDate)
        print(getPriceId)
        print(getCItyName)

        try:
            data = (getMOvieName, getHallId, getTime, getDate, getPriceId, getCItyName)
            insert_query = '''INSERT INTO SHOWS(MOVIENAME, HALLID, TIME, DATE, PRICEID, CityName) 
                                    VALUES (?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Show added successfully")
            return redirect("/viewallshows")

        except Exception as e:
            print(e)
    return render_template("showsDashboard.html")


@app.route("/viewallshows")
def viewallshows():
    cur = conn.cursor()
    cur.execute("SELECT * FROM SHOWS")
    res = cur.fetchall()
    return render_template("viewallshows.html", cinemass=res)

if(__name__) == "__main__":
    app.run(debug=True)