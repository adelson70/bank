class Pessoa():

    def __init__(self, nome, cpf, data_nascimento, salario):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.salario = salario
        self.id = None

    def alterar_salario(self, novo_salario):
        self.salario = novo_salario
        return novo_salario