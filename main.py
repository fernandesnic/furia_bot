from config import Config
import google.generativeai as genai
import logging
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    CallbackQuery  
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from functools import lru_cache

# Configuração do Gemini
try:
    GEMINI_API_KEY = Config.get("GEMINI_API_KEY")
    genai.configure(api_key=GEMINI_API_KEY)
    MODEL_NAME = 'gemini-1.5-pro-latest'
except Exception as e:
    logging.error(f"Erro na configuração do Gemini: {e}")
    MODEL_NAME = None

# Configuração do Telegram
TOKEN = Config.get("TELEGRAM_BOT_TOKEN")

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Dados sobre a FURIA CS
FURIA_DATA = {
    "jogadores": {
        "FalleN": {
            "nome": "Gabriel Toledo",
            "funcao": "IGL",
            "idade": 34,
            "rating": 1.08,
            "bio": "Lenda do CS brasileiro, retornou à FURIA em 2024 como líder e awper."
        },
        "KSCERATO": {
            "nome": "Kaike Cerato",
            "funcao": "Rifler",
            "idade": 26,
            "rating": 1.18,
            "bio": "Principal jogador da equipe, mantém excelente consistência desde 2019."
        },
        "yuurih": {
            "nome": "Yuri Santos",
            "funcao": "Lurker",
            "idade": 25,
            "rating": 1.15,
            "bio": "Versátil e explosivo, um dos melhores do mundo em situações difíceis."
        },
        "molodoy": {
            "nome": "Egor Molodoy Zhivoderov",
            "funcao": "AWPer",
            "idade": 21,
            "rating": 1.12,
            "bio": "Jovem promessa russa contratada em 2025, mostrando grande potencial."
        },
        "YEKINDAR": {
            "nome": "Mareks Gaļinskis",
            "funcao": "Entry Fragger",
            "idade": 26,
            "rating": 1.10,
            "bio": "Letão agressivo, ex-Virtus.pro, traz experiência internacional."
        },
        "chelo": {
            "status": "Reserva",
            "nome": "Marcelo Cespedes",
            "idade": 30,
            "bio": "Experiente jogador de apoio, agora no banco de reservas."
        },
        "skulz": {
            "status": "Reserva",
            "nome": "Pedro Scuracchio",
            "idade": 22,
            "bio": "Jovem promessa brasileira, aguardando oportunidade."
        }
    },
    "elenco_principal": ["FalleN", "KSCERATO", "yuurih", "molodoy", "YEKINDAR"],
    "coaching": {
        "sidde": {
            "nome": "Sidnei Macedo Pereira Filho",
            "funcao": "Técnico",
            "idade": 28,
            "bio": "Líder técnico desde 2024, guiando o elenco da FURIA."
        }
    },
    "titulos": [
        "ESL Pro League Season 12: North America",
        "Elisa Masters Espoo 2023",
        "BLAST.tv Paris Major 2023: RMR Americas (1º Lugar)",
        "Brasil Game Show 2023",
        "Pinnacle Cup V (Vice-campeonato)",
        "Semifinais IEM Rio Major"
    ],
    "proximos_jogos": [
        "IEM Cologne 2025 - 15/07/2025",
        "BLAST Premier Fall Groups - 20/08/2025",
        "Major Rio 2025 - 10/10/2025"
    ],
    "redes": {
        "Twitter": "https://twitter.com/furiagg",
        "Instagram": "https://instagram.com/furiagg",
        "Site": "https://furia.gg",
        "YouTube": "https://youtube.com/furiagg",
        "Twitch": "https://twitch.tv/furiagg"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /start"""
    user = update.effective_user
    welcome_message = (
        f"Olá {user.first_name}! 👋\n\n"
        "Eu sou o bot da FURIA CS! 🐯\n\n"
        "Posso te informar sobre:\n"
        "- Elenco atual\n"
        "- Próximos jogos\n"
        "- Títulos conquistados\n"
        "- Redes sociais\n\n"
        "Use os botões abaixo ou digite o que quer saber!"
    )
    
    keyboard = [
        [InlineKeyboardButton("👥 Elenco", callback_data='elenco')],
        [InlineKeyboardButton("🏆 Títulos", callback_data='titulos')],
        [InlineKeyboardButton("🎮 Próximos Jogos", callback_data='proximos_jogos')],
        [InlineKeyboardButton("🌐 Redes Sociais", callback_data='redes')],
        [InlineKeyboardButton("🤖 Perguntar à IA", callback_data='ia_question')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /help"""
    help_text = """
    🐯 FURIA CS:GO Bot 🐯

    Comandos disponíveis:
    /start - Inicia o bot
    /help - Mostra esta ajuda
    /jogadores - Mostra o elenco
    /titulos - Mostra conquistas
    /jogos - Próximas partidas
    /redes - Links das redes sociais
    
    Ou simplesmente me pergunte sobre a FURIA!
    """
    await update.message.reply_text(help_text)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para os callbacks dos botões inline"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'elenco':
        await show_players_menu(query)
    elif query.data == 'titulos':
        await show_titles(query)
    elif query.data == 'proximos_jogos':
        await show_next_matches(query)
    elif query.data == 'redes':
        await show_social_media(query)
    elif query.data == 'ia_question':
        await query.edit_message_text(text="Digite sua pergunta sobre a FURIA CS:GO:")
    elif query.data == 'back':
        await start_from_query(query)
    elif query.data.startswith('player_'):
        await show_player_details(query)

async def start_from_query(query: CallbackQuery) -> None:
    """Volta para o menu principal a partir de uma query"""
    user = query.from_user
    welcome_message = (
        f"Olá {user.first_name}! 👋\n\n"
        "Eu sou o bot oficial da FURIA CS:GO! 🐯\n\n"
        "Posso te informar sobre:\n"
        "- Elenco atual\n"
        "- Próximos jogos\n"
        "- Títulos conquistados\n"
        "- Redes sociais\n\n"
        "Use os botões abaixo ou digite o que quer saber!"
    )
    
    keyboard = [
        [InlineKeyboardButton("👥 Elenco", callback_data='elenco')],
        [InlineKeyboardButton("🏆 Títulos", callback_data='titulos')],
        [InlineKeyboardButton("🎮 Próximos Jogos", callback_data='proximos_jogos')],
        [InlineKeyboardButton("🌐 Redes Sociais", callback_data='redes')],
        [InlineKeyboardButton("🤖 Perguntar à IA", callback_data='ia_question')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text=welcome_message, reply_markup=reply_markup)

async def show_players_menu(query: CallbackQuery) -> None:
    """Mostra o menu de jogadores"""
    keyboard = []
    for player in FURIA_DATA["elenco_principal"]:
        keyboard.append([InlineKeyboardButton(player, callback_data=f'player_{player}')])
    
    keyboard.append([InlineKeyboardButton("chelo (Reserva)", callback_data='player_chelo')])
    keyboard.append([InlineKeyboardButton("skulz (Reserva)", callback_data='player_skulz')])
    keyboard.append([InlineKeyboardButton("sidde (Técnico)", callback_data='player_sidde')])
    keyboard.append([InlineKeyboardButton("🔙 Voltar", callback_data='back')])
    
    await query.edit_message_text(
        text="Escolha um jogador para ver mais detalhes:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_player_details(query: CallbackQuery) -> None:
    """Mostra detalhes de um jogador específico"""
    player_id = query.data.split('_')[1]
    
    if player_id in FURIA_DATA["jogadores"]:
        player = FURIA_DATA["jogadores"][player_id]
    else:
        player = FURIA_DATA["coaching"][player_id]
    
    message = f"🐯 {player_id} ({player['nome']})\n\n"
    message += f"📌 Função: {player.get('funcao', 'N/A')}\n"
    message += f"🎂 Idade: {player['idade']} anos\n"
    
    if 'rating' in player:
        message += f"⭐ Rating: {player['rating']}\n\n"
    else:
        message += "\n"
    
    message += f"📝 Sobre: {player['bio']}"
    
    await query.edit_message_text(
        text=message,
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data='elenco')]])
    )

