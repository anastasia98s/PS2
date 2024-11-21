class SystemIntent: #für intent mit prozess wie: musik/videos/timer
    def __init__(self):
        self.intent_presenter = None # von aktuellem Intent eingesetzt

    def zurueckgehen(self):
        if self.intent_presenter:
            return self.intent_presenter.aktion_zurueckgehen()
        else:
            return "kein Playlist gefunden", None
        
    def weitergehen(self):
        print("==============================OK")
        if self.intent_presenter:
            return self.intent_presenter.aktion_weitergehen()
        else:
            return "kein Playlist gefunden", None
    
    def wiederholen(self):
        
        if self.intent_presenter:
            return self.intent_presenter.aktion_wiederholen()
        else:
            return "kein Playlist gefunden", None
    
    def abbrechen(self):
        
        if self.intent_presenter:
            return self.intent_presenter.aktion_abbrechen()
        else:
            return "kein Vorgang gefunden", None