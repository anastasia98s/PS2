from datetime import datetime, timedelta
import re
import locale
import config
from playwright.sync_api import sync_playwright

locale.setlocale(locale.LC_TIME, config.ZEIT_STANDORT)

zeitzuordnungen = [
    {"key": "morgen", "value": "08:00", "typ": 0},
    {"key": "mittag", "value": "12:00", "typ": 0},
    {"key": "nachmittag", "value": "15:00", "typ": 0},
    {"key": "abend", "value": "18:00", "typ": 0},
    {"key": "nachts", "value": "22:00", "typ": 0},
    {"key": "früh", "value": "07:00", "typ": 0},
    {"key": "spät", "value": "21:00", "typ": 0},
    {"key": "vormittag", "value": "10:00", "typ": 0},
    {"key": "eins", "value": "01:00", "typ": 1},
    {"key": "zwei", "value": "02:00", "typ": 1},
    {"key": "drei", "value": "03:00", "typ": 1},
    {"key": "vier", "value": "04:00", "typ": 1},
    {"key": "fünf", "value": "05:00", "typ": 1},
    {"key": "sechs", "value": "06:00", "typ": 1},
    {"key": "sieben", "value": "07:00", "typ": 1},
    {"key": "acht", "value": "08:00", "typ": 1},
    {"key": "neun", "value": "09:00", "typ": 1},
    {"key": "zehn", "value": "10:00", "typ": 1},
    {"key": "elf", "value": "11:00", "typ": 1},
    {"key": "zwölf", "value": "12:00", "typ": 1},
    {"key": "dreizehn", "value": "13:00", "typ": 1},
    {"key": "vierzehn", "value": "14:00", "typ": 1},
    {"key": "fünfzehn", "value": "15:00", "typ": 1},
    {"key": "sechzehn", "value": "16:00", "typ": 1},
    {"key": "siebzehn", "value": "17:00", "typ": 1},
    {"key": "achtzehn", "value": "18:00", "typ": 1},
    {"key": "neunzehn", "value": "19:00", "typ": 1},
    {"key": "zwanzig", "value": "20:00", "typ": 1},
    {"key": "einundzwanzig", "value": "21:00", "typ": 1},
    {"key": "zweiundzwanzig", "value": "22:00", "typ": 1},
    {"key": "dreiundzwanzig", "value": "23:00", "typ": 1},
    {"key": "vierundzwanzig", "value": "24:00", "typ": 1}
]

wochentage = {
    "montag": 0, "dienstag": 1, "mittwoch": 2, "donnerstag": 3, 
    "freitag": 4, "samstag": 5, "wochenende":5, "sonntag": 6
}

feiertage = {
    "neujahr": "01-01",
    "heilige drei könige": "06-01",
    "tag der arbeit": "01-05",
    "tag der einheit": "03-10",
    "reformation": "31-10",
    "allerheiligen": "01-11",
    "weihnachten": "24-12",
    "1. weihnachten": "25-12",
    "2. weihnachten": "26-12",
    "silvester": "31-12",
    "karfreitag": "10-04",
    "ostern": "12-04",
    "ostermontag": "13-04",
    "pfingsten": "31-05",
    "pfingstmontag": "01-06",
    "fronleichnam": "11-06",
    "valentinstag": "14-02",
    "valentine": "14-02",
    "frauentag": "08-03",
    "halloween": "31-10",
    "thanksgiving": "25-11",
    "chinesisches neujahr": "12-02",
    "diwali": "04-11",
    "hanukkah": "28-11",
    "eid al-fitr": "13-05",
    "eid al-adha": "20-07",
    "unabhängigkeit usa": "04-07",
    "kanada": "01-07",
    "australischer nationalfeiertag": "26-01",
    "bastille": "14-07",
    "guy fawkes": "05-11",
    "martin luther king jr.": "17-01",
    "st. patrick": "17-03",
    "toten": "02-11",
    "unabhängigkeit indien": "15-08",
    "republik indien": "26-01",
    "goldene woche japan": "29-04",
    "goldene woche china": "01-10",
    "ramadan anfang": "02-04"
}

