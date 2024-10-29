from datetime import datetime, timedelta

def DateZeitKonvertierung(datum, zeit):
    # Zeitzuordnung für verschiedene Tageszeiten
    zeitzuordnungen = {
        "morgen": "08:00",
        "mittag": "12:00",
        "nachmittag": "15:00",
        "abend": "18:00",
        "nacht": "22:00",
        "früh": "07:00",
        "spät": "21:00",
        "vormittag": "10:00"
    }
    
    # Aktuelles Datum und Zeit
    jetzt = datetime.now()
    
    # Datum definieren
    if datum.lower() == "heute":
        datum = jetzt
    elif datum.lower() == "morgen":
        datum = jetzt + timedelta(days=1)
    else:
        try:
            datum = datetime.strptime(datum, "%d.%m.%Y")  # z.B., "18.11.2025"
        except ValueError:
            try:
                datum = datetime.strptime(datum, "%d.%m")  # z.B., "19.12"
                datum = datum.replace(year=jetzt.year)  # Setzt das aktuelle Jahr
            except ValueError:
                raise ValueError("Ungültiges Datumsformat. Verwenden Sie 'heute', 'morgen', 'dd.mm' oder 'dd.mm.yyyy'.")
    print("test", datum)
    # Zeit definieren
    if zeit.lower() in zeitzuordnungen:
        zeit = zeitzuordnungen[zeit.lower()]
    else:
        zeit = zeit.replace(" Uhr", "")
        if ":" not in zeit:
            zeit += ":00"  # Fügt Minuten hinzu, falls nicht angegeben
    
    # Kombiniertes Datum und Zeitformat
    datum_zeit = datetime.strptime(f"{datum.strftime('%Y-%m-%d')} {zeit}", "%Y-%m-%d %H:%M")
    
    # Ergebnis im gewünschten Format
    return datum_zeit.strftime("%Y-%m-%dT%H:%M:%S")

# Tests
print(DateZeitKonvertierung("heute", "19:21 Uhr"))         # 2024-10-28T18:00:00
print(DateZeitKonvertierung("morgen", "18 Uhr"))        # 2024-10-29T18:00:00
print(DateZeitKonvertierung("morgen", "18:30 Uhr"))     # 2024-10-29T18:30:00
print(DateZeitKonvertierung("18.11.2025", "morgen"))    # 2025-11-18T08:00:00
print(DateZeitKonvertierung("19.12", "nachmittag"))     # 2024-12-19T15:00:00



import re

# Contoh string
text1 = "Sekarang jam 10:30 pagi"
text2 = "heute um 10 Uhr"

# Regex untuk mengambil jam
pattern = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'

# Mengambil jam dari kedua string
match1 = re.search(pattern, text1)
match2 = re.search(pattern, text2)

# Menampilkan hasil
if match1:
    print("Jam dari text1:", match1.group(0))  # Output: 10:30
if match2:
    print("Jam dari text2:", match2.group(0))  # Output: 10


print( datetime.now().strftime("%H:%M"))


def date_konvertierung(datum):
    jetzt = datetime.now()

    if datum.lower() == "morgen":
        return (jetzt + timedelta(days=1)).strftime("%Y-%m-%d")
    else:
        try:
            return datetime.strptime(datum, "%d.%m.%Y").strftime("%Y-%m-%d")
        except ValueError:
            try:
                datum = datetime.strptime(datum, "%d.%m")
                return datum.replace(year=jetzt.year).strftime("%Y-%m-%d")
            except ValueError:
                raise ValueError("Ungültiges Datumsformat. Verwenden Sie 'heute', 'morgen', 'dd.mm' oder 'dd.mm.yyyy'.")

# Contoh penggunaan
print(date_konvertierung("morgen"))  # Hasil akan menjadi '2024-10-30'






from datetime import datetime, timedelta
import locale

