from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import logging
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, HTTPException,Request,Form,Depends
from models import UserCreate   
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn


def mydatabase():
    uri = "mongodb+srv://hellotemp83:Switchoff@switchofftest1.ouxfggb.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db=client.test1
    mycollection=db.user
    #mc.insert_one({"username":"new_guy","password":"test@123"})
    #mc.delete_one({"username":"new_guy"})
    cursor=mycollection.find()
    return cursor,mycollection


def delete_one_user(username,password):
    uri = "mongodb+srv://hellotemp83:Switchoff@switchofftest1.ouxfggb.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db=client.test1
    mycollection=db.user
    cursor=mycollection.find()
    for i in cursor:
        if username==i["username"]:     
            if password==i["password"]: 
                mycollection.delete_one({"username":username})
                client.close()
                return {"message":f"username '{username}' deleted successfully"}
            else:
                client.close()
                return {"message":"Incorrect password"}
    client.close()
    return {"message":f"username '{username}' does not exist"}
    
def insert_one_user(username,password):
    uri = "mongodb+srv://hellotemp83:Switchoff@switchofftest1.ouxfggb.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db=client.test1
    mycollection=db.user
    cursor=mycollection.find()
    for i in cursor:
        if username==i["username"]:     
            client.close()
            return {"message":"Username already exists"}
    mycollection.insert_one({"username":username,"password":password})
    client.close()
    return {"message":f"username '{username}' added succesfully"}


def check_userdata(username,password):
    uri = "mongodb+srv://hellotemp83:Switchoff@switchofftest1.ouxfggb.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri, server_api=ServerApi('1'))
    db=client.test1
    mycollection=db.user
    cursor=mycollection.find()
    for i in cursor:
        if username==i["username"]:
            if password==i['password']:     
                client.close()
                return 2
            client.close()
            return 1
    client.close()
    return 0
            

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="html_templates")

users_db = [
    {"username": "john_doe", "password": "secretpassword"},
    {"username": "alice_smith", "password": "password123"},
]


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    content = {"title": "My Secure App", "greeting": "Hello, secure world!", "error_message": ""}
    return templates.TemplateResponse("index.html", {"request": request,"content":content})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    # Logic for validating the username and password can be added here
    print(f"Received login request: username={username}, password={password}")

    # For demonstration purposes, redirect to the "/result" page with a POST request
    content = {"title": "My Secure App", "greeting": "Hello, secure world!", "error_message": ""}

    if username=="test":
        if password=="123":
            return RedirectResponse(url="/result", status_code=307)
        content["error_message"]="Invalid Password"
        return templates.TemplateResponse("index.html", {"request": request, "content": content})
    content["error_message"]="Invalid Username"
    return templates.TemplateResponse("index.html", {"request": request, "content": content})
        

    




@app.route("/result", methods=["GET", "POST"])
async def result(request: Request):
    return await get_login_result(request)

user_database = "user1"

@app.get("/register", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    print(username)
    # Check if the username already exists in the database

    return insert_one_user(username,password)
        

# Define a route to handle the successful registration and redirect to /result
@app.get("/result", response_class=HTMLResponse)
async def show_result(request: Request):
    return templates.TemplateResponse("result.html", {"request": request})


@app.get("/user-database", response_class=HTMLResponse)
async def user_database(request: Request):
    x,y=mydatabase()
    data_from_mongodb=[]
    for i in x:
        data_from_mongodb.append({"username":i['username'],"password":i['password']})
    
    return templates.TemplateResponse("user_database.html", {"request": request, "data_from_mongodb": data_from_mongodb})

@app.get("/update-details", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("update.html", {"request": request})


@app.post("/update-details")
async def update_userdata(request:Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    new_password=data.get("newPassword")
    check=check_userdata(username,password)
    if  check == 2:
        if password==new_password:
            return{"message":"Choose a different password for added security"}
        delete_one_user(username,password)
        insert_one_user(username,new_password)
        return {"message":"Password updated Successfully"}
    elif check==1:
        return {"message":"Incorrect Password"}
    else:
        return{"message":"Username not found"}


@app.get("/delete", response_class=HTMLResponse)
async def get_register(request: Request):
    return templates.TemplateResponse("delete.html", {"request": request})

@app.post("/delete")
async def register(request: Request):
    data = await request.json()
    username = data.get("username")
    password = data.get("password")
    print(username)
    # Check if the username already exists in the database

    return delete_one_user(username,password)
        
async def get_login_result(request: Request = Depends()):
    content = {"title": "Login Result", "result": "Login successful!"}
    return templates.TemplateResponse("login_result.html", {"request": request, "content": content})



if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)