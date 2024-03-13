# Importando modulos
from user import Pessoa
from bank_account import Account
import sqlite3

def conexao():
    conexao = sqlite3.connect('bank.db')
    cursor = conexao.cursor()

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

conexao()