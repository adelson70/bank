class Account():

    def __init__(self, id, cpf, cc):
        self.id = id
        self.cpf = cpf
        self.saldo = 0
        self.conta_corrente = cc

    def enviar_dinheiro(self, quantia):
        if quantia > self.saldo:
            return 0
        else:
            self.saldo -= quantia

    def receber_dinheiro(self, quantia):
        self.saldo += quantia

    def sacar_dinheiro(self, quantia):
        if quantia > self.saldo:
            return 0
        else:
            self.saldo -= quantia