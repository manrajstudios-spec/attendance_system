import os
import json
import bcrypt
import sqlite3
import numpy as np
from rich import print
from rich.console import Console
from datetime import datetime,date
from record_new_face import capture_face

attendace_database_conn = sqlite3.connect("data/attendance_database.db",check_same_thread=False)
cur = attendace_database_conn.cursor()

attenace_time_range = (9,11)

password_file = "data/admin_pass"
embedding_file_det = "data/embeddings_per_batch/"

console = Console()

def ask_user(to_ask,empty_allowed = False):
    while True:
        user_input = console.input(to_ask)
        
        if empty_allowed:
            return user_input
        
        if user_input:
            return user_input

def list_all_batches():
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")

    return [row[0] for row in cur.fetchall()] # row[0] bcz fetchall returns a tuple so names will be as [(a,),(b,),....,]
        
def admin_login_handler():
    try :
        with open(password_file,'r') as file:
            stored_admin_pass = file.read().strip().encode("utf-8")
    except FileNotFoundError:
        stored_admin_pass = ""
    
    # New Admin Password
    
    if not stored_admin_pass:
        new_admin_pass = ask_user("[bold blue]Create A Strong Password: [/bold blue] ")

        new_admin_pass = bcrypt.hashpw(new_admin_pass.encode("utf-8"),bcrypt.gensalt()).decode()
        
        with open(password_file,'w') as file:
            file.write(new_admin_pass)
        
        return None
                
    # Compare password
    entered_password = ask_user("[bold blue]Enter Your Password: [/bold blue]").encode("utf-8")
    
    if bcrypt.checkpw(entered_password,stored_admin_pass):
        return True
    else:
        return False

def table_exists(name):
    cur.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?",(name,))
    return cur.fetchone() is not None    

def id_exists(table_name,idd):
    cur.execute(f"SELECT 1 FROM '{table_name}' WHERE id=?",(idd,))
    return cur.fetchone() is not None
    
def add_new_batch(selected_batch):    
    if table_exists(selected_batch):
        return False
    else:
        cur.execute(f"CREATE TABLE '{selected_batch}' (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT,age INTEGER,attendance TEXT,joining_date TEXT)")
        attendace_database_conn.commit()

        emebddings_array = np.zeros((50,512))
        np.save(f"{embedding_file_det}{selected_batch}.npy",emebddings_array)

        return True

def delete_a_batch(selected_batch):    
    if table_exists(selected_batch):
        cur.execute(f"DROP TABLE '{selected_batch}'")
        
        attendace_database_conn.commit()
        path = f"{embedding_file_det}{selected_batch}.npy"
        
        if os.path.exists(path):
            os.remove(path=path)
            
        return True
    else:
        print("[bold red]Table Not Found[/bold red]")
        return False
        
def remove_a_student(selected_batch,idd):
    if selected_batch == "q":
        return False
    
    if table_exists(selected_batch):        
        if id_exists(selected_batch,idd) and idd.isdigit():
            cur.execute(f"DELETE FROM '{selected_batch}' WHERE id=?",(idd,))

            attendace_database_conn.commit()
            path = f"{embedding_file_det}{selected_batch}.npy"
            
            embedidngs = np.load(path)
            embedidngs[int(idd)-1] = np.zeros((1,512))    
            np.save(path,embedidngs)

            return True
        else:
            print("[bold red]Student Not Found Invalid Id[/bold red]")
            return "Student Not Found Invalid Id"        
    else:
        print("[bold red]Batch Not Found[/bold red]")
        return "Batch Not Found"
    
def enroll_a_student(selected_batch,name_of_student,age_of_student,new_face_embedding):    
    if table_exists(selected_batch):
        joining_date = date.today()
        joining_date = f"Date: {joining_date.day}\nMonth: {joining_date.month}\nYear: {joining_date.year}"
        
        path = f"{embedding_file_det}{selected_batch}.npy"
        stored_embeddings = np.load(path)

        sims = (stored_embeddings @ new_face_embedding.T).flatten()
        
        maxx = sims.max()
        
        if maxx >= 0.65:
            print("[bold orange]Student With This Face Already Exists: [/bold orange]")
            return "Student With This Face Already Exists"
        
        cur.execute(f"INSERT INTO '{selected_batch}' (name,age,joining_date) VALUES (?,?,?)",(name_of_student,age_of_student,joining_date))
        attendace_database_conn.commit()

        assigned_id = cur.lastrowid
        
        if new_face_embedding.shape[0] < assigned_id-1:
            temp_emebddings = np.zeros((stored_embeddings.shpae[0]* 2 ,512))
            
            temp_emebddings[:stored_embeddings.shape[0]] = stored_embeddings
            stored_embeddings = temp_emebddings
        
        stored_embeddings[assigned_id-1] = new_face_embedding

        np.save(path,stored_embeddings)
        
        return assigned_id
    else:
        print("[bold red]Batch Not Found[/bold red]")
        return "Table Dosent Exists"

