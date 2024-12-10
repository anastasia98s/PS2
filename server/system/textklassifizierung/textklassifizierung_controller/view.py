import textklassifizierung_controller.template.base
import textklassifizierung_controller.template.page_1
import textklassifizierung_controller.template.page_2

class View:
    def __init__(self):
        self.head_1 = textklassifizierung_controller.template.page_1.head
        self.head_2 = textklassifizierung_controller.template.page_2.head
        self.body_1 = textklassifizierung_controller.template.page_1.body
        self.body_2 = textklassifizierung_controller.template.page_2.body

    def showPage(self, site):
        match site:
            case 1:
                head = self.head_1
                body = self.body_1 
            case 2:
                head = self.head_2
                body = self.body_2
            case _:
                head = self.head_1
                body = self.body_1

        return textklassifizierung_controller.template.base.call_base(head, body)