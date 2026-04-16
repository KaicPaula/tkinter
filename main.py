import customtkinter as ctk
import database as db
from time import sleep


db.inicializar_banco()

# dados manual:
# kaic = db.NovoFuncionario("kaic", "1122", "dono")
# kaic.salvar_funcionario_db()


# ------------------------------------------

# def funcao_frame():
#     verificar_texto = entry_teste.get()
#     if verificar_texto in banco:
#         pagina_login.pack_forget()
#         pagina_sistema.pack()
#     else:
#         label_erro.configure(text="Nome invalido")

def validar_login():
    nome_login = entrada_nome.get() 
    senha_login = entrada_senha.get()
    retorno_consulta = db.consultar_login(nome_login, senha_login)
    if retorno_consulta == None:
        label_pagina_login.configure(text="Nome invalido")
    elif retorno_consulta == False:
        label_pagina_login.configure(text="Senha invalida")
    elif retorno_consulta == True:
        sleep(1)
        pagina_login.pack_forget()
        pagina_sistema.pack()
        
        
        
def copiar_nome(nome):
    label_nome.configure(text=nome)
    


janela = ctk.CTk()
janela.title("Pagina de login")
janela.geometry("400x300")

pagina_login = ctk.CTkFrame(janela)
pagina_login.pack()

label = ctk.CTkLabel(pagina_login, text="Login")
label.pack()
entrada_nome = ctk.CTkEntry(pagina_login,placeholder_text="Nome de login")
entrada_nome.pack(pady=10)
entrada_senha = ctk.CTkEntry(pagina_login, placeholder_text="Senha", show="*")
entrada_senha.pack(pady=10)
botao_confirmar_login = ctk.CTkButton(pagina_login, text="Acessar", command=validar_login)
botao_confirmar_login.pack()
label_pagina_login = ctk.CTkLabel(pagina_login, text="")
label_pagina_login.pack(pady=10)

# ----------------------- JANELA SISTEMA ---------------------------------
pagina_sistema = ctk.CTkFrame(janela)
ctk.CTkLabel(pagina_sistema, text="Bem vindo ao sistema").pack()


# scroll = ctk.CTkScrollableFrame(pagina_sistema, width=200, height=150) # frame scrollavel
# scroll.pack(padx=10, pady=10)

# for i in banco:
#     nome_atual = i
#     ctk.CTkLabel(scroll, text=f"nome: {i}").pack() # widget dentro do escrolavel
#     botao_nome = ctk.CTkButton(scroll,text="Copiar Nome", command= lambda nome=i: copiar_nome(nome))
#     botao_nome.pack()
"""
Lambda faz a pausa do loop pra poder criar um botao independente pra cada nome,
pra q cada botao possa enviar o nome (nesse caso) para a funçao poder tratar o dado.
"""
    
label_nome = ctk.CTkLabel(pagina_sistema, text="")
label_nome.pack()


janela.mainloop()