def date_konverter(datum):
    if not datum:
        return None, config.ERROR_VARIABLE_DATUM
    heute = datetime.now().date()
    
    if re.search(r"\bheute\b", datum.lower()):
        return heute, None
    if re.search(r"\bmorgen\b", datum.lower()):
        return heute + timedelta(days=1), None
    if re.search(r"\b[üu]bermorgen\b", datum.lower()):
        return heute + timedelta(days=2), None
    if re.search(r"\b(gestern|vorgestern)\b", datum.lower()):
        return heute - timedelta(days=1), None
    
    # Wochentage
    datum_lower = datum.lower()
    if datum_lower in wochentage:
        aktueller_wochentag = heute.weekday()
        ziel_wochentag = wochentage[datum_lower]
        
        tage_bis_ziel = (ziel_wochentag - aktueller_wochentag + 7) % 7
        if tage_bis_ziel == 0:
            tage_bis_ziel = 7
            
        return heute + timedelta(days=tage_bis_ziel), None
    
    # Feiertage
    if datum_lower in feiertage:
        jahr = heute.year
        tag, monat = map(int, feiertage[datum_lower].split("-"))
        feiertagsdatum = datetime(jahr, monat, tag).date()
        if feiertagsdatum < heute:
            feiertagsdatum = datetime(jahr + 1, monat, tag).date()
        return feiertagsdatum, None
    
    try:
        # dd.mm.yyyy
        return datetime.strptime(datum, "%d.%m.%Y").date(), None
    except ValueError:
        pass

    try:
        # dd.mm
        if len(datum.split('.')) == 2:
            e_datum = datum + f".{heute.year}"
            return datetime.strptime(e_datum, "%d.%m.%Y").date(), None
    except ValueError:
        pass

    try:
        # dd.mm.
        if len(datum.split('.')) == 3:
            e_datum = datum + str(heute.year)
            return datetime.strptime(e_datum, "%d.%m.%Y").date(), None
    except ValueError:
        pass

    try:
        # dd B (20 Oktober)
        if len(datum.split()) == 2:
            e_datum = datum + f" {heute.year}"
            return datetime.strptime(e_datum, "%d %B %Y").date(), None
    except ValueError:
        pass

    try:
        if len(datum.split()) == 2:
            # dd. B ohne y (20. Oktober)
            e_datum = datum + f" {heute.year}"
            return datetime.strptime(e_datum, "%d. %B %Y").date(), None
    except ValueError:
        pass

    try:
        if len(datum.split()) == 3:
            # dd B yyyy (20 Oktober 2025)
            return datetime.strptime(datum, "%d %B %Y").date(), None
    except ValueError:
        try:
            # dd. B yyyy (20. Oktober 2025)
            return datetime.strptime(datum, "%d. %B %Y").date(), None
        except ValueError:
            return None, config.ERROR_VARIABLE_DATUM
        
    return None, config.ERROR_VARIABLE_DATUM

def zeit_text_konverter(zeit):
    if zeit:
        for item in zeitzuordnungen:
            if item["key"] == zeit.lower():
                if item["typ"] == 1:
                    zeit = f"um {item['value']} Uhr"
                break
        else:
            zeit = zeit.replace('.', ':')
            if ':' not in zeit:
                zeit = f"{zeit}:00"
            zeit = f"um {zeit} Uhr"
        
    return zeit

def date_text_konverter(datum):
    if datum:
        datum_lower = datum.lower()
        if datum_lower in wochentage or datum_lower in feiertage or any(char.isdigit() for char in datum):
            return f"am {datum}"
        else:
            return datum
    else:
        return datum

def date_zeit_konverter(datum, zeit):
    
    datum, errortyp = date_konverter(datum)

    if not datum:
        return None, errortyp
    
    if not zeit:
        return None, config.ERROR_VARIABLE_ZEIT

    # Zeit
    try:
        for item in zeitzuordnungen:
            if item["key"] == zeit.lower():
                zeit = item["value"]
                break
        else:
            if '.' in zeit:
                zeit = zeit.replace('.', ':')
            zeit_muster = r'\b(\d{1,2}:\d{2}|\d{1,2})\b'
            match = re.search(zeit_muster, zeit)
            if match:
                zeit = match.group(0)
                if ":" not in zeit:
                    zeit += ":00"
        
        datum_zeit = datetime.strptime(f"{datum.strftime('%Y-%m-%d')} {zeit}", "%Y-%m-%d %H:%M")
        return datum_zeit.strftime("%Y-%m-%dT%H:%M:%S"), None
    except ValueError:
        return None, config.ERROR_VARIABLE_ZEIT
    
def date_zeit_text_cleaner(text: str, is_zeit: bool) -> str:
    text = re.sub(r'\bum\b|\buhr\b', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'\bam\b', '', text, flags=re.IGNORECASE).strip()
    text = re.sub(r'\s+', ' ', text).strip()
    if is_zeit:
        text = text.replace('.', ':')
    return text

def web_indexing(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("networkidle")
            content = page.content()
            browser.close()
            return content, None
    except Exception as e:
        return None, 1