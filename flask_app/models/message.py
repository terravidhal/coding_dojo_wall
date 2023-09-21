from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
import re  # the regex module

class Messages:
    DB = 'dojo_wall'
    def __init__(self, data):
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user =  None  
        
         
    # CREATE MESSAGE
    @classmethod
    def create_message(cls, datas):
        query = "INSERT INTO messages (content, created_at, updated_at, users_id) VALUES (%(content)s,NOW(), NOW(),%(user_id)s);"
        results = connectToMySQL(cls.DB).query_db(query, datas)
        message_id_created = results 
        return message_id_created 


    # VALIDATE USER MESSAGES (INPUT MESSAGE)
    @staticmethod
    def validate_user_messages(data):
        is_valid = True
        if len(data["content"]) <= 0 :
            is_valid = False
            flash("* Post content must not be blank", "message")
          
        return is_valid

    # DELETE MESSAGE
    @classmethod
    def delete_message(cls, datas):
        query = "DELETE FROM messages WHERE id = %(id)s;"
        results = connectToMySQL(cls.DB).query_db(query, datas)
        message_id_deleted = results 
        return message_id_deleted 


    # SHOW ALL MESSAGES  WITH ALL USERS (ALL COMMUNITY POSTS)
    @classmethod
    def get_all_messages_with_all_users(cls):
        query = "SELECT * FROM messages JOIN users ON users.id = messages.users_id;"
        results = connectToMySQL(cls.DB).query_db(query)

        all_posts = [] 

        for obj in results: 
            user_data = {   
                "id": obj["users_id"],
                "email": obj["email"],
                "first_name": obj["first_name"],
                "last_name": obj["last_name"],
                "created_at": obj["users.created_at"],
                "updated_at": obj["users.updated_at"],
                "password": obj["password"]
            }

            user_instance = user.Users(user_data) 

            mssges_instance = Messages(obj)  
            
            mssges_instance.user = user_instance 

            all_posts.append(mssges_instance)   

        return all_posts 

    





   
        


 














