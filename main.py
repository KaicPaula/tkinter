import customtkinter as ctk
from database import inicializar_banco


inicializar_banco()

banco = [
    ("kaic"),
    ("paula"),
    ("duda")
]

def funcao_frame():
    verificar_texto = entry_teste.get()
    if verificar_texto in banco:
        pagina_login.pack_forget()
        pagina_sistema.pack()
    else:
        label_erro.configure(text="Nome invalido")
        
        
def copiar_nome(nome):
    label_nome.configure(text=nome)
    


janela = ctk.CTk()
janela.title("Pagina de login")
janela.geometry("800x600")

pagina_login = ctk.CTkFrame(janela)
pagina_login.pack()

label = ctk.CTkLabel(pagina_login, text="Testando")
label.pack()
entry_teste = ctk.CTkEntry(pagina_login,placeholder_text="Testando")
entry_teste.pack()
botao_frame = ctk.CTkButton(pagina_login, text="Entrar", command=funcao_frame)
botao_frame.pack()
label_erro = ctk.CTkLabel(pagina_login, text=" ")
label_erro.pack()

pagina_sistema = ctk.CTkFrame(janela)
ctk.CTkLabel(pagina_sistema, text="Bem vindo ao sistema").pack()

scroll = ctk.CTkScrollableFrame(pagina_sistema, width=200, height=150) # frame scrollavel
scroll.pack(padx=10, pady=10)

for i in banco:
    nome_atual = i
    ctk.CTkLabel(scroll, text=f"nome: {i}").pack() # widget dentro do escrolavel
    botao_nome = ctk.CTkButton(scroll,text="Copiar Nome", command= lambda nome=i: copiar_nome(nome))
    botao_nome.pack()
"""
Lambda faz a paausa do loop pra poder criar um botao independente pra cada nome,
pra q cada botao possa enviar o nome (nesse caso) para a funçao poder tratar o dado.
"""
    
label_nome = ctk.CTkLabel(pagina_sistema, text="")
label_nome.pack()


janela.mainloop()