async def show_titles(query: CallbackQuery) -> None:
    """Mostra os títulos conquistados pela FURIA"""
    titles = "\n".join([f"🏆 {title}" for title in FURIA_DATA["titulos"]])
    await query.edit_message_text(
        text=f"🏆 Títulos da FURIA CS:GO 🏆\n\n{titles}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data='back')]])
    )

async def show_next_matches(query: CallbackQuery) -> None:
    """Mostra os próximos jogos da FURIA"""
    matches = "\n".join([f"🕒 {match}" for match in FURIA_DATA["proximos_jogos"]])
    await query.edit_message_text(
        text=f"🎮 Próximos Jogos da FURIA 🎮\n\n{matches}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data='back')]])
    )

async def show_social_media(query: CallbackQuery) -> None:
    """Mostra as redes sociais da FURIA"""
    social_media = "\n".join([f"🔗 {network}: {link}" for network, link in FURIA_DATA["redes"].items()])
    await query.edit_message_text(
        text=f"🌐 Redes Sociais da FURIA 🌐\n\n{social_media}",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Voltar", callback_data='back')]])
    )

@lru_cache(maxsize=100)
def generate_furia_response(user_question: str) -> str:
    """Gera uma resposta usando a API do Gemini"""
    if not MODEL_NAME:
        return "Desculpe, o serviço de IA não está disponível no momento."
    
    prompt = {
        'parts': [{
            'text': f"""
            Você é um assistente especializado na equipe brasileira de CS2 da FURIA Esports.
            Responda em português com dados REAIS e precisos. Esse bot foi criado por Nicolas Fernandes, para um processo seletivo de estágio na furia.

            Contexto atual:
            - Elenco: {', '.join(FURIA_DATA['elenco_principal'])}
            - Último título: {FURIA_DATA['titulos'][-1] if FURIA_DATA['titulos'] else 'Nenhum'}
            - Próximo jogo: {FURIA_DATA['proximos_jogos'][0] if FURIA_DATA['proximos_jogos'] else 'Não agendado'}

            Regras: 
            1. Seja técnico mas acessível
            2. Use termos de CS2 quando relevante
            3. Limite a 250 palavras
            4. Formate para mobile

            Pergunta: {user_question}
            """
        }],
        'role': 'user'
    }
    
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)  # Changed to synchronous call
        return response.text
    except Exception as e:
        logger.error(f"Erro Gemini: {type(e).__name__} - {str(e)}")

