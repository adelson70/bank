class Account():

    def __init__(self, id, cpf, cc, senha):
        self.id = id
        self.cpf = cpf
        self.saldo = 0
        self.conta_corrente = cc
        self.password = senha

    def enviar_dinheiro(self, quantia):
        if quantia > self.saldo:
            return 0
        else:
            self.saldo -= quantia
            return True

    def receber_dinheiro(self, quantia):
        self.saldo += quantia

    def sacar_dinheiro(self, quantia):
        if quantia > self.saldo:
            return 0
        else:
            self.saldo -= quantia
            return True

    def alterar_senha(self, nova_senha):
        if nova_senha == self.password:
            return 2
        
        elif len(nova_senha) < 8:
            return 0
        
        else:
            self.password = nova_senha
            return 1