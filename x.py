import pathlib
from bottle import request, response, template
import re
import sqlite3
import smtplib
import time
import hashlib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date
import json
import requests
from PIL import Image
import os


ITEMS_PER_PAGE = 5
COOKIE_SECRET = "41ebeca46f3b-4d77-a8e2-554659075C6319a2fbfb-9a2D-4fb6-Afcad32abb26a5e0"
COOKIE_NAME = "user"
COOKIE_BOOKING_NAME = "booking"

##############################
def dict_factory(cursor, row):
    col_names = [col[0] for col in cursor.description]
    return {key: value for key, value in zip(col_names, row)}

##############################
def arango(query, type = "cursor"):
    try:
        url = f"http://arangodb:8529/_api/{type}"
        res = requests.post( url, json = query )        
        return res.json()
    except Exception as ex:
        print("#"*50)
        print(ex)
    finally:
        pass

##############################

def db():
    db = sqlite3.connect(str(pathlib.Path(__file__).parent.resolve())+"/company.db")  
    db.row_factory = dict_factory
    return db

##############################
def no_cache():
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", 0)    


##############################
def validate_user_logged():
    user = request.get_cookie("user", secret=COOKIE_SECRET)
    if user is None: raise Exception("User must be logged in", 400)
    return user


##############################

def validate_logged():
    # Prevent logged pages from caching
    response.add_header("Cache-Control", "no-cache, no-store, must-revalidate")
    response.add_header("Pragma", "no-cache")
    response.add_header("Expires", "0")  
    user_id = request.get_cookie("id", secret = COOKIE_SECRET)
    if not user_id: raise Exception("***** user not logged *****", 400)
    return user_id


##############################

NAME_MIN = 2
NAME_MAX = 20
NAME_REGEX = r"^[a-zA-Z_ ]{2,20}$"

def validate_name():
    
    name = request.forms.get("name", "").strip()
    print(name)
    if not re.match(NAME_REGEX, name): return False
    return name

##############################

EMAIL_REGEX = r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$"

def validate_email():
    error = f"email invalid"
    email = request.forms.get("email", "").strip()
    if not re.match(EMAIL_REGEX, email): return False
    return email

##############################

PHONE_REGEX = r"^(?:(?:\+45)?[\s-]?)?(?:[2-9]{1}\d{1})[\s-]?\d{2}[\s-]?\d{2}[\s-]?\d{2}$"

def validate_phone():
    error = f"Angiv et gyldigt telefon nummer."
    phone = request.forms.get("phone", "")
    print(phone)
    if not re.match(PHONE_REGEX, phone): return False
    return phone

##############################

POST_NO_REGEX = r"^(?:[1-9]\d{3})$"

def validate_post_no():
    error = f"Angiv et gyldigt post nr."
    postno = request.forms.get("postno", "").strip()    
    if not re.match(POST_NO_REGEX, postno): return False
    return postno

##############################

CITY_REGEX = r"^[a-zA-ZæøåÆØÅ\s-]+$"

def validate_city():
    error = f"Angiv et gyldigt by."
    city = request.forms.get("city", "").strip()
    print(city)
    if not re.match(CITY_REGEX, city): return False
    return city

##############################

def validate_message():

    message = request.forms.get("message", "")

    if len(message) > 500: return False
    
    return message

##############################

