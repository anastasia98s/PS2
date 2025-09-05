
import pandas as pd

def schreibe_in_textdatei_links():
    df = pd.read_csv('datei.csv')


    # Verwende try-except um den Zugriff auf die Spalten abzufangen
    try:
        url_list = df['content']
    except KeyError:  # Falls die Spalte 'content' nicht existiert
        try:
            url_list = df['href']
        except KeyError:  # Falls die Spalte 'href' auch nicht existiert
            url_list = None  # Oder andere Standardbehandlung
            print("Neither 'content' nor 'href' exist in the DataFrame.")




    with open("urls.txt", "w") as file:
        file.write(str(url_list))

schreibe_in_textdatei_links()