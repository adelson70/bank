# Importando modulos
from user import Pessoa
from bank_account import Account
import sqlite3
import tkinter as tk

# FONTES PERSONALIZADAS
fonte_titulo = ('Helvica',16)
fonte_labels = ('Helvica',14)
fonte_botao = ('Helvica',15)

# GUI DA TELA INICIAL
def tela_inicial():
    global fonte_titulo
    global fonte_botao
    global fonte_labels
    global janela

    janela = tk.Tk()
    janela.title('Menu Inicial')
    janela.geometry('300x210')
    janela.resizable(width=False, height=False)

    tk.Label(janela, text='Bem-vindo ao Banco Cobra', font=fonte_titulo).pack(pady=5)

    tk.Label(janela).pack(pady=2)

    # USUARIO JÁ CADASTRADO
    acessar_conta = tk.Button(janela, text='Acessar Conta', font=fonte_botao, command=tela_login)
    acessar_conta.pack(pady=5)

    # NOVO USUARIO
    criar_conta = tk.Button(janela, text='Criar Conta', font=fonte_botao, command=...)
    criar_conta.pack(pady=5)

    janela.mainloop()

def tela_login():
    global fonte_titulo
    global fonte_botao
    global fonte_labels

    for widget in janela.winfo_children():
        widget.destroy()

    janela.title('Area do Usuario')
    janela.geometry('300x210')
    janela.resizable(width=False, height=False)

    tk.Label(janela, text='Area do Usuario', font=fonte_titulo).pack(pady=5)

    tk.Label(janela).pack(pady=2)

    # USUARIO JÁ CADASTRADO
    acessar_conta = tk.Button(janela, text='Acessar Conta', font=fonte_botao, command=...)
    acessar_conta.pack(pady=5)

    # NOVO USUARIO
    criar_conta = tk.Button(janela, text='Criar Conta', font=fonte_botao, command=...)
    criar_conta.pack(pady=5) 

tela_inicial()