# Image Gallery Webpage Generator

MCS 275 Spring 2022 Project

## Assignment

The goal of this project is to build a web application that when given a series of images, will generate
a web page or a series web pages that displays thumbnails of all of these images in a gallery format. 
The web pages should allow the user to click and save on the images thumbnail to aquire the full image being displayed. 

## How to test

(This program uses the templates functions of flask and requires a folder to place the html files in,
because gradescope does not allow me to upload folders, I have provided a zip file that has the application
set up with folders, a database, and the html templates necessary for the program to function properly.)

After running gallery.py, a web page is hosted locally at port :5000, all of the functions of the
application can be accessed by going to the index of this web page.

In order to display images on the page generated, the program uploads images from a 'images' folder where a database is present.
When the web page is loaded, the user is prompted to upload images, upload the images you wish to see in the gallery and they will be added
to the image folder. In order to save these images to the database, the user must update the gallery with the uploaded images.
Clicking on the update gallery link will save all images in the images folder to the database within that folder.
Accessing the index will fetch all of the images from the database and place them in a folder readable by the gallery web page.
After there are images in the database, going to the /gallery page will display the images in a gallery format as thumbnails.
Because the images in the image folder are temporary, loading the gallery will clear the image folder of all images.
(Note that if a database already exists, any uploaded images will be displayed in addition to the images in the database already.)

## Personal contribution

My contributions to this project include adapting the source of the image uploading code to function using a SQL database to store file paths, 
This includes writing a class that defines the structure of the database, functions to read and write from this database, and the logic to determine
when the database should be accessed.
Making HTML additional templates to produce pages to display uploaded images on. 

## Sources and credits

Tutorial for constructing an SQLite database for the purposes of storing files uploaded by a user to a webpage:
https://www.twilio.com/blog/intro-multimedia-file-upload-python-sqlite3-database

Sample code for using flask and python to upload files to HTML templates and host the resulting page on a server:
https://github.com/ibrahimokdadov/upload_file_python

SQLlite python interface documentation:
https://www.tutorialspoint.com/sqlite/sqlite_python.htm

