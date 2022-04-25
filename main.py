import flask
from flask import Flask, request, render_template, redirect, session, url_for
import sqlite3
from flask_session import Session
from instamojo_wrapper import Instamojo
API_KEY = "test_79ae585bb2ff567c3f593b7cb1c"

AUTH_TOKEN = "test_99fbc09589ba9a5dbfa3b451ed5"

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')

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

halls_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='HALL'").fetchall()
Book_tickets_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOKED_TICKETS'").fetchall()

if halls_table:
    print("Table Already Exists ! ")

else:
    conn.execute(''' CREATE TABLE HALL(
                            HALLID INTEGER PRIMARY KEY AUTOINCREMENT,
                            SHOWID FOREIGN KEY REFERENCES SHOW(SHOWID),
                            movieName TEXT,
                            Class TEXT,
                            No_of_seats INTEGER); ''')
    print("Table has created")


if Book_tickets_table:
    print("Table Already Exists ! ")

else:
    conn.execute(''' CREATE TABLE BOOKED_TICKETS(
                            TICKET_NO INTEGER PRIMARY KEY AUTOINCREMENT,
                            SHOWID INTEGER,
                            SEAT_NO INTEGER); ''')
    print("Table has created")

user_table = conn.execute("SELECT name from sqlite_master WHERE type='table' AND name='users'").fetchall()

if user_table:
    print("Table Already Exists ! ")
else:
    conn.execute(''' CREATE TABLE users(
                            ID INTEGER PRIMARY KEY AUTOINCREMENT,
                            mname TEXT, 
                            maddress TEXT, 
                            mphone INTEGER,
                            memail TEXT, 
                            musername TEXT, 
                            mpassword TEXT); ''')
    print("User Table has created")

############################################################################################################################################

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
            return redirect("/view")

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
            return redirect("/viewallmovies")

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


