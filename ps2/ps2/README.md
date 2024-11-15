# Intent zur PDF Verarbeitung

## Intentbeschreibung

Dieses Intent ermöglicht die Verarbeitung eines PDF-Dokuments, in unserem Fall einer Prüfungsordnung, und bietet ein Frage-Antwort-System basierend auf den extrahierten Inhalten. Der Ablauf umfasst folgende Schritte:

1. **PDF-Verarbeitung**:  
   - Die PDF-Datei wird in reinen Text umgewandelt.  
   - Enthält das PDF Hyphen (Trennstriche), werden diese automatisch entfernt, um einen flüssigen Text zu erzeugen.

2. **Paragraphenaufteilung**:  
   - Der extrahierte Text wird anhand der Paragraphenstruktur (z. B. "`§ 1`") in sinnvolle Abschnitte gegliedert.  
   - Übergeordnete und untergeordnete Paragraphen (bspw. ) werden zugeordnet, um eine konsistente Datenstruktur zu gewährleisten.

3. **Frage-Antwort-Logik**:  
   - Der Nutzer stellt eine spezifische Frage.  
   - Das System analysiert die Frage und durchsucht die Paragraphen, um den relevantesten Paragraphen für die Beantwortung zu finden.  
   - Basierend auf dem relevantesten Abschnitt wird die Frage beantwortet.

4. **Antworten ausgeben**:  
   - Die generierte Antwort wird ausgegeben.


---

## Voraussetzungen

- **Python 3.8 oder höher**
- Installierte Python-Bibliotheken:
  - `pdfplumber` (PDF-Textextraktion)
  - `re` (Reguläre Ausdrücke zur Textaufbereitung)
  - `scikit-learn` (TF-IDF und Cosine Similarity)
  - `requests` (API-Aufrufe, falls externe Modelle verwendet werden)

- Installiere die Abhängigkeiten mit:

    - pip install pdfplumber scikit-learn requests

- Nutzung von llama 3.2
---

## Ausführung

- python main.py

--- 

## TO DO:
- sinnvolles Filtersystem für Antworten
- Kompatibilität mit BERT