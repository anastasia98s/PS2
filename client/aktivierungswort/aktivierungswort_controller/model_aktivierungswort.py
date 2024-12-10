import sqlite3
import config
import os
import json

class ModelAktivierungswort:
    def __init__(self):
        self.create_table()
    
    def connect_db(self):
        return sqlite3.connect(config.AKTIVIERUNGSWORT_DATENBANK_PATH)

    def create_table(self):
        dataset_dir = os.path.dirname(config.AKTIVIERUNGSWORT_DATENBANK_PATH)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
            
        conn = self.connect_db()
        cursor = conn.cursor()

        # User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_aktivierungswort_merkmale (
                aktivierungswort_merkmale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                aktivierungswort_merkmale TEXT NOT NULL,
                typ BOOLEAN NOT NULL
            );
        ''')

        conn.commit()
        conn.close()

    #################################################################

    def add_merkmale(self, merkmale, typ):
        merkmale = merkmale.tolist()
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute('INSERT INTO sp_aktivierungswort_merkmale (aktivierungswort_merkmale, typ) VALUES (?, ?)', (json.dumps(merkmale), typ))
            conn.commit()
            if cursor.rowcount == 1:
                return True
            else:
                return False 
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()