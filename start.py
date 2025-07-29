import logging, json
import asyncio
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters

botToken = str()
__allowed = str()
_chat_member_username_id = {}

try: 
    botTokenFileHandler = open("botToken.txt","r")
    botToken = botTokenFileHandler.read()
    botTokenFileHandler.close()
except FileNotFoundError:
    print("Il file contenente il token del bot è vuoto.")
    exit()

try: 
    chatMembersFileHandler = open("chatmembers.json","r")
    _chat_member_username_id = chatMembersFileHandler.read()
    chatMembersFileHandler.close()
except FileNotFoundError:
    print("La lista degli utenti è vuoto.")
    exit()


logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.WARNING
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "Bot pronto. Richiede permessi di admin.")

async def ban_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    __member_to_ban_username = context.args[0] # obtain only the raw username
    if (len(__member_to_ban_username) <= 4): # usernames must be at least 4 characters long.
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "Username non valido.")
    else: # here we have a valid username
        __banned = get_id_from_username(__member_to_ban_username)
        if (__banned == 0):
            await context.bot.send_message(chat_id = update.effective_chat.id, text = "Username non trovato.")
        else:
            try:
                successful_ban = await context.bot.ban_chat_member(chat_id = update.effective_chat.id, user_id = __banned)
                if (successful_ban is False): # this should never happen according to the docs.
                    await context.bot.send_message(chat_id = 1091498287, text = f"Ban di {__member_to_ban_username} fallito, controlla i log.")
                else:
                    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"{__member_to_ban_username} bannato.")
            except: # we are trying to ban a channel
                await context.bot.ban_chat_sender_chat(chat_id = update.effective_chat.id, user_id = __banned)
                await context.bot.send_message(chat_id = update.effective_chat.id, text = f"Canale {__member_to_ban_username} bannato.")

async def unban_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    __member_to_unban_username = context.args[0]
    if (len(__member_to_unban_username) <= 4):
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "Username non valido.")
    else:
        __unbanned = get_id_from_username(__member_to_unban_username)
        if (__unbanned == 0):
            await context.bot.send_message(chat_id = update.effective_chat.id, text = "Username non trovato.")
        else:
            try:
                successful_unban = await context.bot.unban_chat_member(chat_id = update.effective_chat.id, user_id = __unbanned, only_if_banned = True)
                if (successful_unban is False): # this should never happen according to the docs.
                    await context.bot.send_message(chat_id = 1091498287, text = f"Unban di {__member_to_unban_username} fallito, controlla i log.")
                else:
                    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"{__member_to_unban_username} sbannato.")
            except: # we are trying to unban a channel
                await context.bot.unban_chat_sender_chat(chat_id = update.effective_chat.id, user_id = __unbanned)
                await context.bot.send_message(chat_id = update.effective_chat.id, text = f"Canale {__member_to_ban_username} sbannato.")

async def kick_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    __member_to_kick_username = context.args[0]
    if (len(__member_to_kick_username) <= 4):
        await context.bot.send_message(chat_id = update.effective_chat.id, text = "Username non valido.")
    else:
        __kicked = get_id_from_username(__member_to_kick_username)
        if (__kicked == 0):
            await context.bot.send_message(chat_id = update.effective_chat.id, text = "Username non trovato.")
        else:
            try:
                successful_ban = await context.bot.ban_chat_member(chat_id = update.effective_chat.id, user_id = __kicked)
                successful_unban = await context.bot.unban_chat_member(chat_id = update.effective_chat.id, user_id = __kicked, only_if_banned = True)
                if (successful_unban is False or successful_ban is False): # this should never happen according to the docs.
                    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"Kick di {__member_to_kick_username} fallito, controlla i log.")
                else:
                    await context.bot.send_message(chat_id = update.effective_chat.id, text = f"{__member_to_kick_username} kickato.")
            except: # we are trying to kick a channel
                await context.bot.send_message(chat_id = update.effective_chat.id, text = "Non puoi kickare un canale, leggi i docs idiota") # non è proprio vero... ma facciamo finta lo sia
                
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    parole = context.args[0]
    await context.bot.send_message(chat_id = update.effective_chat.id, text = parole)

def get_id_from_username(usrname):
    banhammer = 0
    for user in _chat_member_username_id['users']:
        if ((user["user"]) == usrname):
            banhammer = user["id"]
    return banhammer
       

if __name__ == '__main__':
    application = ApplicationBuilder().token(botToken).build()
    
    __start_handler = CommandHandler('start', start)
    application.add_handler(__start_handler)

    __member_ban_handler = CommandHandler('ban', ban_member)
    application.add_handler(__member_ban_handler)

    __member_unban_handler = CommandHandler('unban', unban_member)
    application.add_handler(__member_unban_handler)

    __member_kick_handler = CommandHandler('kick', kick_member)
    application.add_handler(__member_kick_handler)

    echo_handler = CommandHandler('annuncio', echo)
    application.add_handler(echo_handler)

    application.run_polling()

    # Funzioni da implementare:
    # Ban e unban ☑
    # Kick ☑
    # Mutare e smutare: come creare un oggetto telegram.ChatPermissions? vedi https://docs.python-telegram-bot.org/en/v20.7/telegram.chatpermissions.html
    # Echo ☑
    # Cancellare i messaggi altrui (quando MessageHandler non farà schifo al cazzo magari)