def validate_question():

    answer = request.forms.get("question", "")
    answer = int(answer)
    if answer != 5: return False
    
    return answer

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"    
    user_password = request.forms.get("user_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_password): raise Exception(error, 400)
    return user_password

##############################

USER_PASSWORD_MIN = 6
USER_PASSWORD_MAX = 50
USER_PASSWORD_REGEX = "^.{6,50}$"

def validate_old_password():
    error = f"password {USER_PASSWORD_MIN} to {USER_PASSWORD_MAX} characters"    
    user_old_password = request.forms.get("user_old_password", "").strip()
    if not re.match(USER_PASSWORD_REGEX, user_old_password): raise Exception(error, 400)
    return user_old_password

##############################

def get_thumbnails():
    
    THUMBNAILS_DIR = './images/small'

    files = os.listdir(THUMBNAILS_DIR)

    images = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', 'webp'))]

    if len(images) == 0: raise Exception("No image found", 400)        

    return images

##############################

def upload():  
    try:

        # Define the directories to store resized images
        BASE_UPLOAD_DIR = './images'
        SMALL_DIR = os.path.join(BASE_UPLOAD_DIR, 'small')
        MEDIUM_DIR = os.path.join(BASE_UPLOAD_DIR, 'medium')
        LARGE_DIR = os.path.join(BASE_UPLOAD_DIR, 'large')
        SUPER_LARGE_DIR = os.path.join(BASE_UPLOAD_DIR, 'super_large')

        # Get the uploaded image file
        my_img = request.files.get('image')

        if not my_img:
            return "No file uploaded!"

        # Ensure directories for small, medium, large, and super large images exist
        os.makedirs(SMALL_DIR, exist_ok=True)
        os.makedirs(MEDIUM_DIR, exist_ok=True)
        os.makedirs(LARGE_DIR, exist_ok=True)
        os.makedirs(SUPER_LARGE_DIR, exist_ok=True)

        # Open the uploaded image directly from the file-like object (without saving original)
        img = Image.open(my_img.file)

        # Resize and save for small images (320px wide)
        small_img = img.copy()
        small_img.thumbnail((320, int(img.height * (320 / img.width))))
        small_img.save(os.path.join(SMALL_DIR, my_img.filename))

        # Resize and save for medium images (768px wide)
        medium_img = img.copy()
        medium_img.thumbnail((768, int(img.height * (768 / img.width))))
        medium_img.save(os.path.join(MEDIUM_DIR, my_img.filename))

        # Resize and save for large images (1024px wide)
        large_img = img.copy()
        large_img.thumbnail((1024, int(img.height * (1024 / img.width))))
        large_img.save(os.path.join(LARGE_DIR, my_img.filename))

        # Resize and save for super large images (1920px wide for projectors)
        super_large_img = img.copy()
        super_large_img.thumbnail((1920, int(img.height * (1920 / img.width))))
        super_large_img.save(os.path.join(SUPER_LARGE_DIR, my_img.filename))

        
        return True
    
    except Exception as ex:
        print(ex)
        raise Exception(ex, 400)
    finally:
        pass
##############################
NUMBER_IMAGES_MIN = 3

def get_all_images():
    uploads = request.files.getall('property_images')
    if len(uploads) < NUMBER_IMAGES_MIN:
        raise Exception('Please upload minimum 3 images.', 400)
    # Debugging: Print information about each upload
    print(f"Total uploads received: {len(uploads)}")
    for i, upload in enumerate(uploads):
        print(f"Upload {i}: filename={upload.filename}, content_length={len(upload.file.read())}")
        upload.file.seek(0)  # Reset file pointer after reading

    # Filter out any empty file inputs
    uploads = [upload for upload in uploads if upload.filename and len(upload.file.read()) > 0]
    for upload in uploads:
        upload.file.seek(0)  # Reset file pointer for subsequent operations        
    
    return uploads

##############################

def get_delete_images():    
    images = request.forms.getall('delete_images')
    return images

##############################

def confirm_password():
  error = f"password and confirm_password do not match"
  user_password = request.forms.get("user_password", "").strip()
  user_confirm_password = request.forms.get("user_confirm_password", "").strip()
  if user_password != user_confirm_password: raise Exception(error, 400)
  return True

##############################

def send_email(user_name, receiver_email, verification_key, action, title):
    
    # Email configuration
    sender_email = "iffijarral@gmail.com"    
    password = "flolrybuytwclchl"
    subject = "Test Email via Python"
    # message_body = "<h1>Hello, this is a test email sent via Python!</h1>"
    message_body = template('email/email_welcome', user_name = user_name, verification_key = verification_key, action = action, title = title)    
    # Create message container
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Attach message body
    message.attach(MIMEText(message_body, 'html'))
    
    try:
        # Connect to SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)

        # Send email
        server.sendmail(sender_email, receiver_email, message.as_string())

        # Quit SMTP session
        server.quit()
        
        return True
    except Exception as e:
        print("An error occurred:", e)
        return False
    finally:
        pass 

    


############################### ArangoDB actions
# Function to insert a document in a collection
def insert_document(collection, document):
    try:
        query = {
            "query": f"INSERT @doc INTO {collection} RETURN NEW",
            "bindVars": { "doc": document }
        }
        result = arango(query)
        if result and not result.get('error'):
            return result['result'][0]  # Return the inserted document
        raise Exception(f"Document insertion failed: {result.get('errorMessage', 'Unknown error')}")
    except Exception as e:
        print(f"Error while creating document: {e}")
        raise Exception('System is under update', 500)

################################
# Function to create an edge between two documents
def create_edge(edge_collection, from_id, to_id):
    try:
        query = {
            "query": f"INSERT {{ '_from': '{from_id}', '_to': '{to_id}' }} INTO {edge_collection}"
        }
        result = arango(query)
        if result:
            print(f"Edge successfully created between {from_id} and {to_id}.")
            return result
        else:
            print(f"Failed to create edge between {from_id} and {to_id}.")
            raise Exception(f"System is under updation", 400)
    except Exception as e:
        print(f"Error while creating edge: {e}")
        raise Exception('System is under updation', 400)

################################
def add_property_to_doc(collection, doc_key, doc_data):
    print(f"_key: {doc_key}")
    try:
        query = {   "query": "UPDATE @doc_key WITH @doc_data IN properties RETURN NEW",
                "bindVars":{"doc_key":doc_key, "doc_data":doc_data}
             }
        result = arango(query)
        if result and result.get('error') is False:
            print(f"Property {doc_key} successfully updated with new data.")
            return result
        else:
            raise Exception('Property update failed', 400)
    except Exception as e:
        print(f"Error while updating property: {e}")
        raise