def admin_options():
    options = "[bold purple]Press 1 To Add New Batch \nPress 2 To Delete A Batch \nPress 3 To Remove A Student \nPress 4 To Enroll A Student\nPress Q to Quit\n: [/bold purple]"

    while True:
        names = list_all_batches() 
        
        for i,name in enumerate(names):
            print(f"[bold purple]{i}: {name}\n [/bold purple]")

        option_selected = ask_user(options)
                
        if option_selected == '1':
            selected_batch = ask_user("[bold blue]Enter Name Of Batch: [/bold blue]")
            
            out = add_new_batch(selected_batch)

            if not out:
                print("[bold yellow]Batch With This Name Already Exists [/bold yellow]")
            else:
                print("[bold green]Batch Created [/bold green]")

        elif option_selected == '2':
            selected_batch = ask_user("[bold blue]Enter Name Of Batch: [/bold blue]")

            out = delete_a_batch(selected_batch)

            if out:
                print("[bold green]Batch Deleted Successfully[/bold green]")
            else:
                print("[bold red]No Batch Found[/bold red]")

        elif option_selected == '3':
            selected_batch = ask_user("[bold blue]Enter Name Of Batch: [/bold blue]")

            idd = ask_user("[bold lime]Enter Id Of Student You wanna Remove: [bold /lime]")
            out = remove_a_student(selected_batch,idd)
            
            if isinstance(out,str):
                print(f"[bold red]{out} [/bold red]")
                            
            elif isinstance(out,bool):
                print("[bold green]Student Removed [/bold green]")
            

        elif option_selected == '4':
            selected_batch = ask_user("[bold blue]Enter Name Of Batch: [/bold blue]")

            name_of_student = ask_user("[bold cyan]Enter The Name Of Student Your Wanna Enroll: [/bold cyan]")
            age_of_student = ask_user("[bold cyan]Enter The Age Of Student You Wanna Enroll: [/bold cyan]")
            new_face_embedding = capture_face()
                    
            out = enroll_a_student(selected_batch,name_of_student,age_of_student,new_face_embedding)
            
            if isinstance(out,str):
                print(f"[bold red] {out} [/bold red]")
                
            elif isinstance(out,bool):
                print("[bold orange]Some Error Occured Try Again [/bold orange]")
            else:
                print(f"[bold green]Student Regsitered Sucessfully! [bold green] \n[bold blue] Student Id => {out}[/bold blue]")
        elif option_selected == "q":
            print("[bold yellow]Going Back! [/bold yellow]")
            break
        else:
            print(f"[bold cream]No Option Matches [/bold cream]")
            break 

def conduct_attendance(selected_batch,scan_result):
    date_today = date.today()

    print("[bold blue]Starting Face Scan Please Stand Idle [/bold blue]")
    
    if isinstance(scan_result,str):
        print(f"[bold red] {scan_result} [/bold red]")
        return scan_result        
    
    path = f"{embedding_file_det}{selected_batch}.npy"
    
    stored_embeddings = np.load(path)
    
    sims = (scan_result @ stored_embeddings.T).flatten()
    matching_id = int(np.argmax(sims))
    
    if sims[matching_id] < 0.65:
        print("[bold red]Invalid Face [/bold red]")
        
        return "Student Not Enrolled"    
    
    date_today = [date_today.day,date_today.month,date_today.month]
    
    cur.execute(f"SELECT attendance FROM '{selected_batch}' WHERE id = ?",(matching_id+1,))
    result = cur.fetchone()
    result  = result[0]
    
    if result is not None:
        result = json.loads(result)
        
        if date_today in result:
            print("[bold orange]Already Marked For Today [/bold orange]")
            return "Already Marked For Today"

        result.append(date_today)
    else:
        result = [date_today]
            
    result = json.dumps(result)
    
    cur.execute(f"UPDATE '{selected_batch}' SET attendance = ? WHERE id = ?",(result,matching_id+1))
    attendace_database_conn.commit()

    print("[bold green]Attendence Was Successful [/bold green]")
    
    return True
        
def student_option():
    hour = datetime.now().hour

    if hour not in list(range(attenace_time_range[0],attenace_time_range[1]+1)):
        print(f"[bold red]Time For Attendence Is Gone You'll Be Marked For Today [/bold red] \n[bold cyan]Time Now: {int(hour)}\nAttendance Time Range: ({attenace_time_range[0]} - {attenace_time_range[1]})\nNext Time Be On Time[/bold cyan]\n")
        return
    
    selected_batch = ask_user("[bold cyan]Enter Your Batch: [/bold cyan]")
    
    if table_exists(selected_batch):
        scan_result = capture_face()
        
        conduct_attendance(selected_batch,scan_result)
    else:
        return False

def start_day():
    while True:        
        to_ask = "[bold purple]Press 1 If Yu Are Admin\nPress 2 If You Are Student\nPress Q To Quit\n: [/bold purple]"
    
        user_reply = ask_user(to_ask)
    
        if user_reply == '1':
            admin_handler_result = admin_login_handler()
            
            if admin_handler_result is None:
                continue
            
            if admin_handler_result:
                print("[bold green]Login Sucessful! [/bold green]\n")
                admin_options()
            else:
               print("[bold red]Login Failed [/bold red]\n")

            continue
        elif user_reply == '2':
            student_option()
        elif user_reply == 'q':
            break
        
if __name__ == "__main__":
    start_day()