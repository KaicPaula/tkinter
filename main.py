import customtkinter as ctk
import sqlite3
import database as db

# -------------------------- Auxilio da intreface ------------------------------
COR_FUNDO   = "#1a1a2e"
COR_PAINEL  = "#16213e"
COR_BOTAO   = "#0f3460"
COR_ACENTO  = "#e94560"
COR_TEXTO   = "#eaeaea"
COR_SUBTXT  = "#a0a0b0"
COR_ENTRADA = "#0d2137"

def label_titulo(principal, texto):
    return ctk.CTkLabel(principal, text=texto, font=("Consolas", 18, "bold"), text_color=COR_ACENTO)

def label_info(principal, texto):
    return ctk.CTkLabel(principal, text=texto, font=("Consolas", 11), text_color=COR_SUBTXT)

def entrada(principal, placeholder="", show=""):
    return ctk.CTkEntry(principal, placeholder_text=placeholder, show=show,
                        font=("Consolas", 13), fg_color=COR_ENTRADA,
                        border_color=COR_BOTAO, text_color=COR_TEXTO, width=280)

def botao(principal, texto, comando, cor=None, largura=200):
    return ctk.CTkButton(principal, text=texto, command=comando,
                         fg_color=cor or COR_BOTAO, hover_color=COR_ACENTO,
                         font=("Consolas", 13, "bold"), width=largura, corner_radius=6)

def separador(principal):
    ctk.CTkLabel(principal, text="─"*40, text_color=COR_BOTAO, font=("Consolas", 10)).pack(pady=2)

def limpar_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def msg_status(label, texto, erro=False):
    cor = COR_ACENTO if erro else "#4caf50"
    label.configure(text=texto, text_color=cor)