async def handle_ai_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Lida com perguntas para a IA"""
    user_question = update.message.text.strip()
    
    if len(user_question) < 3:
        await update.message.reply_text("Por favor, faça uma pergunta mais detalhada.")
        return
    
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )
    
    answer = generate_furia_response(user_question) 
    
    if answer:
        formatted_answer = f"🐯 *Resposta sobre FURIA* 🐯\n\n{answer}\n\n_Fonte: Dados atualizados 2025_"
        await update.message.reply_text(formatted_answer, parse_mode='Markdown')
    else:
        await update.message.reply_text(
            "🔧 Estou com dificuldades técnicas no momento.\n"
            "Você pode tentar:\n"
            "- Perguntas mais específicas (/jogadores, /titulos)\n"
            "- Visitar o site: https://furia.gg\n"
            "- Tentar novamente mais tarde"
        )

async def show_players_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /jogadores"""
    keyboard = []
    for player in FURIA_DATA["elenco_principal"]:
        keyboard.append([InlineKeyboardButton(player, callback_data=f'player_{player}')])
    
    keyboard.append([InlineKeyboardButton("Reservas/Técnico", callback_data='elenco')])
    
    await update.message.reply_text(
        "Escolha um jogador:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_titles_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /titulos"""
    titles = "\n".join([f"🏆 {title}" for title in FURIA_DATA["titulos"]])
    await update.message.reply_text(f"🏆 Títulos da FURIA CS:GO 🏆\n\n{titles}")

async def show_matches_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /jogos"""
    matches = "\n".join([f"🕒 {match}" for match in FURIA_DATA["proximos_jogos"]])
    await update.message.reply_text(f"🎮 Próximos Jogos da FURIA 🎮\n\n{matches}")

async def show_social_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para o comando /redes"""
    social_media = "\n".join([f"🔗 {network}: {link}" for network, link in FURIA_DATA["redes"].items()])
    await update.message.reply_text(f"🌐 Redes Sociais da FURIA 🌐\n\n{social_media}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handler para mensagens de texto não comandos"""
    text = update.message.text.lower()
    
    if any(word in text for word in ["jogador", "elenco", "time", "equipe"]):
        await show_players_command(update, context)
    elif any(word in text for word in ["titulo", "conquista", "trofeu"]):
        await show_titles_command(update, context)
    elif any(word in text for word in ["jogo", "partida", "calendario"]):
        await show_matches_command(update, context)
    elif any(word in text for word in ["rede", "social", "instagram", "twitter"]):
        await show_social_command(update, context)
    else:
        await handle_ai_question(update, context)

def main() -> None:
    """Inicia o bot"""
    # Cria a aplicação
    application = Application.builder().token(TOKEN).build()
    
    # Adiciona os handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("jogadores", show_players_command))
    application.add_handler(CommandHandler("titulos", show_titles_command))
    application.add_handler(CommandHandler("jogos", show_matches_command))
    application.add_handler(CommandHandler("redes", show_social_command))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Bot iniciado...")
    application.run_polling()

if __name__ == '__main__':
    main()