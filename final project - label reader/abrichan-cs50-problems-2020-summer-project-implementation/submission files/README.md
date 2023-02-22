# LOGOS DOCUMENTATION

## Introduction

This is a webapp that allows users to upload a picture of an ingredient list and check to see
if that ingredient list contains any concerns. These concerns can be anything that the
user decides to add.

## How to use

In order to run the program, you must be in directory ~/project/logos
In this directory, install the following (with the commands listed after the colon)

tesseract : sudo apt install tesseract-ocr
            sudo apt install libtesseract-dev

pytesseract : pip install pytesseract

regex : pip install regex

Once these have been installed, run the website using the command 'flask run' in the ~/project/logos directory.
Click the link that is provided in order to see the working webiste.

Then, you will be taken to a login page.


If you would like to create a new user, click the "Register" button
on the top right corner of the website. This will take you to a page where you can register a new user.

If you already have an account, go ahead and login with your username and password. I have registered a test account
which can be logged into by using the username "bees" and the password "bees!".

You will then be taken to a main page which will display all of your current 'concerns'.

There are five buttons that will take you to different portions of the website.

### Scan

Scan allows the user to upload a picture of their choice to be sent to an ocr function.

(In this prototype, the user can upload a picture and press "check for concerns", but the image that is
processed by the program is hard coded, because of limitations within the IDE.)

### Edit Concerns

Edit Concerns allows the user to add and delete concerns as need be. In order to delete a concern, click
into the drop down menu and select the concern that you would like to be deleted. Then, click update.
If you would like to add a concern, type it into the text box. Then click update. You can also delete a
concern and add one at the same time.

### Change Password

Change Password allows the user to change their password. To do this, enter in your current password,
a new password, and a confirmation of the new password.

### Logout

Pressing the Logout button will log the current user out, and allow for a new user to login, or
a new user to register.

### The Logo

Pressing the logo will take the user back to the home page of the website that displays
the user's current concerns.

NOTE FOR MOBILE USERS: the register, logout, scan, edit concerns and change passwords button will be instead
accesible by clicking the menu button with three horizontal lines at the top right hand corner of the website.

## user bees

Because I needed to hardcode an image into the ocr function, I created a user 'bees'. This user contains the concerns
wheat, peanut, cocoa, and soybeen.

When the scan function is used, the concerns that match will be wheat, cocoa and soybeen.
Both wheat and cocoa are directly inside of the ingredient list. Soybeen is an intentional
misspelling, to show that the function will still match an ingredient if it is slightly different.
If you would like to see the picture that was used, go into folder zpics . Below is the text
that the ocr function returns for that picture.

INGREDIENTS: SUGAR, ENRICHED BLEACHED FLOUR (WHEAT

FLOUR, NIACIN, REDUCED IRON, THIAMIN MONONITRATE,
RIBOFLAVIN, FOLIC ACID), SEMI-SWEET CHOCOLATE CHIPS
(SUGAR, CHOCOLATE LIQUOR, COCOA BUTTER, SOY LECITHIN

[EMULSIFIER], VANILLA), COCOA (PROCESSED WITH ALKAL)),
CANOLA OR SOYBEAN OIL, BITTERSWEET CHOCOLATE CHIPS

(CHOCOLATE LIQUOR, SUGAR, COCOA BUTTER, MILK FAT,
SOY LECITHIN [EMULSIFIER], VANILLA), MILK CHOCOLATE

CHIPS (SUGAR, WHOLE MILK POWDER, CHOCOLATE LIQUOR,
COCOA BUTTER, SOY LECITHIN [EMULSIFIER], VANILLA), SALT,
