from fastapi import FastAPI, Depends
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from typing import Union
from pydantic import BaseModel
import pprint
from models import Inventory, User
from mongoengine import connect
import json
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

USERPROFILE_DOC_TYPE = "userprofile"

def con():
    uri = "mongodb://localhost:27017"
    # Set the Stable API version when creating a new client
    client = MongoClient(uri, server_api=ServerApi('1'))
                            
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        # db = client.admin
        # col = db.inventory
        # item = {"item" : "cotton", "color" : "white"}
        # item_id = col.insert_one(item).inserted_id
        return client.admin

    except Exception as e:
        print(e)
        return "error"
    
# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None

# class UserInDB(User):
#     type: str = USERPROFILE_DOC_TYPE
#     hashed_password: str

app = FastAPI()
connect(db="inventory_db", host="localhost", port=27017)





# @app.get("/users/{username}", response_model=User)
# def read_user(username: str):
#     collect = con().inventory
#     user = collect.find_one({"item": "canvas"})
#     pprint.pprint(user)

@app.get("/all")
def get_all():
    inv = Inventory.objects().to_json()
    return {"inventory": json.loads(inv)}

class NewUser(BaseModel):
    username: str
    password: str
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

@app.post("/log_up")
def sign_up(new_user: NewUser):
    user = User(username=new_user.username,
                password=get_password_hash(new_user.password))
    user.save()
    return {"message": "you've logged up"}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password


@app.get("/")
def home(token: str = Depends(oauth2_scheme)):
    return {"message": "Hello World"}



