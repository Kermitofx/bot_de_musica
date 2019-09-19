from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from multiprocessing import Process
from os import mkdir as create
from datetime import datetime
from bs4 import BeautifulSoup
from os.path import exists
from time import sleep
import urllib.request
import requests
import pafy


path_communication = 'files/communication.txt'
path_command = 'files/command.txt'
path_whitelist = 'files/users.txt'
path_history = 'files/history.txt'
path_token = 'files/token.txt'
path_queue = 'files/queue.txt'

if not exists('files'):
    create('files')

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

try:
    communication_file = open(path_communication, 'r')
    communication_file.close()
except:
    communication_file = open(path_communication, 'w')
    communication_file.close()

try:
    token_file = open(path_token, 'r')
    token = token_file.read()
    token_file.close()
except:
    token = input('Token do telegram não encontrado, cole o Token de seu Bot aqui: ')

    token_file = open(path_token, 'w')
    token_file.write(str(token))
    token_file.close()

user_blocked = 'Você não tem permissão para usar este comando, digite /password <senha>'
password = input('Digite uma senha: ')
help_message = '''/play nome_da_música ou url.
/pause Pausa a faixa atualmente sendo reproduzida.
/resume Retomar a música pausada.
/np Mostra o nome da atual música.
/volume Verifique ou altere o volume atual.
/skip Ignora a música atual e reproduz a próxima música da fila'''



def history(msg):
    history_file = open(path_history, 'a')
    history_file.write(msg+'\n')
    history_file.close()
    print(msg)



def set_command(update,command_player):
    command_file = open(path_command, 'w')
    command_file.write(str(update.message.chat_id)+' '+command_player+' '+update.message.chat['first_name'])
    command_file.close()



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



def logger(update):
    if update:
        log = datetime.strftime(datetime.now(), '%H:%M:%S %d/%m/%Y')
        log += ' '+str(update.message.chat_id)+' '+update.message.chat['first_name']+': '+update.message.text
        return log
    else:
        return 'Erro: objeto vazio'


def setAnswer(user,message):
    if message:
        answer = requests.get('https://api.telegram.org/bot'+str(token)+'/sendMessage?chat_id='+str(user)+'&text='+str(message))
        return True
    else:
        return False


def start(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        response_message = help_message
    else:
        response_message = 'Digite /password <senha> para utilizar este bot'

    setAnswer(update.message.chat_id,response_message)
    


def verifyPassword(bot, update):
    history(logger(update))

    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        response_message = 'Você já está cadastrado, digite /help para ver os comandos.'
    else:
        try:
            text = update.message.text.split(' ',1)[1]
        except:
            text = None

        if text == None:
            response_message = 'Digite uma senha para usar o bot.'
        elif text == password:
            whitelist_file = open(path_whitelist, 'a')
            whitelist_file.write(str(update.message.chat_id)+'\n')
            whitelist_file.close()

            response_message = 'Senha correta, digite /help para ver os comandos.'
        else:
            response_message = 'Senha incorreta, tente novamente.'

    setAnswer(update.message.chat_id,response_message)


def getHelp(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        response_message = help_message
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)


def setPause(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        set_command(update,'pause')
        response_message = 'Música pausada!'
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)


def setResume(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        set_command(update,'resume')
        response_message = 'Reproduzindo música!'
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)


def skipMusic(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        set_command(update,'skip')
        response_message = 'Reproduzindo próxima música!'
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)


def setVolume(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        if update.message.text == '/volume':
            set_command(update,'volume')
        else:
            try:
                text = int(update.message.text.split(' ',1)[1])

                if text < 0:
                    text = 0
                elif text > 100:
                    text = 100
            except:
                text = None

            if text == None:
                response_message = 'Digite um valor entre 0 a 100'
            else:
                set_command(update,'volume'+str(text))
                response_message = 'Volume alterado para: '+str(text)+'%'
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)


def nowPlaying(bot, update):
    history(logger(update))
    whitelist = getWhiteList()

    if str(update.message.chat_id) in whitelist:
        set_command(update,'nowplaying')
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)
        

def playMusic(bot, update):
    history(logger(update))
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
            setAnswer(update.message.chat_id,'Pesquisando por: '+textToSearch)
            query = urllib.parse.quote(textToSearch)
            url = 'https://www.youtube.com/results?search_query=' + query
            response = urllib.request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                link = 'https://www.youtube.com' + vid['href']
                break

        queue_file = open(path_queue, 'a')
        queue_file.write(link+'\n')
        queue_file.close()
        response_message = 'Música adicionada: '+pafy.new(link).title
    else:
        response_message = user_blocked

    setAnswer(update.message.chat_id,response_message)


def listen_communication():
    while True:
        sleep(0.3)
        communication_file = open(path_communication, 'r')
        messages = communication_file.read()
        communication_file.close()

        if messages:
            communication_file = open(path_communication, 'w')
            communication_file.write('')
            communication_file.close()

            messages = messages.split('\n')
            for user_body in messages:
                if user_body:
                    user_id = user_body.split(' ',1)[0]
                    user_msg = user_body.split(' ',1)[1]
                    setAnswer(user_id,user_msg)


def main():
    updater = Updater(token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler(['password', 'pw'], verifyPassword))
    dispatcher.add_handler(CommandHandler(['skip', 's', 'next'], skipMusic))
    dispatcher.add_handler(CommandHandler(['np', 'nowplaying'], nowPlaying))
    dispatcher.add_handler(CommandHandler(['play', 'p'], playMusic))
    dispatcher.add_handler(CommandHandler(['resume'], setResume))
    dispatcher.add_handler(CommandHandler(['volume'], setVolume))
    dispatcher.add_handler(CommandHandler(['pause'], setPause))
    dispatcher.add_handler(CommandHandler(['stop'], setPause))
    dispatcher.add_handler(CommandHandler(['help'], getHelp))
    dispatcher.add_handler(CommandHandler(['start'], start))

    updater.start_polling()
    updater.idle()


print('Bot iniciado!\n')


assincrono = True

if assincrono == True:
    if __name__ == "__main__":
        telegram_process = Process(target=main)
        send_messages = Process(target=listen_communication)

        telegram_process.start()
        send_messages.start()

        telegram_process.join()
        send_messages.join()
else:
    main()