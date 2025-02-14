# MCS 275 Spring 2022

# I am the author of the code provided unless stated otherwise by comment citations and the readme, and I abide by the rules defined in the course syllabus.
"""Application creates a web page that allows a user to upload images to the application. The user can then save the images
to a database in the application. When the user visits the Gallery web page the contents of the database as read by the application on the
index page is displayed as thumbnails in a modular grid depending on the aspect ratio of the uploaded images."""
import os
import sqlite3
from flask import Flask, request, render_template, send_from_directory

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


class Image(object):
    """A class that defines functions for generating a database of images from a folder within the working directory"""

    def __init__(self):
        "Defines a list for the names of image files"
        self.image_name = []

    def load_directory(self):
        """Appends the path of all the files in the working directory to a list and returns it when called"""
        for x in os.listdir():
            self.image_name.append(x)

        return self.image_name

    def create_database(self, name, image):
        """Creates a database with tables for the filename in text and the binary data (BLOB) of any images in the database"""

        conn = sqlite3.connect("Image.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS images 
        (name TEXT,image BLOB)""")

        cursor.execute(""" INSERT INTO images 
        (name, image) VALUES (?,?)""",(name,image))

        conn.commit()
        cursor.close()
        conn.close()

def generate():
    """Defines a function that creates a database using the image class.
    Appends all images in the defined directory to the database"""
    obj = Image()
    print(os.getcwd())
    os.chdir(".\\images")
    for x in obj.load_directory():
        if ".png" in x:
            with open(x,"rb") as f:
                data = f.read()
                obj.create_database(name=x, image=data)
                print("{} added to db ".format(x))

        elif ".jpg" in x:
            with open(x,"rb") as f:
                data = f.read()
                obj.create_database(name=x,image=data)
                print("{} added to db".format(x))
    os.chdir("..")

def fetch_data():
    """Defines a function that reads the database file from the Images folder and writes all of the images from that database to
    a seperate Output folder based on their location in the database table.
    Creates a output folder if it does not yet exist."""
    print(os.getcwd())
    counter = 1
    os.chdir(".\\images")
    conn = sqlite3.connect("Image.db")
    cursor = conn.cursor()
    os.chdir("..")
    if not os.path.exists(".\\output"):
        os.makedirs(".\\output")
    os.chdir(".\\output")
    data = cursor.execute("""SELECT * FROM images""")
    for x in data.fetchall():
        print(x[1])
        with open("{}.png".format(counter),"wb") as f:
            f.write(x[1])
            counter= counter + 1

    conn.commit()
    cursor.close()
    conn.close()
    os.chdir("..")

def clear():
    """Clears the images folder of any images"""
    Folder=[]
    os.chdir(".\\images")
    for x in os.listdir():
        if ".png" in x:
            Folder.append(x)
        elif ".jpg" in x:
            Folder.append(x)
    for x in Folder:
        os.remove(x)
    os.chdir("..")

    

#Web server application routes
#The templates for these routes are adapted from
#https://github.com/ibrahimokdadov/upload_file_python

@app.route("/")
def index():
    """Generates the main page for the hosted site, here the Upload page template is used to allow the user to upload their images,
    the index page also loads all of the images from the database to the output folder in order to update the gallery."""
    fetch_data()
    return render_template("upload.html")

@app.route("/upload", methods=["POST"])
def upload():
    #This upload function and upload button HTML is adapted from
    #https://github.com/ibrahimokdadov/upload_file_python
    """Defines the method for which the upload page handles uploaded images inputted by the user.
    Saves a copy of the file to the local path of the application.
    Creates a folder to store images if one does not exist."""
    target = os.path.join(APP_ROOT, 'images/')
    if not os.path.isdir(target):
            os.mkdir(target)
    else:
        print("Couldn't create upload directory: {}".format(target))
    for upload in request.files.getlist("file"):
        filename = upload.filename
        destination = "/".join([target, filename])
        upload.save(destination)

    # return send_from_directory("images", filename, as_attachment=True)
    return render_template("complete.html", image_name=filename)

@app.route('/upload/<filename>')
def send_image(filename):
    "Defines a page that allows one to view an uploaded image directly if the image exists in the application directory"
    return send_from_directory("output", filename)

@app.route("/save")
def save():
    "Defines a page that indicates that the uploaded files have been saved to the database"
    generate()
    clear()
    return render_template("save.html")

@app.route('/gallery')
def get_gallery():
    """Defines a page that loads the gallery template, as well as creating a variable with a list of the directories of all images that
    the gallery needs to display"""
    clear()
    image_names = os.listdir('./output')
    return render_template("gallery.html", image_names=image_names)

#Start the application
if __name__ == "__main__":
    app.run(port=5000, debug=True)