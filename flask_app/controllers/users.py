from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask import Flask, render_template,redirect, request , session, flash
from flask_app.models.user import Users 
from flask_app.models.message import Messages 




# HOME 
@app.route("/")
def home():
   return redirect('/register')

# SHOW REGISTER PAGE
@app.route("/register")
def register_page():
   if "user_id" in session: 
        session["user_created"] = False  
        flash("you are  logged in, please log out", 'success')
        return redirect ("/success")
   
   return render_template("register.html")


# REGISTER / CREATE NEW USER
@app.route('/register_process', methods=["POST"])
def register_process():

    datas = {
        "fname": request.form["firstname"],
        "lname": request.form["lastname"],
        "eml": request.form["email"],
        "psswrd": request.form["password"],
        "conf_pass": request.form["conf_pass"],
    }

    # validate method
    if not Users.validate_user_infos(datas): 
        # Make it so the data the user input isn't lost when they have an error
        session["firstname"] = request.form["firstname"]
        session["lastname"] = request.form["lastname"]
        session["email"] = request.form["email"]
        return redirect("/register")
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    datas["psswrd"] = pw_hash
    user_id = Users.create_user(datas)
    session["user_id"] = user_id
    session["firstname"] = request.form["firstname"] 
    session["user_created"] = True 
    flash("User created!","success")
    return redirect("/success")



# SHOW LOGIN PAGE
@app.route("/login")
def login_page():
   if "user_id" in session: 
        session["user_created"] = False  
        flash("You are  logged in, please log out", 'success')
        return redirect ("/success")
   
   return render_template("login.html")


# LOGIN / SHOW USER SESSION
@app.route('/login_process', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    this_user = Users.user_with_specific_email(data)
    if not this_user:
        flash("Invalid Email", "login")
        session["email"] = request.form["email"]
        return redirect("/login")
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid Password", "login")
        session["email"] = request.form["email"]
        return redirect('/login')
    
    session['user_id'] = this_user.id
    session["firstname"] = this_user.first_name 
    
    return redirect("/success")



# SHOW SUCCESS PAGE
@app.route("/success")
def success():
    if "user_id" not in session: 
        flash("You are not logged in, please log in", 'login')
        return redirect ("/login")


    all_mssag_users = Messages.get_all_messages_with_creator()
    


    return render_template("success.html", all_the_messages = all_mssag_users)


# END SESSION
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")



@app.errorhandler(404)  # we specify in parameter here the type of error, here it is 404
def page_not_found(
    error,
):  # (error) is important because it recovers the instance of the error that was thrown
    return f"<h2 style='text-align:center;padding-top:40px'>Error 404. Sorry! No response. Try again</h2>"    

