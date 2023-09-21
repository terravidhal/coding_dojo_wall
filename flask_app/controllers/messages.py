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
        "user_id": session['user_id']
    }
  
    # validate method
    if not Messages.validate_user_messages(data): 
        return redirect("/success")
    
    message_id = Messages.create_message(data)
    
    return redirect("/success")


@app.route("/message/delete/<message_id>")
def delete_message(message_id):
    datas = {
        "id":  message_id,
    }
   
    Messages.delete_message(datas)

    return redirect("/success")
   

