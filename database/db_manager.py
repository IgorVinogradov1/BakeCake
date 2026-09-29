import os
import json


DB_FILE = 'database.json'

def init_db():
    if not(os.path.exists(DB_FILE)):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump({'users': [], 'orders': []}, f, ensure_ascii=False, indent=4)