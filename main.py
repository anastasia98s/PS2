import re
import requests

def fetch_wetter(city_name):
    url = f"http://wttr.in/{city_name}?format=%C+%t"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Konnte Wetterinformationen nicht abrufen."

def fetch_temperature():
    return "20°C"  # Contoh fungsi lain

def call_function(func_name):
    if func_name == "fetch_wetter":
        return fetch_wetter("Berlin")  # Ganti dengan nama kota yang diinginkan
    elif func_name == "fetch_temperature":
        return fetch_temperature()
    else:
        return "Fungsi tidak ditemukan."

# Contoh kalimat
antwort_dialog = "Wird es bewölkt mit %%fetch_wetter%% Grad und die Temperatur ist %%fetch_temperature%%."

# Mengganti semua fungsi dalam format %%...%%
pattern = r"%%(.*?)%%"
matches = re.findall(pattern, antwort_dialog)

for match in matches:
    result = call_function(match)  # Memanggil fungsi berdasarkan nama
    antwort_dialog = antwort_dialog.replace(f"%%{match}%%", result)

print(antwort_dialog)
