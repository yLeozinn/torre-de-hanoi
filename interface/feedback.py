"""Mensagens de feedback exibidas pela interface."""


class Feedback:
    def __init__(self):
        self.mensagem = "Clique em uma torre para selecionar um disco."
        self.tipo = "info"

    def set_info(self, mensagem):
        self.mensagem = mensagem
        self.tipo = "info"

    def set_error(self, mensagem):
        self.mensagem = mensagem
        self.tipo = "erro"

    def set_success(self, mensagem):
        self.mensagem = mensagem
        self.tipo = "sucesso"
