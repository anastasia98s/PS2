class ToDoListIntent:
    def __init__(self):
        pass # verbinden mit dem database
    
    # Zustand = erledig/unerledigt
    # Artikel = Meeting/.../...
    
    def abfragen(self, i_artikel, i_zeit, i_datum, i_zustand, i_user_id):
        # gefragte Artikel in Datenbank suchen

        if i_artikel: # Frag nach Zeit
            if i_zustand:
                return f"du hast {i_zustand} {i_artikel} am [2 Oktober] um [12] uhr"
            else:
                return f"Du hast {i_artikel} am [2 Oktober] um [12] uhr"
            
        elif i_zeit or i_datum: # Frag nach Artikel in einem bestimmten Zeit/Datum
            if i_zeit and i_datum:
                return f"Am {i_datum} um {i_zeit} du hast [MEETING]"
            elif i_datum:
                return f"Am {i_datum} du hast [MEETING]"
            elif i_zeit:
                return f"um {i_zeit} du hast [MEETING]"
    
    def eingeben(self, i_artikel, i_zeit, i_datum, i_user_id):
        # neuer Artikel In die Datenbank eingeben
        return f"neue {i_artikel} am {i_datum} um {i_zeit} wurde in ToDO Liste eingegeben"
    
    def aendern(self, i_artikel, i_zeit, i_datum, i_zustand, i_user_id):
        # Artikel In die Datenbank ändern
        return f"{i_artikel} am {i_datum} um {i_zeit} Uhr wurde auf {i_zustand} in ToDO Liste geändert"
    
    def entfernen(self, i_artikel, i_zeit, i_datum, i_user_id):
        # Artikel In die Datenbank entfernen
        return f"{i_artikel} am {i_datum} um {i_zeit} Uhr wurde in ToDO Liste gelöscht"