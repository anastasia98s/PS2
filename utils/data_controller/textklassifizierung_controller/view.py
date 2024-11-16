import utils.data_controller.textklassifizierung_controller.template.base
import utils.data_controller.textklassifizierung_controller.template.page_1
import utils.data_controller.textklassifizierung_controller.template.page_2

class View:
    def __init__(self):
        self.head_1 = utils.data_controller.textklassifizierung_controller.template.page_1.head
        self.head_2 = utils.data_controller.textklassifizierung_controller.template.page_2.head
        self.body_1 = utils.data_controller.textklassifizierung_controller.template.page_1.body
        self.body_2 = utils.data_controller.textklassifizierung_controller.template.page_2.body

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

        return utils.data_controller.textklassifizierung_controller.template.base.call_base(head, body)