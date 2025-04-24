# 🤖 FURIA Bot - Telegram Edition

Um bot para fãs da FURIA no CS2, desenvolvido com Python e integração opcional com IA (Gemini). Este projeto foi criado para fins de portfólio e como parte de um processo seletivo.  
**#GoFURIA 🔥**

---

## 📋 Pré-requisitos

- ✅ Python **3.8+**
- ✅ Token do Bot Telegram _(obtenha com o [@BotFather](https://t.me/BotFather))_
- ✅ Chave da API Gemini _(opcional, para IA)_

---

## ⚙️ Configuração Inicial

1️⃣ **Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/furia-bot.git
cd furia-bot
```

2️⃣ **Crie e ative um ambiente virtual:**

```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
.env\Scriptsctivate         # Windows
```

3️⃣ **Instale as dependências:**

```bash
pip install -r requirements.txt
```

4️⃣ **Configure as variáveis de ambiente:**

Renomeie `.env.example` para `.env` e preencha com suas credenciais:

```env
TELEGRAM_BOT_TOKEN=seu_token_aqui       # Obrigatório
GEMINI_API_KEY=sua_chave_gemini         # Opcional (para IA)
```

---

## 🚀 Como Executar

Inicie o bot com o comando:

```bash
python main.py
```

▶ O bot estará online e pronto para interagir no Telegram!

---

## ⌨️ Comandos Disponíveis

| Comando      | Descrição                         |
| ------------ | --------------------------------- |
| `/start`     | Inicia o bot e mostra o menu      |
| `/help`      | Lista todos os comandos           |
| `/jogadores` | Mostra o elenco atual da FURIA    |
| `/titulos`   | Lista os títulos conquistados     |
| `/jogos`     | Exibe próximas partidas agendadas |
| `/redes`     | Links das redes sociais da FURIA  |

---

## 🎯 Funcionalidades Extras

- ✔ Respostas com IA via Gemini
- ✔ Botões interativos no Telegram
- ✔ Sistema de cache para melhor desempenho

---

## 📂 Estrutura do Projeto

```
furia-bot/
├── main.py             # Código principal do bot
├── config.py           # Configurações do bot
├── FURIA_DATA.py       # Dados e informações da FURIA
├── .env                # Variáveis de ambiente (não versionado)
├── .env.example        # Modelo de configuração
├── .gitignore          # Padrões ignorados pelo Git
├── requirements.txt    # Dependências do projeto
└── README.md           # Documentação do projeto
```

---

## 🤝 Contribuição

Contribuições são muito bem-vindas!

1. Faça um fork
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um **Pull Request**

---

## 📜 Licença

Este projeto é open-source, desenvolvido para fins educacionais e de portfólio. Fique à vontade para reutilizar com os devidos créditos.

---

## 📬 Contato

Desenvolvido por **Nicolas Fernandes**  
✉ [nicolasbafernandes@gmail.com](mailto:nicolasbafernandes@gmail.com)  
🌐 [nicolas-fernandes-portfolio.vercel.app](https://nicolas-fernandes-portfolio.vercel.app/)

---
