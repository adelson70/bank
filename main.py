# Importando modulos
from user import Pessoa
from bank_account import Account
import sqlite3

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
                      saldo DECIMAL,
                      cc VARCHAR(4),
                      senha VARCHAR(8),
                      FOREIGN KEY (id) REFERENCES pessoa(id),
                      FOREIGN KEY (cpf) REFERENCES pessoa(cpf)
)
""")
    conexao.commit()
    saida = (conexao, cursor)

    return saida

def carregar_usuario(cpf):
    _, cursor = conexao_banco()

    cursor.execute('SELECT * FROM pessoa WHERE cpf=?', (cpf,))
    result = cursor.fetchone()

    if result:
        return Pessoa(*result)
    else:
        print('Não encontrado!')
        return 0

def carregar_conta(cc, cpf, senha):
    _, cursor = conexao_banco()

    cursor.execute('SELECT * FROM conta WHERE cc=? AND cpf=? AND senha=?',(cc, cpf, senha,))
    result = cursor.fetchone()

    if result:
        return Account(*result)
    else:
        print('Conta não encontrada')
        return 0