import sqlite3
import config
import os
import json

class ModelUser:
    def __init__(self):
        self.create_table()
    
    def connect_db(self):
        return sqlite3.connect(config.USER_DATENBANK_PATH)

    def create_table(self):
        dataset_dir = os.path.dirname(config.USER_DATENBANK_PATH)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
            
        conn = self.connect_db()
        cursor = conn.cursor()

        # User
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_benutzer (
                benutzer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                benutzer TEXT NOT NULL
            );
        ''')

        # Authentifizierungsdatensatz
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_merkmale (
                merkmale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                benutzer_id INTEGER NOT NULL,
                merkmale TEXT,
                FOREIGN KEY (benutzer_id) REFERENCES sp_benutzer(benutzer_id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        ''')

        # To-Do-Liste
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_todo (
                todo_id INTEGER PRIMARY KEY AUTOINCREMENT,
                benutzer_id INTEGER NOT NULL,
                todo TEXT NOT NULL,
                datum DATETIME,
                FOREIGN KEY (benutzer_id) REFERENCES sp_benutzer(benutzer_id) ON DELETE CASCADE ON UPDATE CASCADE
            );
        ''')

        conn.commit()
        conn.close()

    #################################################################

    # neues User eingeben
    def add_benutzer(self, name):
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO sp_benutzer (benutzer) VALUES (?)', (name,))
            conn.commit()
            if cursor.rowcount == 1:
                return cursor.lastrowid
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()

    # Authentifizierungsdaten von Users eingeben
    def add_merkmale(self, benutzer_id, merkmale):
        merkmale = merkmale.tolist()
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute('INSERT INTO sp_merkmale (benutzer_id, merkmale) VALUES (?, ?)', (benutzer_id, json.dumps(merkmale)))
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

    # To-Do von Users eingeben
    def add_todo(self, aktivitaet, datezeit, benutzer_id):
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute('INSERT INTO sp_todo (benutzer_id, todo, datum) VALUES (?, ?, ?)', (benutzer_id, aktivitaet, datezeit))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()
    
    # einen Benutzernamen abfragen
    def show_benutzer_name(self, benutzer_id):
        conn = self.connect_db()
        benutzer_id = int(benutzer_id)
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT benutzer FROM sp_benutzer WHERE benutzer_id = ?', (benutzer_id,))
            benutzer = cursor.fetchone()
        finally:
            conn.close()
        if benutzer:
            return benutzer[0]
        return None
    
    # To-Do-Liste von einem User abfragen
    def show_todo(self, aktivitaet, datum, datezeit, benutzer_id):
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if aktivitaet: # Frag nach Zeit
                if datum:  # Bsp. Wann ist mein Meeting morgen
                    cursor.execute('SELECT * FROM sp_todo WHERE todo LIKE ? AND DATE(datum) = ? AND benutzer_id = ?', (f'%{aktivitaet}%', datum, benutzer_id))
                else: # Bsp. Wann ist mein Meeting
                    cursor.execute('SELECT * FROM sp_todo WHERE todo LIKE ? AND benutzer_id = ?', (f'%{aktivitaet}%', benutzer_id))
            elif datezeit or datum:
                if datezeit: # Was habe ich morgen um 12 Uhr
                    cursor.execute('SELECT * FROM sp_todo WHERE datum = ? AND benutzer_id = ?', (datezeit, benutzer_id))
                else: # Was habe ich morgen
                    cursor.execute('SELECT * FROM sp_todo WHERE DATE(datum) = ? AND benutzer_id = ?', (datum, benutzer_id))
            else:
                cursor.execute('SELECT * FROM sp_todo WHERE benutzer_id = ? ORDER BY datum ASC', (benutzer_id,))
            return cursor.fetchall()
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            conn.close()
    
    # To-Do von einem User löschen
    def delete_todo(self, aktivitaet, datum, datezeit, benutzer_id):
        conn = self.connect_db()
        try:
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON")
            if datezeit:
                cursor.execute('DELETE FROM sp_todo WHERE todo LIKE ? AND datum = ? AND benutzer_id = ?', (f'%{aktivitaet}%', datezeit, benutzer_id))
            else:
                if datum:
                    cursor.execute('DELETE FROM sp_todo WHERE todo LIKE ? AND DATE(datum) = ? AND benutzer_id = ?', (f'%{aktivitaet}%', datum, benutzer_id))
                else:
                    cursor.execute('DELETE FROM sp_todo WHERE todo LIKE ? AND benutzer_id = ?', (f'%{aktivitaet}%', benutzer_id))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            conn.close()