📊 Aplicativo Controle de Vendas - Hashtag

Um aplicativo mobile/desktop completo desenvolvido em Python utilizando o framework Kivy e integrado ao Firebase (Authentication e Realtime Database) para gerenciamento, lançamento e acompanhamento de vendas em equipe em tempo real.

📱 Sobre o Projeto

O Controle de Vendas permite que vendedores registrem suas transações diárias, acompanhem seu faturamento total, visualizem dados de outros membros da equipe e monitorem o desempenho geral da empresa.

O projeto segue uma arquitetura modular baseada no padrão KV Language, utilizando um layout raiz fixo no main.kv que gerencia a transição entre 9 telas dinâmicas através do ScreenManager.

🛠️ Tecnologias Utilizadas

Python 3.12

Kivy 2.3.1 (Interface gráfica, manipulação de UI e eventos)

Firebase Authentication (Criar conta e Login seguro via e-mail/senha)

Firebase Realtime Database (Armazenamento em nuvem via API REST com a biblioteca requests)

python-dotenv (Gerenciamento seguro da chave de API)


🚀 Arquitetura e Estrutura do App
Desenvolvimento de Aplicativos com Python - Kivy/
├── .venv312/                  # Ambiente virtual do Python 3.12
├── icones/                    # Ativos gráficos (fotos de perfil, ícones de produtos, clientes e fundos)
│   ├── fotos_clientes/
│   ├── fotos_perfil/
│   └── fotos_produtos/
├── kv/                        # Interfaces em KV Language (Subtelas)
│   ├── adicionarvendas.kv     # Formulário de lançamento de vendas
│   ├── adicionarvendedores.kv # Tela para inclusão de novos parceiros por ID
│   ├── ajustespage.kv         # Painel de configurações do usuário
│   ├── homepage.kv            # Tela inicial com histórico de vendas próprias
│   ├── listarvendedores.kv    # Lista da equipe do vendedor
│   ├── loginpage.kv           # Login e cadastro
│   ├── mudarfoto.kv           # Galeria para troca de avatar
│   ├── todasvendas.kv         # Visão geral de vendas de toda a empresa
│   └── vendasoutrovendedor.kv # Detalhes das vendas de um membro específico
├── .env                       # Variáveis de ambiente (API_KEY do Firebase)
├── bannervenda.py             # Card customizado (GridLayout) para renderizar uma venda
├── bannervendedor.py          # Card customizado (FloatLayout) para exibir dados de um vendedor
├── botoes.py                  # Componentes reutilizáveis (LabelButton, ImageButton)
├── main.py                    # Classe principal MainApp, regras de negócio e rotas
├── main.kv                    # Layout Raiz (Header Fixo + ScreenManager com as 9 telas)
├── myfirebase.py              # Módulo de autenticação e comunicação REST com o Firebase
└── telas.py                   # Declaração das classes de tela



⚡ Fluxo de Funcionamento e Navegação
Layout Raiz (main.kv):

Define a cor de fundo padrão (#001824).

Mantém a Foto de Perfil fixa no topo (#foto_perfil).

Utiliza um ScreenManager para alternar entre as 9 telas sem recarregar a interface inteira.

Autenticação (loginpage.kv / myfirebase.py):

Ao fazer login/cadastro, o aplicativo salva o refreshToken localmente em refreshtoken.txt.

A cada inicialização, o token é atualizado automaticamente na API do Google Tokens.

Inclusão de Vendas (adicionarvendas.kv / main.py):

O aplicativo carrega dinamicamente as fotos de clientes e produtos da pasta icones/.

Permite selecionar o cliente, produto, unidade (kg, unidades, litros), valor total e quantidade.

O valor é adicionado à lista do usuário no Firebase e o total acumulado do vendedor é atualizado via PATCH.

Rede de Vendedores (adicionarvendedores.kv / bannervendedor.py):

Cada usuário possui um ID Único de Vendedor sequencial (gerado a partir do nó proximo_id_vendedor).

É possível adicionar outros vendedores à sua equipe informando o ID.

Clicar no banner de um colega abre a tela VendasOutroVendedor, buscando em tempo real as vendas daquele ID específico.

🔒 Configuração de Regras de Segurança no Firebase
No console do Firebase Realtime Database, configure a aba Rules da seguinte forma para garantir o funcionamento das requisições com autenticação:

{
  "rules": {
    ".read": "auth.uid !== null",
    ".indexOn": ["id_vendedor"],

    "proximo_id_vendedor": {
      ".read": "auth.uid !== null", 
      ".write": "auth.uid !== null"
    },

    "$uid": {
      ".write": "$uid == auth.uid"
    }
  }
} 
  

💻 Como Executar o Projeto
Clone o repositório:

Bash
git clone https://github.com/seu-usuario/desenvolvimento-kivy-python.git
cd desenvolvimento-kivy-python
Crie e ative o ambiente virtual:

Bash
python -m venv .venv312
# Windows:
.venv312\Scripts\activate
# Linux/Mac:
source .venv312/bin/activate
Instale as dependências:

Bash
pip install kivy requests python-dotenv
Configure o arquivo .env:
Crie o arquivo .env na raiz do projeto com a sua chave de API do Firebase:

Snippet de código
API_KEY=SuaChaveDeApiWebDoFirebaseAqui
Inicie a aplicação:

Bash
python main.py