@app.route("/showsDashboard", methods=["GET", "POST"])
def arrangeShow():
    if request.method == "POST":
        getMOvieId = request.form["mid"]
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
            data = (getMOvieId, getMOvieName, getHallId, getTime, getDate, getPriceId, getCItyName)
            insert_query = '''INSERT INTO SHOW(MOVIEID, MOVIENAME, HALLID, TIME, DATE, PRICEID, CityName) 
                                    VALUES (?,?,?,?,?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Show added successfully")
            return redirect("/viewallshows")

        except Exception as e:
            print(e)
    return render_template("showsDashboard.html")


@app.route("/viewallshows")
def viewAllShows():
    cur = conn.cursor()
    cur.execute("SELECT * FROM SHOW")
    res = cur.fetchall()
    return render_template("viewallshows.html", cinemass=res)

###################################################################################################################################################

@app.route("/viewallHalls")
def viewAllHalls():
    cur = conn.cursor()
    cur.execute("SELECT * FROM HALL")
    res = cur.fetchall()
    return render_template("viewallhalls.html", cinemas=res)


@app.route('/ViewSeats', methods=['GET', 'POST'])
def home1():
    if request.method == "POST":
        hallId = request.form["hallId"]
        showId = request.form["showId"]
        return redirect(url_for('getAvailableSeats', hallId=hallId, showId=showId))
    return render_template('ViewSeats.html')


@app.route("/getAvailableSeats", methods=["GET", "POST"])
def seatingManagement():
    if request.method == "POST":
        hallId = request.form["hallId"]
        showId = request.form["showId"]
        print("showId : ", showId)
        print("hallId: ", hallId)
        cur = conn.cursor()
        cur.execute("SELECT * FROM HALL WHERE HALLID = ? AND SHOWID = ?", (hallId, showId))
        res = cur.fetchall()
        cur.execute("SELECT * FROM HALL")
        halls = cur.fetchall()
        print(res)
        print("***")
        # data = (hall_class,showId)
        # q =  "SELECT * FROM HALL"
        # cur.execute(q,data)
        # res = cur.fetchall()
        # print("* res **: ", res )

        totalGold = 0
        totalStandard = 0

        print("* res *", res)
        for i in res:
            print("** ele ***: ", i[2])
            if i[2] == 'gold':
                totalGold = i[3]
            if i[2] == 'silver':
                totalStandard = i[3]
        # if request.method == "POST":
        #     hallId = request.form["hallId"]
        #     showId = request.form["showId"]
        #     print(hallId)
        #     print(showId)
        #     return redirect("/getAvailableSeats?hallId=hallId&showId=showId")
        # return render_template("ViewSeats.html")
    return render_template("getAvailableSeats.html", goldSeats=totalGold, standardSeats=totalStandard)


@app.route("/showsHalls", methods=["GET", "POST"])
def arrangeHalls():
    if request.method == "POST":
        # getMovieName = request.form["movieName"]
        getMShowId = request.form["sid"]
        getClass = request.form["class"]
        getNoOfSeats= request.form["nos"]


        print(getMShowId)
        # print(getMovieName)
        print(getClass)
        print(getNoOfSeats)


        try:
            data = (getMShowId, getClass, getNoOfSeats)
            insert_query = '''INSERT INTO HALL( SHOWID, Class, No_of_seats) 
                                    VALUES (?,?,?)'''

            cursor.execute(insert_query, data)
            conn.commit()
            print("Hall added successfully")
            return redirect("/viewallHalls")

        except Exception as e:
            print(e)
    return render_template("showsHalls.html")

@app.route("/deleteHalls", methods =['GET','POST'])
def deleteHalls():
        if request.method == "POST":
            getHALLID = request.form["HALLID"]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM HALL WHERE HALLID = '" + getHALLID + "' ")
            conn.commit()
            return redirect("/viewallHalls")
        return render_template("deleteHalls.html")

@app.route("/deleteMovies", methods =['GET','POST'])
def deleteMovies():
        if request.method == "POST":
            getMOVIEID = request.form["MOVIEID"]
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PICTURE WHERE MOVIEID = '" + getMOVIEID + "' ")
            conn.commit()
            return redirect("/viewallmovies")
        return render_template("deleteMovies.html")


# @app.route("/getAvailableSeats", methods=["GET"])
# def seatingManagementA():
#     if request.method == "GET":
#         hallId = request.args.get('hallId')
#         showId = request.args.get('showId')
#         print("showId : ", showId)
#         print("hallId: ", hallId)
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM HALL WHERE HALLID = ? AND SHOWID = ?", (hallId, showId))
#         res = cur.fetchall()
#         cur.execute("SELECT * FROM HALL")
#         halls = cur.fetchall()
#         print(res)
#         print("*****")
#         # data = (hall_class,showId)
#         # q =  "SELECT * FROM HALL"
#         # cur.execute(q,data)
#         # res = cur.fetchall()
#         # print("*** res **: ", res )
#
#         totalGold = 0
#         totalStandard = 0
#
#         print("*** res ***", res)
#         for i in res:
#             print("***** ele ****: ", i[2])
#             if i[2] == 'gold':
#                 totalGold = i[3]
#             if i[2] == 'silver':
#                 totalStandard = i[3]
#
#         # cur.execute("SELECT SEAT_NO FROM BOOKED_TICKETS WHERE SHOWID = " + getshowID)
#
#         # goldSeats = []
#         # standardSeats = []
#         #
#         # for i in range(1, totalGold + 1):
#         #     goldSeats.append([i, ''])
#         #
#         #     for i in range(1, totalStandard + 1):
#         #         standardSeats.append([i, ''])
#         #
#         #     for i in res:
#         #         if i[0] > 1000:
#         #             goldSeats[i[0] % 1000 - 1][1] = 'disabled'
#         #         else:
#         #             standardSeats[i[0] - 1][1] = 'disabled'
#         return render_template("seating.html", goldSeats=totalGold, standardSeats=totalStandard)


@app.route("/seats", methods=["GET", "POST"])
def seats():
    return render_template("seating.html")


@app.route("/insertBooking", methods=["GET","POST"])
def createBooking():
    print(request.method)
    if request.method == "POST":
        hallID = request.form['hallID']
        showID = request.form['showID']
        noOfSeats = request.form['noOfSeats']
        seatClass = request.form['seatClass']

        print(hallID)
        print(showID)
        print(noOfSeats)
        print(seatClass)

        cur = conn.cursor()
        cur.execute("SELECT No_of_seats FROM HALL WHERE HALLID = ? AND SHOWID = ? AND Class = ?", (hallID, showID, seatClass))
        res = cur.fetchall()
        seats = res[0]
        print("* res * : ", res)
        remaining_seats = seats[0] - int(noOfSeats)

        cur = conn.cursor()
        cur.execute("UPDATE HALL SET No_of_seats = ?  WHERE  HALLID = ? AND SHOWID = ? AND Class = ? ;",(remaining_seats,hallID, showID, seatClass))
        conn.commit()
        return redirect("/pay")


    return render_template("insertBooking.html")


################################################################################################################################################

@app.route("/userdashboard", methods=['GET', 'POST'])
def userdashboard():
    return render_template("userdashboard.html")


@app.route("/userEntry", methods=["GET", "POST"])
def userEntry():
    if request.method == "POST":
        getName = request.form["mname"]
        getAddress = request.form["maddress"]
        getPhone = request.form["mphone"]
        getEmail = request.form["memail"]
        getUsername = request.form["musername"]
        getPassword = request.form["mpassword"]

        print(getName)
        print(getAddress)
        print(getPhone)
        print(getEmail)
        print(getUsername)
        print(getPassword)

        try:
            conn.execute("INSERT INTO users(mname, maddress, mphone, memail, musername, mpassword )VALUES('"+getName+"','"+getAddress+"','"+getPhone+"','"+getEmail+"','"+getUsername+"','"+getPassword+"')")
            print("Successfully inserted")
            conn.commit()
            return redirect("/userdashboard")

        except Exception as e:
            print(e)
    return render_template("userEntry.html")


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == "POST":
        getUsername = request.form["musername"]
        getPassword = request.form["mpassword"]
        print(getUsername)
        print(getPassword)
        cur2 = conn.cursor()
        cur2.execute( "SELECT * FROM users WHERE musername = '" + getUsername + "' AND mpassword = '" + getPassword + "'")
        res2 = cur2.fetchall()
        if len(res2) > 0:
            for i in res2:
                getName = i[1]
                getid = i[0]

            session["name"] = getName
            session["id"] = getid

            return redirect("/userdashboard")
    return render_template("userlogin.html")


@app.route("/moviesearch", methods=["GET", "POST"])
def moviesearch():
    if request.method == "POST":
        getName = request.form["MOVIENAME"]
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PICTURE WHERE MOVIENAME = '"+getName+"' ")
        result = cursor.fetchall()
        return render_template("moviesearch.html", movies=result)
    return render_template("msearch.html")


@app.route("/insertBooking", methods=["GET","POST"])
def createBookingUser():
    print(request.method)
    if request.method == "POST":
        hallID = request.form.get('hallID')
        showID = request.form['showID']
        noOfSeats = request.form['noOfSeats']
        seatClass = request.form['seatClass']

        print(hallID)
        print(showID)
        print(noOfSeats)
        print(seatClass)

        cur = conn.cursor()
        cur.execute("SELECT No_of_seats FROM HALL WHERE HALLID = ? AND SHOWID = ? AND Class = ?", (hallID, showID, seatClass))
        res = cur.fetchall()
        print("** res **: ", res)
        seats = res[0]
        remaining_seats = seats[0] - int(noOfSeats)

        cur = conn.cursor()
        cur.execute("UPDATE HALL SET No_of_seats = ?  WHERE  HALLID = ? AND SHOWID = ? AND Class = ? ;",(remaining_seats,hallID, showID, seatClass))
        conn.commit()
        return redirect("payment.html")
    return render_template("insertBooking.html")


@app.route('/pay')
def homePay():
    return render_template('payment.html')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/pay', methods=['POST', 'GET'])
def pay():
    if request.method == 'POST':
        name = request.form.get('name')
        seatClass = request.form.get('seatClass')
        email = request.form.get('email')
        amount = request.form.get('amount')


        response = api.payment_request_create(
            amount=amount,
            purpose=seatClass,
            buyer_name=name,
            send_email=True,
            email=email,
            redirect_url="http://localhost:5000/success"
        )

        return redirect(response['payment_request']['longurl'])

    else:

        return redirect('/')


if(__name__) == "__main__":
    app.run(debug=True)