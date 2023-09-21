from flask_app import app
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)     
from flask import Flask, render_template,redirect, request , session, flash
from flask_app.models.message import Messages 
from flask_app.models.user import Users 





@app.route('/message/create', methods=["POST"])
def createMessage():
    data = {
        "content": request.form['message'],
        # Pass in the id of the User in session to use as the foreign key to describe who made the Tweet
        "user_id": session['user_id']
    }
  
    # validate method
    if not Messages.validate_user_messages(data): 
        return redirect("/success")
    
    message_id = Messages.create_message(data)
    Messages.create_message(data)
    
    
    return redirect("/success")
   

