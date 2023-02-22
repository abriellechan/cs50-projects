from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

import regex as re

from helpers import apology, login_required, ocr, concernlist

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///logos.db")

@app.route("/")
@login_required
def index():

    # displays a table of user's concerns

    if request.method == "GET":

        concerns = concernlist() # calls function which creates a list and fills it with concerns
        username = db.execute("SELECT username FROM users WHERE user_id=:user_id", user_id=session["user_id"])[0]["username"]
        return render_template("index.html", concerns=concerns, username=username) # passes variables to html page


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)


        # Remember which user has logged in
        session["user_id"] = rows[0]["user_id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get("username")

        if not username or not request.form.get("password") or not request.form.get("confirmation"):
            return apology("Username, Password and Confirm pls!")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username=username)
        if rows:
            return apology("Username already exists")


        if request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and Confirmation must match")


        db.execute("INSERT INTO users (username, hash) VALUES (:username, :pswdhash)", username=username, pswdhash=generate_password_hash(request.form.get("password")))
        return redirect("/login")


@app.route("/changepassword", methods=["GET", "POST"])
@login_required
def changepassword():
    """Change Password for current logged in user"""
    if request.method == "GET":

        return render_template("changepassword.html")

    else:

        if not request.form.get("password") or not request.form.get("newpassword") or not request.form.get("confirmation"):
            return apology("Current Password, New Password and Confirmation pls!")

        rows = db.execute("SELECT * FROM users WHERE user_id = :user_id",user_id=session["user_id"])

        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid current password", 403)


        if request.form.get("newpassword") != request.form.get("confirmation"):
            return apology("new password and confirmation must match!")


        db.execute("UPDATE users SET hash = :pswdhash", pswdhash=generate_password_hash(request.form.get("newpassword")))
        print("BEFORE REDIRECT")
        return redirect("/login")


@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():

    # allows user to add and delete concerns

    concerns = concernlist() # list of users concerns
    num_concerns = len(concerns) # how many concerns the user has

    if request.method == "GET":

        return render_template("edit.html", concerns=concerns, num_concerns=num_concerns)

    # if POST

    delete = request.form.get("del_concerns") # the concern the user wants to delete
    add = request.form.get("add") # the concern the user wants to add

    # check if user did not add or delete anything
    if not delete and not add:
        return apology("no values to add or delete!")

    # if user added a concern that already exists
    if add in concerns:
        return apology("concern already exists!")

    # concerns are good to add or delete
    else:
        if delete: # deletes from table
            db.execute("DELETE FROM concerns WHERE concern=:concern AND user_id=:user_id", concern=delete, user_id=session["user_id"])

        if add: # adds to table
            db.execute("INSERT INTO concerns VALUES (:user_id, :add)", user_id=session["user_id"], add=add)

    concerns=concernlist() # updates new concernlist to concern variable
    num_concerns = len(concerns) # updates number of concerns

    return render_template("edit.html", concerns=concerns, num_concerns=num_concerns)


@app.route("/scan", methods=["GET", "POST"])
@login_required


def scan():
    # on desktop, allows user to select an image from their computer to upload. On phone, allows user to upload or take a photo.
    # passes the image file to ocr function, which extracts text from it and returns the text as a string
    # compares concerns to the text, notifying the user if one of their concerns is present in the text by displaying display.html

    if request.method == "GET":
        return render_template("scan.html")

    """

    Saving local files does not work on ide

    if not request.files.get("picture"):
        return apology("must provide picture")

    if not image:
        #return apology("must provide picture")

    text = ocr(request.files.get("picture"))

    """

    text = ocr("zpics/test.jpg") # sends picture to ocr function, hardcoded since above code does not work in ide
 
    concerns = concernlist()
    matches= []

    # checks if concerns are similar to any words in the text using regex
    for i in concerns:
        for j in re.finditer("(?fie)(?:%s){e<=1}" % re.escape(i), text): # (fuzzy logic) close matches instead of exact matches
            matches.append(i)

    matches = set(matches) # removes duplicate matches

    return render_template("display.html", matches=matches)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
