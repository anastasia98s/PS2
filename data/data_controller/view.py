import data.data_controller.template.base
import data.data_controller.template.page_1
import data.data_controller.template.page_2

class View:
    def __init__(self):
        self.head_1 = data.data_controller.template.page_1.head
        self.head_2 = data.data_controller.template.page_2.head
        self.body_1 = data.data_controller.template.page_1.body
        self.body_2 = data.data_controller.template.page_2.body

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

        return data.data_controller.template.base.call_base(head, body)