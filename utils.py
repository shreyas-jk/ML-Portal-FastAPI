import os
from datetime import datetime
import sqlite3

def get_created_datetime(file_path):
    created_datetime = os.path.getctime(file_path)
    modified_datetime = os.path.getmtime(file_path)
    created_datetime = datetime.fromtimestamp(created_datetime).strftime('%Y-%m-%d %H:%M:%S')
    modified_datetime = datetime.fromtimestamp(modified_datetime).strftime('%Y-%m-%d %H:%M:%S')
    return created_datetime, modified_datetime

def delete_file(file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

def clear_logs_files():
    folder = './Log_Files/'
    for files in os.listdir(folder):
        delete_file(folder + files)

def clear_all_models():
    folder_list = ['./Saved_Data/clustering_models/', './Saved_Data/models/']
    for folder in folder_list:
        for files in os.listdir(folder):
            delete_file(folder + files)

def cursor_to_json(cursor):
    return [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

def execute_sql(query):
    with sqlite3.connect('./Database/etesql.db') as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor

def update_sql(query):
    with sqlite3.connect('./Database/etesql.db') as conn:
        conn.execute(query)
        conn.commit()
    
def preprocess_logs(text):
    data = ''.join(text)
    data = '<pre>' + str(data).replace('[','').replace(']','') + '</pre>'
    return data

def file_if_exists(file_path):
    if os.path.exists(file_path):
        return True
    else:
        return False