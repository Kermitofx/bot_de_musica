# -*- coding: utf-8 -*-

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from datetime import timedelta
from bs4 import BeautifulSoup
from time import sleep
import urllib.request
import pafy
import vlc


class Play_music:
    
    fila = []
    owners = []
    owner = ''
    block_queue = False

    url = ''
    video = None
    best = None
    playurl = None

    Instance = vlc.Instance()
    player = Instance.media_player_new()

    Media = None
    volume = 0

    ajuda = """/play nome_da_música ou url.
/pause Pausa a faixa atualmente sendo reproduzida.
/resume Retomar a música pausada.
/np Mostra o nome da música.
/volume Verifique ou altere o volume atual.
/skip Ignora a música atual e reproduz a próxima música da fila
/queue Mostra todas as músicas na fila
/remove Remove uma música da fila
/clear Remove todas músicas da fila"""

    def start(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)
        bot.send_message(
            chat_id=update.message.chat_id,
            text=self.ajuda
        )


    def help(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)
        
        bot.send_message(
            chat_id=update.message.chat_id,
            text=self.ajuda
        )


    def fill_queue(self,link,owner,bot,update,next=False):

        if self.video != None and self.player.is_playing() == 1 and next == False or self.video != None and next == False and len(self.fila) >= 1:

            self.owners.append(owner)
            self.fila.append(link)

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Adicionado a fila: '+pafy.new(link).title+'\nPosição: '+str(len(self.fila))
            )
        else:
            if self.player != None:
                self.player.stop()
            
            if next == True:
                self.owner = self.owners[0]
                self.owners.pop(0)

                self.url = self.fila[0]
                self.fila.pop(0)
            else:
                self.owner = owner
                self.url = link

            self.video = pafy.new(self.url)
            self.best = self.video.getbest()
            self.playurl = self.best.url

            self.Media = self.Instance.media_new(self.playurl)
            self.Media.get_mrl()
            self.player.set_media(self.Media)
            self.player.audio_set_volume(self.volume)

            import ipdb; ipdb.set_trace()
            self.player.play()
            self.block_queue = False

            if next == False:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Reproduzindo: '+self.video.title
                )


    def skipMusic(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)

        if len(self.fila) >= 1:
            self.fill_queue(None,None,bot,update,True)

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Reproduzindo: '+self.video.title+'\nAdicionado por: '+self.owner
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, a fila está vazia'
            )


    def play(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)
        
        try:
            textToSearch = update.message.text.split(' ',1)[1]

            query = urllib.parse.quote(textToSearch)
            url = "https://www.youtube.com/results?search_query=" + query
            response = urllib.request.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html, 'html.parser')
            for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
                link = 'https://www.youtube.com' + vid['href']
                break

            self.fill_queue(link,update.message.chat['first_name'],bot,update)
        except Exception as e:
            print('Erro: '+str(e))
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, digite o nome de uma música ou envie a url'
            )


    def pause(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)
        
        if self.block_queue == False:
            self.block_queue = True
            self.player.set_pause(1)

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Música pausada!'
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, a música já está pausada'
            )


    def resume(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)

        if self.block_queue == True:        
            self.block_queue = False
            self.player.set_pause(0)

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Reproduzindo: '+self.video.title
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, a música já está tocando'
            )


    def np(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)

        if self.video != None and self.player.is_playing() == 1:

            current_time = str(timedelta(microseconds=self.player.get_time()*1000))[:7]
            total_time = self.video.duration

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Tocando no momento: '+self.video.title +'\n'+current_time+' / '+total_time+'\nAdicionado por: '+self.owner
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Nenhuma música tocando no momento.'
            )


    def showQueue(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)

        if len(self.fila) >= 1:
            queue_msg = ''

            for item in range(len(self.fila)):
                queue_msg += '('+str(item+1)+') '+self.owners[item]+' - '+pafy.new(self.fila[item]).title+'\n'

            bot.send_message(
                chat_id=update.message.chat_id,
                text=queue_msg
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, a fila está vazia'
            )


    def clearQueue(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)
        
        if len(self.fila) >= 1:
            self.fila = []
            self.owners = []

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Você limpou a fila'
            )
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, a fila já está vazia'
            )

    
    def removeQueue(self, bot, update):
        try:
            music = int(update.message.text.split(' ',1)[1])-1

            link = self.fila[music]
            self.fila.pop(music)
            self.owners.pop(music)

            bot.send_message(
                chat_id=update.message.chat_id,
                text='Removido da fila: '+pafy.new(link).title
            )
                
        except Exception as e:     
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Oops, esta posição da fila não existe'
            )


    def changeVolume(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)

        if update.message.text.lower() == '/volume':
            bot.send_message(
                chat_id=update.message.chat_id,
                text='Volume: '+str(self.volume)
            )
        else:
            try:
                new_volume = int(update.message.text.split(' ',1)[1])

                if new_volume > 100:
                    new_volume = 100
                elif new_volume < 0:
                    new_volume = 0

                self.volume = new_volume

                if self.player != None and self.player.is_playing() == 1:
                    self.player.audio_set_volume(self.volume)

                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Volume alterado para: '+str(self.volume)
                )
                    
            except Exception as e:     
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text='Oops, envie um valor entre 0 a 100'
                )


    def unknown(self,bot, update):
        print(update.message.chat['first_name']+': '+update.message.text)
        
        response_message = "Comando não encontrado\nDigite /help para obter os comandos"
        bot.send_message(
            chat_id=update.message.chat_id,
            text=response_message
        )


    def main(self):
        updater = Updater(token='823044227:AAH2fTfEVflRAfLWBRLWHgdulRVQ7BnwjD8')
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', self.start))
        dispatcher.add_handler(CommandHandler('help', self.help))
        dispatcher.add_handler(CommandHandler('play', self.play))
        dispatcher.add_handler(CommandHandler('p', self.play))
        dispatcher.add_handler(CommandHandler('remove', self.removeQueue))
        dispatcher.add_handler(CommandHandler('rm', self.removeQueue))
        dispatcher.add_handler(CommandHandler('clear', self.clearQueue))
        dispatcher.add_handler(CommandHandler('pause', self.pause))
        dispatcher.add_handler(CommandHandler('stop', self.pause))
        dispatcher.add_handler(CommandHandler('resume', self.resume))
        dispatcher.add_handler(CommandHandler('skip', self.skipMusic))
        dispatcher.add_handler(CommandHandler('queue', self.showQueue))
        dispatcher.add_handler(CommandHandler('np', self.np))
        dispatcher.add_handler(CommandHandler('volume', self.changeVolume))
        dispatcher.add_handler(MessageHandler(Filters.command, self.unknown))

        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    print("ChickenMusic iniciado!\n")    
    Play_music().main()