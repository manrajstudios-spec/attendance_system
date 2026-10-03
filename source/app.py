import cv2
import base64
import numpy as np
from fastapi import FastAPI
from admin_auth import compare_pass
from call_modle import recognize_faces
from fastapi.middleware.cors import CORSMiddleware
from main import add_new_batch,delete_a_batch,enroll_a_student,remove_a_student,table_exists,list_all_batches,conduct_attendance,list_all_students

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

auth_done = False
selected_batch = ""

@app.get("/reset_auth")
def reset_auth():
    global auth_done,selected_batch
    
    auth_done = False
    selected_batch = ""
    
    return {"success":True}

@app.post("/verify_password")
def varify_password(password_holder:dict):
    global auth_done
    admin_password = password_holder["admin_password"]
    
    result = compare_pass(admin_password)
    
    auth_done = result
    
    print(f"Password Was {"correct" if result else  "InCorrect"}")
    return {"success":result}
    
@app.get("/check_auth")
def check_auth():
    print(f"Auth Status: {"Authenticated" if auth_done else "Un Authenticated"}")
    
    return {"auth_status":auth_done}

@app.post("/add_new_batch")
def add_batch(batch_data:dict):
    batch_name = batch_data["batch_name"]
    
    batch_result = add_new_batch(batch_name)
    
    print(f"Batch Result: {batch_result}")

    return {"success":batch_result}

@app.get("/list_batches")
def return_batches():
    all_batches = list_all_batches()
    
    print(f"All Batches: {all_batches}")
    return {"all_batches":all_batches}

@app.post("/remove_batch")
def remove_batches(batch_name_object:dict):
    result = delete_a_batch(batch_name_object["batch_name"])
    
    print(f"Batch With The Name: {batch_name_object["batch_name"]} Was {"Successfully Removed" if result else "Wasnt Removed"}")
    
    return {"success":result}

@app.post("/enroll_student")
def add_student(student_data:dict):
    student_name = student_data["student_name"]
    student_age = student_data["student_age"]
    selected_program = student_data["selected_batch"]
    
    base64_pic = student_data["student_picture"]
    
    image_bytes = base64.b64decode(base64_pic.split(",")[1])

    image_in_bytes = np.frombuffer(image_bytes,np.uint8)
    
    cv_im = cv2.imdecode(image_in_bytes,cv2.IMREAD_COLOR)
    
    face_emebdding = recognize_faces(cv_im)
    
    if isinstance(face_emebdding,str):
        return {"output_reply": face_emebdding}
    
    result = enroll_a_student(selected_program,student_name,student_age,face_emebdding)
    
    return {"output_reply":result}
    
@app.post("/remove_student")
def remove_student(student_data:dict):
    student_id = student_data["student_id"]
    selected_batch = student_data["selected_batch"]
    
    print(f"Batch: {selected_batch} IDD: {student_id}")
    
    print(type(student_id))
    result = remove_a_student(selected_batch=selected_batch,idd=int(student_id))

    print(f"Removing Status: {result}")

    return {"success":result}

@app.post("/attend_class")
def attend_class(student_data:dict):
    selected_batch = student_data["selected_batch"]
    base64_image = student_data["student_picture"]
    
    image_bytes = base64.b64decode(base64_image.split(",")[1])
    image_in_bytes = np.frombuffer(image_bytes,np.uint8)
    cv_im = cv2.imdecode(image_in_bytes,cv2.IMREAD_COLOR)

    face_emebdding = recognize_faces(cv_im)

    if isinstance(face_emebdding,str):
        return {"result":face_emebdding}

    result = conduct_attendance(selected_batch,face_emebdding)

    return {"result":result}
    
@app.post("/list_students")
def list_students(batch_data:dict):
    selected_batch = batch_data["selected_batch"]
    
    print(f"Batch: {selected_batch}")
    students = list_all_students(selected_batch=selected_batch)

    print(f"ALL STUDENTS: {students}")

    return {"students":students}
    