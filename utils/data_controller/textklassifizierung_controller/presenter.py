import json
import config
import webview
from utils.data_controller.textklassifizierung_controller.model_textklassifizierung import ModelTextklassifizierung
from utils.data_controller.textklassifizierung_controller.view import View
from nn_textklassifizierung.predictor import Predictor as PredictorText
from nn_textklassifizierung import train

class PresenterTextklassifizierung:
    def __init__(self):
        self.model = ModelTextklassifizierung()
        self.view = View()

    # Model ##########################################################################

    def show_satz(self):
        try:
            saetze = self.model.show_satz()
            saetze_list = [
                {"satz_id": satz[0],
                "wort_id": satz[1],
                "wort": satz[2],
                "anmerkung_id": satz[3],
                "anmerkung": satz[4],
                "szenario_id": satz[5],
                "szenario": satz[6],
                "absicht_id": satz[7],
                "absicht": satz[8]}
                for satz in saetze
            ]
            return json.dumps(saetze_list)
        except Exception as e:
            return f"Error: {str(e)}"

    def show_anmerkung(self):
        try:
            anmerkungen = self.model.show_anmerkung()
            anmerkungen_list = [
                {"anmerkung_id": anmerkung[0], "anmerkung": anmerkung[1]}
                for anmerkung in anmerkungen
            ]
            return json.dumps(anmerkungen_list)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def show_szenario(self):
        try:
            szenarios = self.model.show_szenario()
            szenarios_list = [
                {"szenario_id": szenario[0], "szenario": szenario[1]}
                for szenario in szenarios
            ]
            return json.dumps(szenarios_list)
        except Exception as e:
            return f"Error: {str(e)}"
    
    def show_absicht(self):
        try:
            absichten = self.model.show_absicht()
            absichten_list = [
                {"absicht_id": absicht[0], "absicht": absicht[1]}
                for absicht in absichten
            ]
            return json.dumps(absichten_list)
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
    
    def update_wort(self, wort_id, neue_anmerkung_id, neue_wort):
        try:
            if wort_id and neue_anmerkung_id and neue_wort:
                result = self.model.update_wort(wort_id, neue_anmerkung_id, neue_wort)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def update_satz_sz_ab(self, satz_id, szenario_id, absicht_id):
        try:
            if satz_id and szenario_id and absicht_id:
                result = self.model.update_satz_sz_ab(satz_id, szenario_id, absicht_id)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
        
    def update_anmerkung(self, anmerkung, neues_id, anmerkung_id):
        try:
            if anmerkung and neues_id and anmerkung_id:
                result = self.model.update_anmerkung(anmerkung, neues_id, anmerkung_id)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def update_szenario(self, szenario, neues_id, szenario_id):
        try:
            if szenario and neues_id and szenario_id:
                result = self.model.update_szenario(szenario, neues_id, szenario_id)
                if result:
                    return f"OK!"
                else:
                    return "Error!!"
            else:
                return "Error!!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def update_absicht(self, absicht, neues_id, absicht_id):
        try:
            if absicht and neues_id and absicht_id:
                result = self.model.update_absicht(absicht, neues_id, absicht_id)
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
        
    def ask_ki_hilfe(self, text):
        predictor_text = PredictorText(config.TEXTKLASSIFIZIERUNG_TRAINED_PATH)
        anmerkung_satz_labels, woerter_anmerkungen, absicht_satz_labels, absicht_class_scores, szenario_satz_labels, szenario_class_scores = predictor_text.predict(text)
        
        absicht_id = int(absicht_class_scores[0][absicht_satz_labels])
        szenario_id = int(szenario_class_scores[0][szenario_satz_labels])
        anmerkungen_ids = woerter_anmerkungen[0]
        anmerkungen_text = woerter_anmerkungen[1]

        for i in range(len(anmerkungen_ids)):
            anmerkungen_ids[i] = int(abs(anmerkung_satz_labels[anmerkungen_ids[i]]))
        
        json_preds = {
            "absicht": absicht_id,
            "szenario": szenario_id,
            "anmerkungen_ids": anmerkungen_ids,
            "anmerkungen_text": anmerkungen_text
        }
        return json.dumps(json_preds)
    
    def train_ki(self):
        try:
            train.train()
            return "Training erfolgreich abgeschlossen."
        except Exception as e:
            return f"Error: {e}"
        
    def open_gui(self):
        webview.create_window('Data Controller', html=self.view.showPage(1), js_api=self)
        webview.start()