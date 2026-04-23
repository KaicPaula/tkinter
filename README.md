Instale a biblioteca necessária: pip install customtkinter

Certifique-se de que o arquivo database.py está no mesmo diretório.

Execute o arquivo principal: python main.py



🚗 Sistema de Gestão de Veículos
Um sistema de gerenciamento automotivo robusto desenvolvido em Python, utilizando interface gráfica moderna e persistência de dados local. O projeto simula o fluxo de trabalho real de uma concessionária, com níveis de acesso distintos para gerentes e vendedores.

🛠️ Tecnologias Utilizadas
Linguagem: Python 3.

Interface Gráfica: CustomTkinter (para um design moderno e responsivo).

Banco de Dados: SQLite3 (armazenamento local eficiente).

Paradigma: Programação Orientada a Objetos (POO).

🧠 O que foi aprendido e aplicado
O desenvolvimento deste sistema permitiu a prática de conceitos avançados de engenharia de software:

1. Programação Orientada a Objetos (POO)
Encapsulamento e Herança: A classe principal App herda de ctk.CTk, organizando toda a lógica da janela e estados globais (como o usuário logado).

Modularização: Separação clara entre a lógica de interface (main.py) e a lógica de persistência de dados (database.py).

2. Interface Gráfica (GUI)
Gerenciamento de Frames: Uso de funções auxiliares para limpeza e troca dinâmica de conteúdo (limpar_frame), permitindo uma navegação fluida sem abrir múltiplas janelas.

UX/UI: Implementação de feedbacks visuais (mensagens de erro/sucesso coloridas), placeholders e máscaras de senha.

Componentes Customizados: Criação de funções de auxílio para padronizar botões, entradas e títulos, garantindo identidade visual.

3. Banco de Dados e Regras de Negócio
Operações CRUD: Create, Read, Update e Delete aplicados a veículos e funcionários.

Lógica de Acesso (Níveis de Permissão): Implementação de restrições onde apenas usuários com cargo "gerente" acessam funções administrativas e relatórios de lucro.

Cálculos Dinâmicos: Implementação de regra de negócio para cálculo de "valor mínimo de venda" baseado na Tabela FIPE, valor de compra e comissões.

🚀 Funcionalidades Principais
Painel Administrativo: Cadastro e remoção de veículos/funcionários e visualização de faturamento total.

Painel do Vendedor: Consulta de estoque disponível, realização de vendas com validação de valor mínimo e acompanhamento de metas pessoais.

Segurança: Sistema de login funcional e opção de alteração de senha pelo próprio usuário.
