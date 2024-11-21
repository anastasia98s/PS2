import sqlite3
import config
import os

class ModelTextklassifizierung:
    def __init__(self):
        self.create_table()
    
    def connect_db(self):
        return sqlite3.connect(config.TEXTKLASSIFIZIERUNG_DATASET_PATH)

    def create_table(self):
        dataset_dir = os.path.dirname(config.TEXTKLASSIFIZIERUNG_DATASET_PATH)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
            
        conn = self.connect_db()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_anmerkung (
                anmerkung_id INTEGER PRIMARY KEY AUTOINCREMENT,
                anmerkung TEXT NOT NULL UNIQUE,
                is_bio_tag BOOLEAN DEFAULT 1
            );
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_szenario (
                szenario_id INTEGER PRIMARY KEY AUTOINCREMENT,
                szenario TEXT NOT NULL UNIQUE
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_absicht (
                absicht_id INTEGER PRIMARY KEY AUTOINCREMENT,
                absicht TEXT NOT NULL UNIQUE
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_satz (
                satz_id INTEGER PRIMARY KEY AUTOINCREMENT,
                szenario_id INTEGER NOT NULL,
                absicht_id INTEGER NOT NULL,
                FOREIGN KEY (szenario_id) REFERENCES sp_szenario(szenario_id) ON DELETE RESTRICT ON UPDATE CASCADE,
                FOREIGN KEY (absicht_id) REFERENCES sp_absicht(absicht_id) ON DELETE RESTRICT ON UPDATE CASCADE
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_wort (
                wort_id INTEGER PRIMARY KEY AUTOINCREMENT,
                satz_id INTEGER NOT NULL,
                anmerkung_id INTEGER NOT NULL,
                wort TEXT NOT NULL,
                FOREIGN KEY (satz_id) REFERENCES sp_satz(satz_id) ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (anmerkung_id) REFERENCES sp_anmerkung(anmerkung_id) ON DELETE RESTRICT ON UPDATE CASCADE
            );
        ''')

        anmerkung_array = [
            "-",
            "Thema",
            "Aktivität",
            "Zeit",
            "Datum",
            "Ort"
        ]

        szenarios_array = [
            "Wetter",
            "Studienordnung",
            "Wikipedia",
            "ToDo",
            "Uhrzeit",
            "Datum",
            "System",
            "Youtube"
        ]

        absichten_array = [
            "abfragen",
            "eingeben",
            "entfernen",
            "zurückgehen",
            "weitermachen",
            "wiederholen",
            "abbrechen"
        ]

        for anmerkung in anmerkung_array:
            try:
                cursor.execute("INSERT INTO sp_anmerkung (anmerkung) VALUES (?);", (anmerkung,))
            except sqlite3.IntegrityError:
                #continue
                pass

        for szenario in szenarios_array:
            try:
                cursor.execute("INSERT INTO sp_szenario (szenario) VALUES (?);", (szenario,))
            except sqlite3.IntegrityError:
                #continue
                pass

        for absicht in absichten_array:
            try:
                cursor.execute("INSERT INTO sp_absicht (absicht) VALUES (?);", (absicht,))
            except sqlite3.IntegrityError:
                #continue
                pass
        
        cursor.execute("UPDATE sp_anmerkung SET is_bio_tag = NULL WHERE anmerkung_id = 1;")

        conn.commit()
        conn.close()

    #################################################################

    def show_anmerkung(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT anmerkung_id, anmerkung FROM sp_anmerkung ORDER BY anmerkung ASC')
        anmerkungen = cursor.fetchall()
        conn.close()
        return anmerkungen
    
    def show_szenario(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT szenario_id, szenario FROM sp_szenario ORDER BY szenario ASC')
        szenarios = cursor.fetchall()
        conn.close()
        return szenarios

    def show_absicht(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT absicht_id, absicht FROM sp_absicht ORDER BY absicht ASC')
        absichten = cursor.fetchall()
        conn.close()
        return absichten
    
    def show_satz(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT sp_satz.satz_id, sp_wort.wort_id, sp_wort.wort, sp_anmerkung.anmerkung_id, sp_anmerkung.anmerkung, sp_szenario.szenario_id, sp_szenario.szenario, sp_absicht.absicht_id, sp_absicht.absicht FROM sp_satz JOIN sp_wort ON sp_satz.satz_id = sp_wort.satz_id JOIN sp_szenario ON sp_satz.szenario_id = sp_szenario.szenario_id JOIN sp_absicht ON sp_satz.absicht_id = sp_absicht.absicht_id JOIN sp_anmerkung ON sp_wort.anmerkung_id = sp_anmerkung.anmerkung_id ORDER BY sp_satz.satz_id DESC')
        saetze = cursor.fetchall()
        conn.close()
        return saetze
    
    def add_anmerkung(self, anmerkung):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_anmerkung (anmerkung) VALUES (?)', (anmerkung,))
        conn.commit()
        conn.close()
        return True
        
    def add_szenario(self, szenario):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_szenario (szenario) VALUES (?)', (szenario,))
        conn.commit()
        conn.close()
        return True
        
    def add_absicht(self, absicht):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_absicht (absicht) VALUES (?)', (absicht,))
        conn.commit()
        conn.close()
        return True
        
    def add_satz(self, json_satz):
        absicht_id_value = json_satz['absicht_id_value']
        szenario_id_value = json_satz['szenario_id_value']
        satz_value = json_satz['satz_value']

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('INSERT INTO sp_satz (szenario_id, absicht_id) VALUES (?, ?)', (szenario_id_value, absicht_id_value))
        conn.commit()

        new_id = cursor.lastrowid
        for wort in satz_value:
            cursor.execute("PRAGMA foreign_keys = ON")
            cursor.execute('INSERT INTO sp_wort (satz_id, anmerkung_id, wort) VALUES (?, ?, ?)', (new_id, wort['anmerkung_id'], wort['wort']))
            conn.commit()
        conn.close()
        self.show_satz()
        return True
    
    def delete_satz(self, id_satz):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('DELETE FROM sp_satz WHERE satz_id = ?', (id_satz,))
        conn.commit()
        conn.close()
        return True
    
    def delete_anmerkung(self, id_anmerkung):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('DELETE FROM sp_anmerkung WHERE anmerkung_id = ?', (id_anmerkung,))
        conn.commit()
        conn.close()
        return True
    
    def delete_szenario(self, id_szenario):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('DELETE FROM sp_szenario WHERE szenario_id = ?', (id_szenario,))
        conn.commit()
        conn.close()
        return True
    
    def delete_absicht(self, id_absicht):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('DELETE FROM sp_absicht WHERE absicht_id = ?', (id_absicht,))
        conn.commit()
        conn.close()
        return True
    
    def update_wort(self, wort_id, neue_anmerkung_id, neue_wort):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('UPDATE sp_wort SET anmerkung_id = ?, wort = ? WHERE wort_id = ?', (neue_anmerkung_id, neue_wort, wort_id))
        conn.commit()
        conn.close()
        return True
    
    def update_satz_sz_ab(self, satz_id, szenario_id, absicht_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('UPDATE sp_satz SET szenario_id = ?, absicht_id = ? WHERE satz_id = ?', (szenario_id, absicht_id, satz_id))
        conn.commit()
        conn.close()
        return True
    
    def update_anmerkung(self, anmerkung, neues_id, anmerkung_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('UPDATE sp_anmerkung SET anmerkung = ?, anmerkung_id = ? WHERE anmerkung_id = ?', (anmerkung, neues_id, anmerkung_id))
        conn.commit()
        conn.close()
        return True
    
    def update_szenario(self, szenario, neues_id, szenario_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('UPDATE sp_szenario SET szenario = ?, szenario_id = ? WHERE szenario_id = ?', (szenario, neues_id, szenario_id))
        conn.commit()
        conn.close()
        return True
    
    def update_absicht(self, absicht, neues_id, absicht_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA journal_mode = OFF")
        cursor.execute("PRAGMA foreign_keys = ON")
        cursor.execute('UPDATE sp_absicht SET absicht = ?, absicht_id = ? WHERE absicht_id = ?', (absicht, neues_id, absicht_id))
        conn.commit()
        conn.close()
        return True