# Importando modulos
# from user import Pessoa
# from bank_account import Account
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

# FUNÇÃO PARA CRIAR CONTA
def criar_conta():
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

    except:
        print('CPF não cadastrado no banco!')