def date_konvertierung(datum):
    # Set locale ke Jerman
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')  # Pastikan ini tersedia di sistem Anda

    jetzt = datetime.now()

    # Memeriksa apakah input adalah 'heute'
    if datum.lower() == "heute":
        return jetzt.strftime("%Y-%m-%d")

    # Memeriksa apakah input adalah 'morgen'
    if datum.lower() == "morgen":
        return (jetzt + timedelta(days=1)).strftime("%Y-%m-%d")

    # Menambahkan dukungan untuk format "2 Oktober", "2 Oktober 2023", "18.11.2025", dan "18.11"
    try:
        # Jika input memiliki format dd.mm.yyyy
        return datetime.strptime(datum, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        pass  # Lanjutkan ke pengecekan berikutnya

    try:
        # Jika input memiliki format dd.mm
        if len(datum.split('.')) == 2:
            datum = datum + f".{jetzt.year}"  # Tambahkan tahun saat ini
            return datetime.strptime(datum, "%d.%m.%Y").strftime("%Y-%m-%d")
    except ValueError:
        pass  # Lanjutkan ke pengecekan berikutnya

    try:
        # Jika input memiliki format dd B
        if len(datum.split()) == 2:
            datum = datum + f" {jetzt.year}"
        
        return datetime.strptime(datum, "%d %B %Y").strftime("%Y-%m-%d")
    
    except ValueError:
        try:
            # Jika input hanya memiliki format dd B tanpa tahun
            datum = datetime.strptime(datum, "%d %B")  
            return datum.replace(year=jetzt.year).strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("Ungültiges Datumsformat. Verwenden Sie 'heute', 'morgen', 'dd.mm', 'dd.mm.yyyy', 'd MMMM' oder 'd MMMM yyyy'.")

# Contoh pemanggilan
print(date_konvertierung("18.11.2025"))  # Misalnya, output: 2025-11-18
print(date_konvertierung("18.11"))        # Misalnya, output: 2024-11-18
print(date_konvertierung("2 Oktober"))    # Misalnya, output: 2024-10-02
print(date_konvertierung("2 Oktober 2024"))  # Misalnya, output: 2024-10-02
print(date_konvertierung("morgen"))
print(date_konvertierung("heute"))
















def date_konvertierung1(datum):
    locale.setlocale(locale.LC_TIME, 'de_DE.UTF-8')
    jetzt = datetime.now()
    if datum.lower() == "heute":
        return jetzt
    
    if datum.lower() == "morgen":
        return (jetzt + timedelta(days=1))
    
    try:
        # dd.mm.yyyy
        return datetime.strptime(datum, "%d.%m.%Y")
    except ValueError:
        pass

    try:
        # dd.mm
        if len(datum.split('.')) == 2:
            datum = datum + f".{jetzt.year}"  # Tambahkan tahun saat ini
            return datetime.strptime(datum, "%d.%m.%Y")
    except ValueError:
        pass

    try:
        # dd B
        if len(datum.split()) == 2:
            datum = datum + f" {jetzt.year}"
        
        return datetime.strptime(datum, "%d %B %Y")
    
    except ValueError:
        try:
            # dd B ohne y
            datum = datetime.strptime(datum, "%d %B")  
            return datum.replace(year=jetzt.year)
        except ValueError:
            raise ValueError("Ungültiges Datumsformat. Verwenden Sie 'heute', 'morgen', 'dd.mm', 'dd.mm.yyyy', 'd MMMM' oder 'd MMMM yyyy'.")

def DateZeitKonvertierung1(datum, zeit):
    zeitzuordnungen = {
        "morgen": "08:00",
        "mittag": "12:00",
        "nachmittag": "15:00",
        "abend": "18:00",
        "nacht": "22:00",
        "früh": "07:00",
        "spät": "21:00",
        "vormittag": "10:00"
    }
        
    datum = date_konvertierung1(datum)
    
    # Zeit definieren
    if zeit.lower() in zeitzuordnungen:
        zeit = zeitzuordnungen[zeit.lower()]
    else:
        """ zeit_muster = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'
        zeit = re.search(zeit_muster, zeit)
        if ":" not in zeit:
            zeit += ":00" """
        
        zeit_muster = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'
        match = re.search(zeit_muster, zeit)
        if match:  # Memeriksa apakah ada hasil pencarian
            zeit = match.group(0)  # Ambil string waktu yang cocok
            if ":" not in zeit:
                zeit += ":00"  # Tambahkan ":00" jika tidak ada menit
        
        """ zeit = zeit.replace(" Uhr", "")
        if ":" not in zeit:
            zeit += ":00" """
    
    # Kombiniertes Datum und Zeitformat
    datum_zeit = datetime.strptime(f"{datum.strftime('%Y-%m-%d')} {zeit}", "%Y-%m-%d %H:%M")
    return datum_zeit.strftime("%Y-%m-%dT%H:%M:%S")


print(DateZeitKonvertierung1("heute", "19:21 Uhr"))         # 2024-10-28T18:00:00
print(DateZeitKonvertierung1("21 Oktober", "18 Uhr"))        # 2024-10-29T18:00:00
print(DateZeitKonvertierung1("morgen", "18:30 Uhr"))     # 2024-10-29T18:30:00
print(DateZeitKonvertierung1("18.11.2025", "morgen"))    # 2025-11-18T08:00:00
print(DateZeitKonvertierung1("19.12", "nachmittag"))     # 2024-12-19T15:00:00