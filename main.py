# Importando modulos
# from user import Pessoa
# from bank_account import Account
import sqlite3
from os import system as sys
from time import sleep
from datetime import datetime

# FUNÇÃO PARA CONSULTAR A DATA
def consultar_data():
    data = datetime.now()
    dia = f'{data.day:02}'
    mes = f'{data.month:02}'
    ano = f'{data.year}'

    data_formatada = f'{dia}/{mes}/{ano}'

    return data()

# FUNÇÃO PARA CONSULTAR O HORARIO
def consultar_horario():
    data = datetime.now()
    hora = f'{data.hour:02}'
    minuto = f'{data.minute:02}'
    segundo = f'{data.second:02}'

    horario_formatado = f'{hora}:{minuto}:{segundo}'

    return horario_formatado
    

# FUNÇÃO DE ESPERA
def esperar(tempo=3):
    sleep(tempo)

# FUNÇÃO PARA LIMPAR A TELA DO CONSOLE
def limpar_console():
    sys('cls')
limpar_console()

# FUNÇÃO PARA CRIAR CONEXÃO AO BANCO DE DADOS
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
# CRIA A TABELA DE EXTRATO SE NÃO EXISTIR
    cursor.execute("""
CREATE TABLE IF NOT EXISTS extrato(
                   id INTEGER PRIMARY KEY,
                   data DATE,
                   horario DATETIME,
                   cc VARCHAR(4),
                   cpf VARCHAR(11),
                   operacao VARCHAR(15),
                   valor DECIMAL DEFAULT 0,
                   obs VARCHAR(4),
                   FOREIGN KEY (id) REFERENCES pessoa(id)
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

# FUNÇÃO PARA DEPOSITAR NA CONTA
def depositar(cpf, saldo_atual):
    limpar_console()
    conexao, cursor = conexao_banco()

    try:
        quantia = int(input('Digite a quantia a ser depositada: '))
        while quantia < 0:
            limpar_console()
            quantia = int(input('Valor Invalido! Digite a quantia a ser depositada: '))

        novo_saldo = saldo_atual+quantia

        cursor.execute("""
                       UPDATE conta
                       SET saldo=?
                       WHERE cpf=?""",(novo_saldo, cpf))
        conexao.commit()

        limpar_console()
        print(f'R${quantia:.2f} Depositados com Sucesso!')
        esperar()

    except:
        limpar_console()
        print('Digite apenas números!')
        esperar()

# FUNÇÃO PARA SACAR
def sacar(cpf, saldo_atual):
    limpar_console()
    conexao, cursor = conexao_banco()

    try:
        quantia = int(input('Digite a quantia a ser sacada: '))
        while quantia > saldo_atual:
            limpar_console()
            quantia = int(input('Você não possui essa quantia, digite um novo valor: '))

        novo_saldo = saldo_atual-quantia

        cursor.execute("""
                       UPDATE conta
                       SET saldo=?
                       WHERE cpf=?""",(novo_saldo, cpf))
        conexao.commit()

        limpar_console()
        print(f'R${quantia:.2f} Sacado com Sucesso!')
        esperar()

    except:
        limpar_console()
        print('Digite apenas números!')
        esperar()

# FUNÇÃO PARA TRANSFERIR
def transferir(cpf_envia, saldo_envia):
    limpar_console()
    try:
        cpf_recebe = input('Digite o CPF vinculado a conta que ira receber o dinheiro: ')
        conexao, cursor = conexao_banco()

        cursor.execute("""SELECT pessoa.nome, conta.cpf, conta.saldo 
                       FROM conta 
                       JOIN pessoa ON conta.id = pessoa.id
                       WHERE conta.cpf=?""",(cpf_recebe,))
        
        result = cursor.fetchall()[0]
        pessoa_recebe, _, saldo_recebe = result

        msg = f"Quanto deseja enviar para conta de {pessoa_recebe.title()}? "
        quantia_enviada = int(input(msg))
        
        if quantia_enviada < 0:
            limpar_console()
            print('Digite uma quantia maior que zero!')
            esperar()

        elif quantia_enviada == 0:
            limpar_console('Operação Cancelada')
            esperar()

        elif quantia_enviada > saldo_envia:
            limpar_console()
            print('Você não tem essa quantia para enviar!')
            esperar()

        else:
            novo_saldo_envia = saldo_envia-quantia_enviada
            novo_saldo_recebe = saldo_recebe+quantia_enviada

            cursor.execute("""
                           UPDATE conta
                           SET saldo=?
                           WHERE cpf=?
                           """,(novo_saldo_envia, cpf_envia))
            
            cursor.execute("""
                           UPDATE conta
                           SET saldo=?
                           WHERE cpf=?
                           """,(novo_saldo_recebe, cpf_recebe))
            
            limpar_console()
            print(f'R${quantia_enviada:.2f} enviados para {pessoa_recebe.title()}')
            esperar()

            conexao.commit()

    except ValueError:
        print('Digite Apenas Números!')

    except:
        limpar_console()
        print('CPF não vinculado a nenhuma conta!')
        esperar()


# FUNÇÃO PARA ACESSAR A CONTA
def acessar_conta():
    limpar_console()
    id = input('Digite o ID da sua conta: ')
    cpf = input('Digite o CPF vinculado a conta: ')
    senha = input('Digite a senha da sua conta: ')

    conexao, cursor = conexao_banco()
    try:
        while True:
            limpar_console()
            cursor.execute("""SELECT pessoa.nome, pessoa.salario, conta.cpf, conta.saldo, conta.cc 
                        FROM conta
                        JOIN pessoa ON conta.id = pessoa.id 
                        WHERE conta.id=? AND conta.cpf=? AND conta.senha=?""",(id, cpf, senha))
            result = cursor.fetchall()[0]

            nome_usuario, salario_usuario, cpf_usuario, saldo_usuario, cc_usuario = result

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
                depositar(cpf_usuario, saldo_usuario)

            elif opcao == '2':
                if saldo_usuario > 0:
                    transferir(cpf_usuario, saldo_usuario)
                else:
                    limpar_console()
                    print('Você não tem dinheiro na sua conta! Faça um deposito')
                    esperar()

            elif opcao == '3':
                if saldo_usuario > 0:
                    sacar(cpf_usuario, saldo_usuario)
                else:
                    limpar_console()
                    print('Você não tem dinheiro na sua conta! Faça um deposito')
                    esperar()

    except:
        limpar_console()
        print('Conta não encontrada!')
        esperar()
        limpar_console()

def extrato():

    ...

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
                limpar_console()
                break

            elif opcao == '1':
                acessar_conta()

            elif opcao == '2':
                criar_usuario()

            elif opcao == '3':
                criar_conta()

main()