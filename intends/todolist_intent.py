class ToDoListIntent:
    def __init__(self):
        pass #verbinden mit dem database
    
    # zustand = erledig/.../...
    # artikel = Meeting/.../...
    
    def abfragen(self, i_artikel, i_zeit, i_datum, i_user_id):
        return f"List abfragen, Artikel: {i_artikel}, Zeit: {i_zeit}, Datum: {i_datum}, User: {i_user_id}"
    
    def eingeben(self, i_artikel, i_zeit, i_datum, i_user_id):
        return f"List abfragen, Artikel: {i_artikel}, Zeit: {i_zeit}, Datum: {i_datum}, User: {i_user_id}"
    
    def aendern(self, i_artikel, i_zeit, i_datum, i_zustand, i_user_id):
        return f"List abfragen, Artikel: {i_artikel}, Zeit: {i_zeit}, Datum: {i_datum}, Zustand: {i_zustand}, User: {i_user_id}"
    
    def entfernen(self, i_artikel, i_zeit, i_datum, i_user_id):
        return f"List abfragen, Artikel: {i_artikel}, Zeit: {i_zeit}, Datum: {i_datum}, User: {i_user_id}"