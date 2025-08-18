from nn_authentifizierung  import train as train_authentifizierung_ki

def main():
    while True:
        print("\n==Authentifizierung")
        print("Bitte wähle eine Option:")
        print("1. AI Training")
        print("2. Beenden")
        
        auswahl = input("Gib die Nummer der Option ein: ")

        if auswahl == '1':
            train_authentifizierung_ki.train()
        elif auswahl == '2':
            break
        else:
            print("Ungültige Auswahl, bitte versuche es erneut.")
        
if __name__ == "__main__":
    main()