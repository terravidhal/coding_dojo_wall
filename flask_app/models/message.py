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
         # Aucun ne peut représenter un espace actuellement vide pour qu'un seul dictionnaire utilisateur soit placé ici, car un Tweet est créé par UN Utilisateur.   Nous voulons qu'une instance User et tous ses attributs soient placés ici, donc quelque chose comme data['...'] ne fonctionnera pas car nous devons créer nous-mêmes l'instance User.
        self.creator = None

   

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
    


    
    @classmethod
    def get_all_messages_with_creator(cls):
        # Get all messages, and their one associated User that created it
        query = "SELECT * FROM messages JOIN users ON users.id = messages.users_id;"
        results = connectToMySQL(cls.DB).query_db(query)
       #print('++++++++++++', results)
        all_messages = []
        for elt in results:
            # Create a Tweet class instance from the information from each db elt
            one_message = cls(elt)
            # Prepare to make a User class instance, looking at the class in models/user.py
            one_message_author_info = {
                # Any fields that are used in BOTH tables will have their name changed, which depends on the order you put them in the JOIN query, use a print statement in your classmethod to show this.
                "id": elt['users.id'], 
                "first_name": elt['first_name'],
                "last_name": elt['last_name'],
                "email": elt['email'],
                "password": elt['password'],
                "created_at": elt['users.created_at'],
                "updated_at": elt['users.updated_at']
            }
            # Create the User class instance that's in the user.py model file
            author_instance = user.Users(one_message_author_info)
            # Associate the Tweet class instance with the User class instance by filling in the empty creator attribute in the Tweet class
            one_message.creator = author_instance
            # Append the Tweet containing the associated User to your list of messages
            all_messages.append(one_message)
    
        return all_messages

 
