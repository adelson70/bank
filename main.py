# Importando modulos
from user import Pessoa
from bank_account import Account
import sqlite3

def conexao():
    conexao_pessoa = sqlite3.connect('pessoa_bank.db')
    conexao_cc = sqlite3.connect('conta_bank.db')
    cursor_pessoa = conexao_pessoa.cursor()
    cursor_cc = conexao_cc.cursor()

    cursor_pessoa.execute("""
CREATE TABLE IF NOT EXISTS pessoa(
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          nome VARCHAR(50),
                          cpf VARCHAR(11),
                          data_nascimento DATE,
                          salario DECIMAL                          
)
""")
    conexao_pessoa.commit()

    cursor_cc.execute("""
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
    conexao_cc.commit()

conexao()