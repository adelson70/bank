# Importando modulos
# from user import Pessoa
# from bank_account import Account
import sqlite3
from os import system as sys
from time import sleep

def esperar(tempo=3):
    sleep(tempo)

def limpar_console():
    sys('cls')
limpar_console()

def conexao_banco():
    conexao = sqlite3.connect('bank.db')
    cursor = conexao.cursor()

# CRIA A TABELA PESSOA SE NÃO EXISTIR
    cursor.execute("""
CREATE TABLE IF NOT EXISTS pessoa(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nome VARCHAR(50),
                          cpf VARCHAR(11),
                          data_nascimento DATE,
                          salario DECIMAL                          
)
""")
    conexao.commit()

# CRIA A TABELA CONTA SE NÃO EXISTIR
    cursor.execute("""
CREATE TABLE IF NOT EXISTS conta(
                      id INTEGER PRIMARY KEY,
                      cpf VARCHAR(11),
                      saldo DECIMAL DEFAULT 0,
                      cc VARCHAR(4),
                      senha VARCHAR(8),
                      FOREIGN KEY (id) REFERENCES pessoa(id),
                      FOREIGN KEY (cpf) REFERENCES pessoa(cpf)
)
""")
    conexao.commit()
    saida = (conexao, cursor)

    return saida
conexao_banco()

# FUNÇÃO PARA CRIAR USUARIO
def criar_usuario():
    limpar_console()
    nome = input('Digite seu nome completo: ')
    cpf = input('Digite apenas o números do seu cpf: ')
    dia_nascimento = int(input('Digite o dia do seu nascimento: '))
    mes_nascimento = int(input('Digite o mês do seu nascimento: '))
    ano_nascimento = int(input('Digite o ano do seu nascimento: '))
    data_nascimento = f'{dia_nascimento:02d}/{mes_nascimento:02d}/{ano_nascimento}'
    salario = float(input('Digite seu salario bruto: '))

    conexao, cursor = conexao_banco()

    cursor.execute(f"""INSERT INTO pessoa (nome, cpf, data_nascimento, salario) 
                   VALUES ('{nome}','{cpf}','{data_nascimento}',{salario})""")
    
    conexao.commit()

    print(f'CPF: {cpf} vinculado ao banco com sucesso!')
    esperar()
    limpar_console()

# FUNÇÃO PARA CRIAR CONTA
def criar_conta():
    limpar_console()
    cpf = input('Digite o CPF cadastrado: ')
    conexao, cursor = conexao_banco()
    cursor.execute('SELECT cpf FROM pessoa WHERE cpf=?',(cpf,))
    
    try:
        result = cursor.fetchone()[0]
        
        if result:
            cursor.execute('SELECT id FROM pessoa WHERE cpf=?',(cpf,))
            conta = cursor.fetchone()[0]
            cc = f'000{str(conta)}-1'
            senha = input('Crie sua senha: ')

            cursor.execute(f"""INSERT INTO conta (cpf, cc, senha)
                        VALUES('{cpf}','{cc}','{senha}')""")
            
        conexao.commit()

        print(f'CPF: {cpf} vinculado a conta: {cc}')
        esperar()
        limpar_console()

    except:
        limpar_console()
        print('CPF não cadastrado no banco!')
        esperar()

def depositar():
    ...

def sacar():
    ...

def transferir():
    ...

# FUNÇÃO PARA ACESSAR A CONTA
def acessar_conta():
    limpar_console()
    id = input('Digite o ID da sua conta: ')
    cpf = input('Digite o CPF vinculado a conta: ')
    senha = input('Digite a senha da sua conta: ')

    conexao, cursor = conexao_banco()
    try:
        cursor.execute("""SELECT pessoa.nome, pessoa.salario, conta.cpf, conta.saldo, conta.cc 
                       FROM conta
                       JOIN pessoa ON conta.id = pessoa.id 
                       WHERE conta.id=? AND conta.cpf=? AND conta.senha=?""",(id, cpf, senha))
        result = cursor.fetchall()[0]

        nome_usuario, salario_usuario, cpf_usuario, saldo_usuario, cc_usuario = result

        limpar_console()
        while True:
            limpar_console()
            msg = (f"""
Bem vindo {nome_usuario.title()}
CPF: {cpf_usuario}
CC: {cc_usuario}

Saldo: R${saldo_usuario:.2f}

[1] - Depositar
[2] - Transferir
[3] - Sacar
[0] - Sair

Digite: """)
            opcao = input(msg)

            if opcao == '0':
                break
            elif opcao == '1':
                depositar()
            elif opcao == '2':
                transferir()
            elif opcao == '3':
                sacar()

    except:
        limpar_console()
        print('Conta não encontrada!')
        esperar()
        limpar_console()

def main():
    while True:
        limpar_console()
        msg = """
[1] - Acessar Conta
[2] - Cadastrar CPF
[3] - Criar Conta
[0] - Sair

Digite: """

        opcoes = ['1','2','3','0']

        opcao = input(msg)

        if opcao in opcoes:
            if opcao == '0':
                break

            elif opcao == '1':
                acessar_conta()

            elif opcao == '2':
                criar_usuario()

            elif opcao == '3':
                criar_conta()

main()