import flask
from flask import Flask, request, render_template, redirect
import sqlite3

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

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
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

if(__name__) == "__main__":
    app.run(debug=True)