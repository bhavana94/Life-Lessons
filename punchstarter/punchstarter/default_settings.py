import os
import cloudinary

DEBUG=True

BASE_DIR=os.path.dirname(os.path.abspath(__file__))

SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI","sqlite:///" + BASE_DIR + "/app.db")
CLOUDINARY_CLOUD_NAME = os.environ.get("CLOUDINARY_CLOUD_NAME","djsl7o6ww")
CLOUDINARY_API_KEY = os.environ.get("CLOUDINARY_API_KEY","154632333375734")
CLOUDINARY_API_SECRET = os.environ.get("CLOUDINARY_API_SECRET","UwlZeIUgBQ3f0Eahj1f9Iw-0rlo" )
SQLALCHEMY_TRACK_MODIFICATIONS = "True"


cloudinary.config( 
  cloud_name =CLOUDINARY_CLOUD_NAME , 
  api_key = CLOUDINARY_API_KEY , 
  api_secret = CLOUDINARY_API_SECRET
)
