import cv2
import base64
import numpy as np
from fastapi import FastAPI
from admin_auth import compare_pass
from call_modle import recognize_faces
from fastapi.middleware.cors import CORSMiddleware
from main import add_new_batch,delete_a_batch,enroll_a_student,remove_a_student,table_exists,list_all_batches

app = FastAPI()

app.add_middleware(middleware_class=CORSMiddleware,allow_credentials=True,allow_methods=["*"],allow_origins=["*"])

auth_done = False

@app.get("/main_menu")
def main_menu():
    global auth_done
    auth_done = False
    
    return {"auth":False}

@app.post("/login")
def login(password:dict):
    global auth_done
    done = compare_pass(password["password"])

    auth_done = done

    return {"sucess":done}

@app.get("/list_batches")
def list_batches():
    all_batches = list_all_batches()
    
    print(all_batches)
    return {"batches_list":all_batches}

@app.post("/remove_batch")
def remove_batch(batch_name:dict):
    exists = table_exists(batch_name["batch_name"])
    
    print(f"Exists: {exists}")

    if exists:
        delete_a_batch(batch_name["batch_name"])
    
    return {"sucess":exists}

@app.get("/check_auth")
def check_auth():
    return {"auth":auth_done}

@app.post("/validate_batch")
def validate_batch(batch_name:dict):
    print(f"Batch Name: {batch_name["batch_name"]}")

    exists = table_exists(batch_name["batch_name"])
    
    if not exists:
        add_new_batch(batch_name["batch_name"]) 

    return {"sucess":exists}

@app.post("/add_new_student")
def add_student(data:dict):
    student_name = data["student_name"]
    student_age = data["student_age"]
    blob = data["picture"]
    
    image_bytes = base64.b64decode(blob.split(",")[1])
        
    cv_image = cv2.imdecode(np.frombuffer(image_bytes,np.uint8),cv2.IMREAD_COLOR)
    
    result = recognize_faces(cv_image)
    
    if isinstance(result,str):
        return {"sucess":False}
    else:
        result = enroll_a_student()
        if not result:
            return {"sucess":False}
        else:
            return {"sucess":True}

    