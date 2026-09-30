import os
import json


DB_FILE = 'database.json'

def init_db():
    if not(os.path.exists(DB_FILE)):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump({'users': [], 'orders': []}, f, ensure_ascii=False, indent=4)

def register_new_user(user_id, username, first_name):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_users = json.load(f)
    for user in db_users['users']:
        if user['user_id'] == user_id:
            return
    new_user = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "agreed_to_terms": False
    }
    db_users['users'].append(new_user)

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db_users, f, ensure_ascii=False, indent=4)

def has_user_agreed(user_id):
    if not os.path.exists(DB_FILE):
        return False
        
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_users = json.load(f)

    for user in db_users['users']:
        if user['user_id'] == user_id:
            return user.get('agreed_to_terms', False) 
    return False

def save_user_agreement(user_id, username, first_name):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_users = json.load(f)
        
    for user in db_users['users']:
        if user['user_id'] == user_id:
            user['agreed_to_terms'] = True
            break
    else:
        new_user = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "agreed_to_terms": True
        }
        db_users['users'].append(new_user)
        
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db_users, f, ensure_ascii=False, indent=4)