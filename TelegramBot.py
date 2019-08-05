from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from bs4 import BeautifulSoup
import urllib.request


path_command = 'files/command.txt'
path_queue = 'files/queue.txt'
path_whitelist = 'files/whitelist.txt'
path_history = 'files/history.txt'


try:
    command_file = open(path_command, 'r')
    command_file.close()
except:
    command_file = open(path_command, 'w')
    command_file.close()

try:
    path_file = open(path_queue, 'r')
    path_file.close()
except:
    path_file = open(path_queue, 'w')
    path_file.close()

try:
    history_file = open(path_history, 'r')
    history_file.close()
except:
    history_file = open(path_history, 'w')
    history_file.close()

password = input("Digite uma senha: ")


def history(msg):
    history_file = open(path_history, 'a')
    history_file.write(msg+'\n')
    history_file.close()
    print(msg)


def getWhiteList():
    try:
        whitelist_file = open(path_whitelist, 'r')
        whitelist = whitelist_file.read()
        whitelist_file.close()
    except:
        whitelist_file = open(path_whitelist, 'w')
        whitelist_file.close()
        whitelist = ''
    
    return whitelist


def start(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)

    response_message = 'Digite /password <senha> para utilizar este bot'
    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def verifyPassword(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)

    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        response_message = "Você já está cadastrado, digite /help para ver os comandos."
    else:
        try:
            text = update.message.text.split(' ',1)[1]
        except:
            text = None

        if text == None:
            response_message = "Digite uma senha para usar o bot."
        elif text == password:
            whitelist_file = open(path_whitelist, 'a')
            whitelist_file.write(str(update.message.chat_id)+'\n')
            whitelist_file.close()

            response_message = "Senha correta, digite /help para ver os comandos."
        else:
            response_message = "Senha incorreta, tente novamente."

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def getHelp(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        response_message = """/play nome_da_música ou url.
        /pause Pausa a faixa atualmente sendo reproduzida.
        /resume Retomar a música pausada.
        /np Mostra o nome da música. (falta desenvolver)
        /volume Verifique ou altere o volume atual.
        /skip Ignora a música atual e reproduz a próxima música da fila
        /queue Mostra todas as músicas na fila"""
    else:
        response_message = "Você não tem permissão para usar este comando, digite /password <senha>"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def setPause(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        command_file = open(path_command, 'w')
        command_file.write('pause')
        command_file.close()
        response_message = "Música pausada!"
    else:
        response_message = "Você não tem permissão para usar este comando, digite /password <senha>"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def setResume(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        command_file = open(path_command, 'w')
        command_file.write('resume')
        command_file.close()
        response_message = "Reproduzindo música!"
    else:
        response_message = "Você não tem permissão para usar este comando, digite /password <senha>"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def skipMusic(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        command_file = open(path_command, 'w')
        command_file.write('skip')
        command_file.close()
        response_message = "Reproduzindo próxima música!"
    else:
        response_message = "Você não tem permissão para usar este comando, digite /password <senha>"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def setVolume(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        try:
            text = int(update.message.text.split(' ',1)[1])

            if text < 0:
                text = 0
            elif text > 100:
                text = 100
        except:
            text = None

        if text == None:
            response_message = "Digite um valor entre 0 a 100"
        else:
            command_file = open(path_command, 'w')
            command_file.write('volume'+text)
            command_file.close()
            response_message = "Volume alterado para %s!" % str(text)
    else:
        response_message = "Você não tem permissão para usar este comando, digite /password <senha>"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )
        

def playMusic(bot, update):
    history(str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text)
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        try:
            textToSearch = update.message.text.split(' ',1)[1]
        except:
            textToSearch = None
        
        if textToSearch == None:
            response_message = 'Oops, digite o nome de uma música ou envie a url'
        elif ('youtube.com' in textToSearch or 'youtu.be' in textToSearch) and ' ' not in textToSearch:
            link = textToSearch
        else:
            query = urllib.parse.quote(textToSearch)
            url = "https://www.youtube.com/results?search_query=" + query
            response = urllib.request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                link = 'https://www.youtube.com' + vid['href']
                break

    
        queue_file = open(path_queue, 'a')
        queue_file.write(link+'\n')
        queue_file.close()
        response_message = "Música adicionada na fila!"
    else:
        response_message = "Você não tem permissão para usar este comando, digite /password <senha>"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=response_message
    )


def main():
    updater = Updater(token='830479165:AAEj5trP77qm3O6IU85qxtlfsTSaz5bIin4')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('password', verifyPassword))
    dispatcher.add_handler(CommandHandler('help', getHelp))
    dispatcher.add_handler(CommandHandler('pause', setPause))
    dispatcher.add_handler(CommandHandler('stop', setPause))
    dispatcher.add_handler(CommandHandler('resume', setResume))
    dispatcher.add_handler(CommandHandler('volume', setVolume))
    dispatcher.add_handler(CommandHandler('play', playMusic))
    dispatcher.add_handler(CommandHandler('p', playMusic))
    dispatcher.add_handler(CommandHandler('skip', skipMusic))
    dispatcher.add_handler(CommandHandler('s', skipMusic))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print('Bot iniciado!')
    main()