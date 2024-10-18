class Presenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view

    # Model ##########################################################################

    def show_satz(self):
        try:
            return self.model.show_satz()
        except Exception as e:
            return f"Error: {str(e)}"

    def show_anmerkung(self):
        try:
            return self.model.show_anmerkung()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def show_szenario(self):
        try:
            return self.model.show_szenario()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def show_absicht(self):
        try:
            return self.model.show_absicht()
        except Exception as e:
            return f"Error: {str(e)}"
    
    def add_anmerkung(self, anmerkung):
        try:
            if anmerkung:
                result = self.model.add_anmerkung(anmerkung)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def add_szenario(self, szenario):
        try:
            if szenario:
                result = self.model.add_szenario(szenario)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def add_absicht(self, absicht):
        if absicht:
            result = self.model.add_absicht(absicht)
            if result:
                return f"OK!"
            else:
                return "Error!!"
        else:
            return "Error!!"
        
    def add_satz(self, json_satz):
        try:
            if json_satz:
                result = self.model.add_satz(json_satz)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def delete_satz(self, id_satz):
        try:
            if id_satz:
                result = self.model.delete_satz(id_satz)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def delete_anmerkung(self, id_anmerkung):
        try:
            if id_anmerkung:
                result = self.model.delete_anmerkung(id_anmerkung)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def delete_szenario(self, id_szenario):
        try:
            if id_szenario:
                result = self.model.delete_szenario(id_szenario)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def delete_absicht(self, id_absicht):
        try:
            if id_absicht:
                result = self.model.delete_absicht(id_absicht)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    # View ##########################################################################

    def showPage(self, site):
        try:
            return self.view.showPage(site)
        except Exception as e:
            return f"Error: {str(e)}"