# ========================= Janela principal =================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Veículos")
        self.geometry("580x500")
        self.configure(fg_color=COR_FUNDO)
        self.resizable(True, True)
        self.login_atual = None
        self.cargo_atual = None
        self._mostrar_login()

    # ---------------- Login ---------------
    def _mostrar_login(self):
        limpar_frame(self)
        self.geometry("580x500")
        frame = ctk.CTkFrame(self, fg_color=COR_PAINEL, corner_radius=12)
        frame.pack(expand=True, padx=60, pady=60, fill="both")

        label_titulo(frame, "🚗  Sistema de Veículos").pack(pady=(30, 5))
        label_info(frame, "Faça login para continuar").pack(pady=(0, 20))
        separador(frame)

        self.e_nome  = entrada(frame, "Nome de usuário")
        self.e_nome.pack(pady=8)
        self.e_senha = entrada(frame, "Senha", show="*")
        self.e_senha.pack(pady=8)

        self.lbl_login_erro = label_info(frame, "")
        self.lbl_login_erro.pack(pady=4)

        botao(frame, "Entrar", self._validar_login).pack(pady=12)

    def _validar_login(self):
        nome  = self.e_nome.get().strip().lower()
        senha = self.e_senha.get().strip()
        resultado = db.consultar_login(nome, senha)

        if resultado is None:
            msg_status(self.lbl_login_erro, "Usuário não encontrado", erro=True)
        elif resultado is False:
            msg_status(self.lbl_login_erro, "Senha incorreta", erro=True)
        elif resultado is True:
            self.login_atual = nome
            self.cargo_atual = db.get_cargo_texto(nome)

            if db.consultar_cargo(nome):
                self._mostrar_gerencial()
            else:
                self._mostrar_vendedor()

    # --------------- Menu gerencial ------------------
    def _mostrar_gerencial(self):
        limpar_frame(self)
        self.geometry("680x560")

        topo = ctk.CTkFrame(self, fg_color=COR_PAINEL, height=50, corner_radius=0)
        topo.pack(fill="x")
        label_titulo(topo, f"  {self.login_atual}  ({self.cargo_atual})").pack(side="left", padx=15, pady=10)
        botao(topo, "Sair", self._mostrar_login, cor="#3a3a5c", largura=80).pack(side="right", padx=15, pady=8)

        corpo = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=15, pady=10)

        col_btns = ctk.CTkFrame(corpo, fg_color=COR_PAINEL, width=200, corner_radius=10)
        col_btns.pack(side="left", fill="y", padx=(0, 10))
        col_btns.pack_propagate(False)

        self.area_conteudo = ctk.CTkFrame(corpo, fg_color=COR_PAINEL, corner_radius=10)
        self.area_conteudo.pack(side="left", fill="both", expand=True)

        label_info(col_btns, "  Menu").pack(pady=(15, 5), anchor="w")
        separador(col_btns)

        opcoes = [
            ("Adicionar Veículo",     self._tela_adicionar_veiculo),
            ("Remover Veículo",       self._tela_remover_veiculo),
            ("Todos os Veículos",     self._tela_todos_veiculos),
            ("Cadastrar Funcionário", self._tela_cadastrar_func),
            ("Remover Funcionário",   self._tela_remover_func),
            ("Todos Funcionários",    self._tela_todos_funcionarios),
            ("Ganhos e Lucro",        self._tela_ganhos_gerencial),
        ]
        for texto, cmd in opcoes:
            botao(col_btns, texto, cmd, largura=180).pack(pady=4, padx=10)

    def _limpar_conteudo(self):
        limpar_frame(self.area_conteudo)

    # -------------- Adicionar Veiculo ---------------
    def _tela_adicionar_veiculo(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Adicionar Veículo").pack(pady=(15, 5))
        separador(f)

        campos = {}
        specs = [
            ("nome",   "Nome do veículo"),
            ("cor",    "Cor"),
            ("ano",    "Ano"),
            ("fipe",   "Valor FIPE (R$)"),
            ("compra", "Valor de compra / cliente (R$)"),
            ("comiss", "Comissão do vendedor (R$)"),
        ]
        for key, placeholder in specs:
            e = entrada(f, placeholder)
            e.pack(pady=4)
            campos[key] = e

        lbl = label_info(f, "")
        lbl.pack(pady=4)

        def salvar():
            try:
                nome   = campos["nome"].get().strip().lower()
                cor    = campos["cor"].get().strip().lower()
                ano    = campos["ano"].get().strip()
                fipe   = float(campos["fipe"].get())
                compra = float(campos["compra"].get())
                comiss = float(campos["comiss"].get())
                if not nome or not cor or not ano:
                    raise ValueError("Preencha todos os campos de texto")
                veiculo = db.NovoVeiculo(nome, cor, ano, fipe, compra, comiss, 'disponivel')
                db.salvar_veiculo(veiculo.nome, veiculo.cor, veiculo.ano,
                               veiculo.valor_fipe, veiculo.valor_compra_ou_cliente, veiculo.comissao_sugerida)
                msg_status(lbl, "Veículo adicionado com sucesso!")
                for e in campos.values():
                    e.delete(0, "end")
            except ValueError as err:
                msg_status(lbl, f"Erro: {err}", erro=True)

        botao(f, "Salvar Veículo", salvar).pack(pady=10)

    # ---------- Remover Veiculo ------------------
    def _tela_remover_veiculo(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Remover Veículo").pack(pady=(15, 5))
        separador(f)
        label_info(f, "Consulte 'Todos os Veículos' para ver os IDs").pack(pady=2)
        e_id = entrada(f, "ID do veículo")
        e_id.pack(pady=8)

        lbl_dados  = label_info(f, "")
        lbl_dados.pack(pady=4)
        lbl_status = label_info(f, "")
        lbl_status.pack(pady=4)

        frame_confirm = ctk.CTkFrame(f, fg_color="transparent")
        frame_confirm.pack()

        def buscar():
            limpar_frame(frame_confirm)
            lbl_dados.configure(text="")
            lbl_status.configure(text="")
            try:
                id_v = int(e_id.get())
            except ValueError:
                msg_status(lbl_status, "Digite um ID válido", erro=True)
                return
            v = db.buscar_veiculo_por_id(id_v)
            if v is None:
                msg_status(lbl_status, "Veículo não encontrado", erro=True)
                return
            lbl_dados.configure(
                text=f"ID: {v[0]}  |  {v[1]}  |  {v[2]}  |  {v[3]}  |  R${v[4]:,.2f}  |  Status: {v[7]}",
                text_color=COR_TEXTO)
            def confirmar():
                db.deletar_veiculo(id_v)
                msg_status(lbl_status, "Veículo removido com sucesso!")
                lbl_dados.configure(text="")
                limpar_frame(frame_confirm)
                e_id.delete(0, "end")
            botao(frame_confirm, "Confirmar Remoção", confirmar, cor=COR_ACENTO, largura=200).pack(side="left", padx=5)
            botao(frame_confirm, "Cancelar", lambda: limpar_frame(frame_confirm), largura=120).pack(side="left", padx=5)

        botao(f, "Buscar", buscar).pack(pady=6)

    # ---------- Todos os Veiculos --------------
    def _tela_todos_veiculos(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Todos os Veículos").pack(pady=(15, 5))
        separador(f)

        scroll = ctk.CTkScrollableFrame(f, fg_color=COR_ENTRADA, corner_radius=8)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        veiculos = db.listar_veiculos(apenas_disponiveis=False)
        if not veiculos:
            label_info(scroll, "Nenhum veículo cadastrado").pack(pady=10)
            return
        for v in veiculos:
            cor_status = "#4caf50" if v[7] == "disponivel" else COR_ACENTO
            bloco = ctk.CTkFrame(scroll, fg_color=COR_PAINEL, corner_radius=6)
            bloco.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(bloco, text=f"ID: {v[0]}  |  {v[1].upper()}  |  {v[2]}  |  {v[3]}",
                         font=("Consolas", 12, "bold"), text_color=COR_TEXTO).pack(anchor="w", padx=10, pady=(6,0))
            ctk.CTkLabel(bloco, text=f"FIPE: R${v[4]:,.2f}  |  Compra/Cliente: R${v[5]:,.2f}  |  Comissão: R${v[6]:,.2f}",
                         font=("Consolas", 11), text_color=COR_SUBTXT).pack(anchor="w", padx=10)
            ctk.CTkLabel(bloco, text=f"Status: {v[7]}",
                         font=("Consolas", 11, "bold"), text_color=cor_status).pack(anchor="w", padx=10, pady=(0,6))

    # ---------- Cadastrar Funcionario ------------------
    def _tela_cadastrar_func(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Cadastrar Funcionário").pack(pady=(15, 5))
        separador(f)

        e_nome  = entrada(f, "Nome do funcionário")
        e_nome.pack(pady=6)
        e_senha = entrada(f, "Senha")
        e_senha.pack(pady=6)

        var_cargo = ctk.StringVar(value="vendedor")
        frame_radio = ctk.CTkFrame(f, fg_color="transparent")
        frame_radio.pack(pady=6)
        ctk.CTkRadioButton(frame_radio, text="Vendedor", variable=var_cargo, value="vendedor",
                           font=("Consolas", 12), text_color=COR_TEXTO).pack(side="left", padx=15)
        ctk.CTkRadioButton(frame_radio, text="Gerente",  variable=var_cargo, value="gerente",
                           font=("Consolas", 12), text_color=COR_TEXTO).pack(side="left", padx=15)

        lbl = label_info(f, "")
        lbl.pack(pady=4)

        def salvar():
            nome  = e_nome.get().strip().lower()
            senha = e_senha.get().strip()
            cargo = var_cargo.get()
            if not nome or not senha:
                msg_status(lbl, "Preencha nome e senha", erro=True)
                return
            funcionario = db.NovoFuncionario(nome, senha, cargo)
            funcionario.salvar_funcionario_db()
            msg_status(lbl, f"Funcionário '{nome}' cadastrado como {cargo}!")
            e_nome.delete(0, "end")
            e_senha.delete(0, "end")

        botao(f, "Cadastrar", salvar).pack(pady=10)

    # ---------- Remover Funcionario ----------------
    def _tela_remover_func(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Remover Funcionário").pack(pady=(15, 5))
        separador(f)

        e_id = entrada(f, "ID do funcionário")
        e_id.pack(pady=8)

        lbl_dados  = label_info(f, "")
        lbl_dados.pack(pady=4)
        lbl_status = label_info(f, "")
        lbl_status.pack(pady=4)

        frame_confirm = ctk.CTkFrame(f, fg_color="transparent")
        frame_confirm.pack()

        def buscar():
            limpar_frame(frame_confirm)
            lbl_dados.configure(text="")
            lbl_status.configure(text="")
            try:
                id_f = int(e_id.get())
            except ValueError:
                msg_status(lbl_status, "Digite um ID válido", erro=True)
                return
            func = db.buscar_funcionario_por_id(id_f)
            if func is None:
                msg_status(lbl_status, "Funcionário não encontrado", erro=True)
                return
            lbl_dados.configure(text=f"ID: {func[0]}  |  {func[1]}  |  {func[2]}", text_color=COR_TEXTO)
            def confirmar():
                db.deletar_funcionario(id_f)
                msg_status(lbl_status, "Funcionário removido!")
                lbl_dados.configure(text="")
                limpar_frame(frame_confirm)
                e_id.delete(0, "end")
            botao(frame_confirm, "Confirmar Remoção", confirmar, cor=COR_ACENTO, largura=200).pack(side="left", padx=5)
            botao(frame_confirm, "Cancelar", lambda: limpar_frame(frame_confirm), largura=120).pack(side="left", padx=5)

        botao(f, "Buscar", buscar).pack(pady=6)

    # ---------- Todos Funcionarios -----------------
    def _tela_todos_funcionarios(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Todos os Funcionários").pack(pady=(15, 5))
        separador(f)

        scroll = ctk.CTkScrollableFrame(f, fg_color=COR_ENTRADA, corner_radius=8)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        funcs = db.listar_funcionarios()
        if not funcs:
            label_info(scroll, "Nenhum funcionário cadastrado").pack(pady=10)
            return
        for func in funcs:
            bloco = ctk.CTkFrame(scroll, fg_color=COR_PAINEL, corner_radius=6)
            bloco.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(bloco, text=f"ID: {func[0]}  |  {func[1].upper()}  |  Cargo: {func[2]}",
                         font=("Consolas", 12), text_color=COR_TEXTO).pack(anchor="w", padx=10, pady=8)

    # ---------- Ganhos Gerencial --------------
    def _tela_ganhos_gerencial(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Ganhos e Lucro").pack(pady=(15, 5))
        separador(f)

        scroll = ctk.CTkScrollableFrame(f, fg_color=COR_ENTRADA, corner_radius=8)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        dados = db.ganhos_todos()
        if not dados:
            label_info(scroll, "Nenhuma venda registrada").pack(pady=10)
            return
        for d in dados:
            nome_func, total, qtd = d
            bloco = ctk.CTkFrame(scroll, fg_color=COR_PAINEL, corner_radius=6)
            bloco.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(bloco, text=f"Funcionário: {nome_func.upper()}",
                         font=("Consolas", 12, "bold"), text_color=COR_TEXTO).pack(anchor="w", padx=10, pady=(8,0))
            ctk.CTkLabel(bloco, text=f"Total vendido: R${total:,.2f}  |  Qtd de vendas: {qtd}",
                         font=("Consolas", 11), text_color=COR_SUBTXT).pack(anchor="w", padx=10, pady=(0,8))

    # -------------- Vendedor -----------------
    def _mostrar_vendedor(self):
        limpar_frame(self)
        self.geometry("680x560")

        topo = ctk.CTkFrame(self, fg_color=COR_PAINEL, height=50, corner_radius=0)
        topo.pack(fill="x")
        label_titulo(topo, f"  {self.login_atual}  ({self.cargo_atual})").pack(side="left", padx=15, pady=10)
        botao(topo, "Sair", self._mostrar_login, cor="#3a3a5c", largura=80).pack(side="right", padx=15, pady=8)

        corpo = ctk.CTkFrame(self, fg_color=COR_FUNDO)
        corpo.pack(fill="both", expand=True, padx=15, pady=10)

        col_btns = ctk.CTkFrame(corpo, fg_color=COR_PAINEL, width=200, corner_radius=10)
        col_btns.pack(side="left", fill="y", padx=(0, 10))
        col_btns.pack_propagate(False)

        self.area_conteudo = ctk.CTkFrame(corpo, fg_color=COR_PAINEL, corner_radius=10)
        self.area_conteudo.pack(side="left", fill="both", expand=True)

        label_info(col_btns, "  Menu").pack(pady=(15, 5), anchor="w")
        separador(col_btns)

        opcoes = [
            ("Veículos Disponíveis", self._tela_veiculos_disponiveis),
            ("Realizar Venda",       self._tela_realizar_venda),
            ("Meus Ganhos",          self._tela_ganhos_vendedor),
            ("Mudar Senha",          self._tela_mudar_senha),
        ]
        for texto, cmd in opcoes:
            botao(col_btns, texto, cmd, largura=180).pack(pady=4, padx=10)

    # ------------ Veiculos disponíveis (vendedor) ----------------
    def _tela_veiculos_disponiveis(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Veículos Disponíveis").pack(pady=(15, 5))
        separador(f)

        scroll = ctk.CTkScrollableFrame(f, fg_color=COR_ENTRADA, corner_radius=8)
        scroll.pack(fill="both", expand=True, padx=10, pady=10)

        veiculos = db.listar_veiculos(apenas_disponiveis=True)
        if not veiculos:
            label_info(scroll, "Nenhum veículo disponível no momento").pack(pady=10)
            return
        for v in veiculos:
            bloco = ctk.CTkFrame(scroll, fg_color=COR_PAINEL, corner_radius=6)
            bloco.pack(fill="x", pady=4, padx=4)
            ctk.CTkLabel(bloco, text=f"ID: {v[0]}  |  {v[1].upper()}  |  {v[2]}  |  {v[3]}",
                         font=("Consolas", 12, "bold"), text_color=COR_TEXTO).pack(anchor="w", padx=10, pady=(6,0))
            ctk.CTkLabel(bloco, text=f"FIPE: R${v[4]:,.2f}  |  Compra/Cliente: R${v[5]:,.2f}  |  Comissão: R${v[6]:,.2f}",
                         font=("Consolas", 11), text_color=COR_SUBTXT).pack(anchor="w", padx=10, pady=(0,6))

    # ---------------- Realizar Venda ------------------
    def _tela_realizar_venda(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Realizar Venda").pack(pady=(15, 5))
        separador(f)
        label_info(f, "Consulte 'Veículos Disponíveis' para ver os IDs").pack(pady=2)

        e_id = entrada(f, "ID do veículo")
        e_id.pack(pady=8)

        lbl_dados  = label_info(f, "")
        lbl_dados.pack(pady=4)

        frame_venda = ctk.CTkFrame(f, fg_color="transparent")
        frame_venda.pack(pady=4)

        lbl_status = label_info(f, "")
        lbl_status.pack(pady=4)

        def buscar():
            limpar_frame(frame_venda)
            lbl_dados.configure(text="")
            lbl_status.configure(text="")
            try:
                id_v = int(e_id.get())
            except ValueError:
                msg_status(lbl_status, "Digite um ID válido", erro=True)
                return
            v = db.buscar_veiculo_por_id(id_v)
            if v is None:
                msg_status(lbl_status, "Veículo não encontrado", erro=True)
                return
            if v[7] == 'indisponivel':
                msg_status(lbl_status, "Veículo já vendido", erro=True)
                return

            valor_minimo = round(v[6] + (v[4] * 1.08), 2)
            lbl_dados.configure(
                text=f"ID:{v[0]}  {v[1].upper()}  {v[2]}  {v[3]}\nFIPE: R${v[4]:,.2f}  |  Compra/Cliente: R${v[5]:,.2f}\nValor mínimo de venda: R${valor_minimo:,.2f}",
                text_color=COR_TEXTO)

            label_info(frame_venda, "Valor final de venda (R$):").pack()
            e_valor = entrada(frame_venda, f"Mínimo: R${valor_minimo:,.2f}")
            e_valor.pack(pady=6)

            def confirmar_venda():
                try:
                    valor_final = float(e_valor.get())
                except ValueError:
                    msg_status(lbl_status, "Digite um valor válido", erro=True)
                    return
                if valor_final < valor_minimo:
                    msg_status(lbl_status, f"Valor mínimo: R${valor_minimo:,.2f}", erro=True)
                    return
                db.realizar_venda_db(id_v, self.login_atual, valor_final)
                msg_status(lbl_status, f"Venda realizada! R${valor_final:,.2f}")
                lbl_dados.configure(text="")
                limpar_frame(frame_venda)
                e_id.delete(0, "end")

            botao(frame_venda, "Confirmar Venda", confirmar_venda, cor="#2e7d32").pack(pady=4)

        botao(f, "Buscar Veículo", buscar).pack(pady=6)

    # ------------- Ganhos do Vendedor -----------------
    def _tela_ganhos_vendedor(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Meus Ganhos").pack(pady=(15, 5))
        separador(f)

        dados = db.ganhos_vendedor(self.login_atual)
        if dados is None:
            label_info(f, "Nenhuma venda registrada ainda").pack(pady=20)
            return
        nome_func, total, qtd = dados
        bloco = ctk.CTkFrame(f, fg_color=COR_ENTRADA, corner_radius=8)
        bloco.pack(padx=20, pady=20, fill="x")
        ctk.CTkLabel(bloco, text=nome_func.upper(), font=("Consolas", 16, "bold"), text_color=COR_ACENTO).pack(pady=(15,5))
        ctk.CTkLabel(bloco, text=f"Total vendido:   R$ {total:,.2f}", font=("Consolas", 14), text_color=COR_TEXTO).pack(pady=4)
        ctk.CTkLabel(bloco, text=f"Qtd de vendas:  {qtd}", font=("Consolas", 14), text_color=COR_TEXTO).pack(pady=(4,15))

    # ------------- Mudar Senha -----------------
    def _tela_mudar_senha(self):
        self._limpar_conteudo()
        f = self.area_conteudo
        label_titulo(f, "Mudar Senha").pack(pady=(15, 5))
        separador(f)

        e_atual = entrada(f, "Senha atual", show="*")
        e_atual.pack(pady=6)
        e_nova  = entrada(f, "Nova senha", show="*")
        e_nova.pack(pady=6)
        e_conf  = entrada(f, "Confirmar nova senha", show="*")
        e_conf.pack(pady=6)

        lbl = label_info(f, "")
        lbl.pack(pady=4)

        def salvar():
            senha_atual_bd = db.verificar_senha_atual(self.login_atual)
            if e_atual.get() != senha_atual_bd:
                msg_status(lbl, "Senha atual incorreta", erro=True)
                return
            if e_nova.get() != e_conf.get():
                msg_status(lbl, "As senhas novas não coincidem", erro=True)
                return
            if e_nova.get() == e_atual.get():
                msg_status(lbl, "A nova senha é igual à atual", erro=True)
                return
            if not e_nova.get():
                msg_status(lbl, "Digite uma nova senha", erro=True)
                return
            db.alterar_senha_db(self.login_atual, e_nova.get())
            msg_status(lbl, "Senha alterada com sucesso!")
            for e in [e_atual, e_nova, e_conf]:
                e.delete(0, "end")

        botao(f, "Alterar Senha", salvar).pack(pady=10)


# --------------------------- Inicialização --------------------------------
if __name__ == "__main__":
    db.inicializar_banco()   # usa db.inicializar_banco() do seu database.py
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = App()
    app.mainloop()