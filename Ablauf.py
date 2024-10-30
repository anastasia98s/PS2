import subprocess

try:
    # Mache die Suche
    subprocess.run(
                   [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                   "text_search.py"], 
                   check=True, 
                   cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests")
    print("test_search.py completed successfully.")

    # Erstelle eine Urlliste
    subprocess.run(
                   [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                   "test_Url_list.py"], 
                   check=True, 
                   cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests"
                   )

    print("test_Url_list.py completed successfully.")

    # Formatiere die Urlliste
  
    subprocess.run(
                   [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                   "test_url_extractor.py"], 
                   check=True, 
                   cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests"
                   )

    print("test_url_extractor.py completed successfully.")

    # Erstelle Screenshots von den jeweiligen Seiten.
    subprocess.run(
                [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                "test_Screenshot_from_website.py"], 
                check=True, 
                cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests"
                )
    print("test_url_extractor.py completed successfully.")
    
        # Erstelle Screenshots von den jeweiligen Seiten.
    subprocess.run(
                [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                "test_pytesseract_from_screenshots.py"], 
                check=True, 
                cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests"
                )
    print("test_pytesseract_from_screenshots.py completed successfully.")

# Erstelle Screenshots von den jeweiligen Seiten.
    subprocess.run(
                [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                "test_ob_antwort_gut_ist.py"], 
                check=True, 
                cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests"
                )
    print("test_ob_antwort_gut_ist.py completed successfully.")
    
    
# Erstelle Screenshots von den jeweiligen Seiten.
    subprocess.run(
                [r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\venv\Scripts\python.exe", 
                "test_antworten_zusammenfassen.py"], 
                check=True, 
                cwd=r"C:\Users\Erik\Documents\Sprachassistenten\DuckduckgoAPI\Tests"
                )
    print("test_antworten_zusammenfassen.py completed successfully.")


except subprocess.CalledProcessError as e:
    print(f"Error in {e.cmd}. Stopping execution.")