import requests

import pytesseract as tess
from cs50 import SQL
from PIL import Image, ImageEnhance, ImageFilter


from flask import redirect, render_template, request, session
from functools import wraps

db = SQL("sqlite:///logos.db")

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def ocr(image):
    # enhances image so text is easier to read, and then passes image to pytesseract to extract text
    img = Image.open(image)
    # preproccessing image for pytesseract
    enhancer = ImageEnhance.Contrast(img)
    cont = enhancer.enhance(2)
    sharp = cont.filter(ImageFilter.SHARPEN)
    text = tess.image_to_string(sharp, lang='eng') # passes to pytesseract
    return text

def concernlist():

    # inserts concerns from query into a list

    concerns = (db.execute("SELECT concern FROM concerns WHERE user_id=:user_id", user_id=session["user_id"]))
    concern_list = []

    for i in range(len(concerns)):

        concern_list.append(concerns[i]["concern"])

    return concern_list