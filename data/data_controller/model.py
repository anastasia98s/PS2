import sqlite3
import json
import config
import os

class Model:
    def __init__(self):
        self.create_table()
    
    def connect_db(self):
        return sqlite3.connect(config.DATASET_PATH)

    def create_table(self):
        dataset_dir = os.path.dirname(config.DATASET_PATH)
        if not os.path.exists(dataset_dir):
            os.makedirs(dataset_dir)
            
        conn = self.connect_db()
        # conn.execute('PRAGMA foreign_keys = ON;')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_anmerkung (
                anmerkung_id INTEGER PRIMARY KEY AUTOINCREMENT,
                anmerkung TEXT NOT NULL UNIQUE
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
                FOREIGN KEY (szenario_id) REFERENCES sp_szenario(szenario_id) ON DELETE RESTRICT,
                FOREIGN KEY (absicht_id) REFERENCES sp_absicht(absicht_id) ON DELETE RESTRICT
            );
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sp_wort (
                wort_id INTEGER PRIMARY KEY AUTOINCREMENT,
                satz_id INTEGER NOT NULL,
                anmerkung_id INTEGER NOT NULL,
                wort TEXT NOT NULL,
                FOREIGN KEY (satz_id) REFERENCES sp_satz(satz_id) ON DELETE CASCADE,
                FOREIGN KEY (anmerkung_id) REFERENCES sp_anmerkung(anmerkung_id) ON DELETE RESTRICT
            );
        ''')

        anmerkung_array = [
            "-",
            "Item-b",
            "Datum-b",
            "Zeit-b",
            "Zeiteinheit-b",
            "Gewichtseinheit-b",
            "Längeneinheit-b",
            "Temperatureinheit-b",
            "Währung-b",
            "Aufgabe-b",
            "Aktion-b",
            "Ort-b",
            "Musik-b",
            "Person-b",
            "Film-b",
            "URL-b",
            "Telefonnummer-b",
            "Nachricht-b",
            "Kategorie-b",
            "Aktie-b",
            "Transport-b",
            "Lautstärke-b",
            "Zahl-b",
            "Operator-b",
            "Pfad-b",
            "Datei-b",
            "Netzwerk-b",
            "WLAN-b",
            "Gerät-b",
            "Anfrage-b",
            "Titel-b",
            "Plattform-b",
            "Calculation-b",
            "Farbe-b",
            "Ereignisse-b",
            "Nachrichteninhalt-b",
            "Haustier-b",
            "Stadt-b",
            "Hausort-b",
            "Wetterdeskriptor-b",
            "Zeitzone-b",
            "Artist-b",
            "Thema-b",
            "Qualität-b",
            "Geschäft-b",
            "Information-b",
            "Medien-i",
            "Item-i",
            "Datum-i",
            "Zeit-i",
            "Zeiteinheit-i",
            "Gewichtseinheit-i",
            "Längeneinheit-i",
            "Temperatureinheit-i",
            "Währung-i",
            "Aufgabe-i",
            "Aktion-i",
            "Ort-i",
            "Musik-i",
            "Person-i",
            "Film-i",
            "URL-i",
            "Telefonnummer-i",
            "Nachricht-i",
            "Kategorie-i",
            "Aktie-i",
            "Transport-i",
            "Lautstärke-i",
            "Zahl-i",
            "Operator-i",
            "Pfad-i",
            "Datei-i",
            "Netzwerk-i",
            "WLAN-i",
            "Gerät-i",
            "Anfrage-i",
            "Titel-i",
            "Plattform-i",
            "Calculation-i",
            "Farbe-i",
            "Ereignisse-i",
            "Nachrichteninhalt-i",
            "Haustier-i",
            "Stadt-i",
            "Hausort-i",
            "Medien-i",
            "Wetterdeskriptor-i",
            "Zeitzone-i",
            "Artist-i",
            "Thema-i",
            "Qualität-i",
            "Geschäft-i",
            "Information-i"
        ]

        szenarios_array = [
            "-",
            "Listen-Szenario",
            "Terminplan-Szenario",
            "Termin-Szenario",
            "Licht-Szenario",
            "Kamera-Szenario",
            "Musik-Szenario",
            "Filme-Szenario",
            "Video-Szenario",
            "URL-Szenario",
            "Nachricht-Szenario",
            "Telefon-Szenario",
            "Wetter-Szenario",
            "Nachrichten-Szenario",
            "Aktien-Szenario",
            "Transport-Szenario",
            "Alarm-Szenario",
            "Audio-Szenario",
            "Wikipedia-Szenario",
            "Daten-Szenario",
            "WLAN-Szenario",
            "Bluetooth-Szenario",
            "Berechnung-Szenario",
            "System-Szenario",
            "Timer-Szenario",
            "Alarm-Szenario",
            "Essen-Szenario",
            "Zeit-Szenario"
        ]


        absichten_array = [
            "-",
            "löschen",
            "eingeben",
            "buchen",
            "stornieren",
            "dimmen",
            "heller machen",
            "machen",
            "ausschalten",
            "einschalten",
            "verringern",
            "vergrößern",
            "fotografieren",
            "video aufnehmen",
            "aufnehmen",
            "abspielen",
            "stoppen",
            "ändern",
            "öffnen",
            "indizieren",
            "senden",
            "anrufen",
            "abfragen",
            "verkaufen",
            "kaufen",
            "entfernen",
            "einstellen",
            "verringern",
            "erhöhen",
            "drucken",
            "lesen",
            "löschen",
            "konvertieren",
            "verbinden",
            "wiederholen",
            "einstellen",
            "pausieren",
            "fortsetzen",
            "mischen",
            "spielen",
            "bestellen"
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


        conn.commit()
        conn.close()

    #################################################################

    def show_anmerkung(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT anmerkung_id, anmerkung FROM sp_anmerkung ORDER BY anmerkung ASC')
        anmerkungen = cursor.fetchall()
        conn.close()

        anmerkungen_list = [
            {"anmerkung_id": anmerkung[0], "anmerkung": anmerkung[1]}
            for anmerkung in anmerkungen
        ]
        return json.dumps(anmerkungen_list) #[anmerkung[0] for anmerkung in anmerkungen]
    
    def show_szenario(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT szenario_id, szenario FROM sp_szenario ORDER BY szenario ASC')
        szenarios = cursor.fetchall()
        conn.close()

        szenarios_list = [
            {"szenario_id": szenario[0], "szenario": szenario[1]}
            for szenario in szenarios
        ]
        return json.dumps(szenarios_list) # [szenario[0] for szenario in szenarios]

    def show_absicht(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT absicht_id, absicht FROM sp_absicht ORDER BY absicht ASC')
        absichten = cursor.fetchall()
        conn.close()

        absichten_list = [
            {"absicht_id": absicht[0], "absicht": absicht[1]}
            for absicht in absichten
        ]

        return json.dumps(absichten_list) # [absicht[0] for absicht in absichten]
    
    def show_satz(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('SELECT sp_satz.satz_id, sp_wort.wort, sp_anmerkung.anmerkung, sp_szenario.szenario, sp_absicht.absicht FROM sp_satz JOIN sp_wort ON sp_satz.satz_id = sp_wort.satz_id JOIN sp_szenario ON sp_satz.szenario_id = sp_szenario.szenario_id JOIN sp_absicht ON sp_satz.absicht_id = sp_absicht.absicht_id JOIN sp_anmerkung ON sp_wort.anmerkung_id = sp_anmerkung.anmerkung_id ORDER BY sp_satz.satz_id DESC')
        """ cursor.execute('''
                            SELECT sp_satz.satz_id, sp_wort.wort, sp_anmerkung.anmerkung, sp_szenario.szenario, sp_absicht.absicht
                            FROM sp_satz
                            LEFT JOIN sp_wort ON sp_satz.satz_id = sp_wort.satz_id
                            LEFT JOIN sp_szenario ON sp_satz.szenario_id = sp_szenario.szenario_id
                            LEFT JOIN sp_absicht ON sp_satz.absicht_id = sp_absicht.absicht_id
                            LEFT JOIN sp_anmerkung ON sp_wort.anmerkung_id = sp_anmerkung.anmerkung_id
                            ORDER BY sp_wort.wort_id
                        ''') """
        """ cursor.execute('''
                            SELECT 
                                sp_satz.satz_id, 
                                IFNULL(sp_wort.wort, '') AS wort, 
                                IFNULL(sp_anmerkung.anmerkung, 'O') AS anmerkung, 
                                IFNULL(sp_szenario.szenario, '') AS szenario, 
                                IFNULL(sp_absicht.absicht, '') AS absicht
                            FROM sp_satz
                            LEFT JOIN sp_wort ON sp_satz.satz_id = sp_wort.satz_id
                            LEFT JOIN sp_szenario ON sp_satz.szenario_id = sp_szenario.szenario_id
                            LEFT JOIN sp_absicht ON sp_satz.absicht_id = sp_absicht.absicht_id
                            LEFT JOIN sp_anmerkung ON sp_wort.anmerkung_id = sp_anmerkung.anmerkung_id
                        ''') """
        saetze = cursor.fetchall()
        conn.close()

        saetze_list = [
            {"satz_id": satz[0], "wort": satz[1], "anmerkung": satz[2], "szenario": satz[3], "absicht": satz[4]}
            for satz in saetze
        ]

        # print(saetze_list)

        return json.dumps(saetze_list)
    
    def add_anmerkung(self, anmerkung):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_anmerkung (anmerkung) VALUES (?)', (anmerkung,))
        conn.commit()
        conn.close()
        return 1
        
    def add_szenario(self, szenario):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_szenario (szenario) VALUES (?)', (szenario,))
        conn.commit()
        conn.close()
        return 1
        
    def add_absicht(self, absicht):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_absicht (absicht) VALUES (?)', (absicht,))
        conn.commit()
        conn.close()
        return 1
        
    def add_satz(self, json_satz):
        absicht_id_value = json_satz['absicht_id_value']
        szenario_id_value = json_satz['szenario_id_value']
        satz_value = json_satz['satz_value']

        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO sp_satz (szenario_id, absicht_id) VALUES (?, ?)', (szenario_id_value, absicht_id_value))
        conn.commit()

        new_id = cursor.lastrowid

        for wort in satz_value:
            cursor.execute('INSERT INTO sp_wort (satz_id, anmerkung_id, wort) VALUES (?, ?, ?)', (new_id, wort['anmerkung_id'], wort['wort']))
            conn.commit()

        conn.close()

        self.show_satz()

        return 1
    
    def delete_satz(self, id_satz):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sp_satz WHERE satz_id = ?', (id_satz,))
        conn.commit()
        conn.close()
        return 1
    
    def delete_anmerkung(self, id_anmerkung):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sp_anmerkung WHERE anmerkung_id = ?', (id_anmerkung,))
        conn.commit()
        conn.close()
        return 1
    
    def delete_szenario(self, id_szenario):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sp_szenario WHERE szenario_id = ?', (id_szenario,))
        conn.commit()
        conn.close()
        return 1
    
    def delete_absicht(self, id_absicht):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM sp_absicht WHERE absicht_id = ?', (id_absicht,))
        conn.commit()
        conn.close()
        return 1