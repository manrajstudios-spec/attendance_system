import bcrypt

pass_file = "data/admin_pass.txt"

def record_new_password(password):
    password = bcrypt.hashpw(password.encode("utf-8"),bcrypt.gensalt()).decode()
    
    with open(pass_file,'w') as f:
        f.write(password)

    return password

def compare_pass(entered_pass):
    try:
        with open(pass_file,'r') as f:
            admin_pass = f.read().strip().encode("utf-8")
            print("OLd")
    except:
        admin_pass = record_new_password(entered_pass).encode("utf-8")
        print("NEW")

    return bcrypt.checkpw(entered_pass.encode("utf-8"),admin_pass)