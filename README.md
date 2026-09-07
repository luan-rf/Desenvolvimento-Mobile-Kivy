# 📊 Aplicativo Controle de Vendas - Hashtag

Um aplicativo mobile/desktop completo desenvolvido em **Python** utilizando o framework **Kivy** e integrado ao **Firebase** (Authentication e Realtime Database) para gerenciamento, lançamento e acompanhamento de vendas em equipe em tempo real.

---

## 📱 Sobre o Projeto

O **Controle de Vendas** permite que vendedores registrem suas transações diárias, acompanhem seu faturamento total, visualizem dados de outros membros da equipe e monitorem o desempenho geral da empresa.

O projeto segue uma arquitetura modular baseada no padrão **KV Language**, utilizando um layout raiz fixo no `main.kv` que gerencia a transição entre 9 telas dinâmicas através do `ScreenManager`.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.12**
* **Kivy 2.3.1** (Interface gráfica, manipulação de UI e eventos)
* **Firebase Authentication** (Criar conta e Login seguro via e-mail/senha)
* **Firebase Realtime Database** (Armazenamento em nuvem via API REST com a biblioteca `requests`)
* **python-dotenv** (Gerenciamento seguro da chave de API)

---

## 🚀 Arquitetura e Estrutura do App

```text
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
