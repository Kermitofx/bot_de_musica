from time import sleep
import pafy
import vlc


path_queue = 'files/queue.txt'
path_command = 'files/command.txt'

Instance = vlc.Instance()
player = Instance.media_player_new()
command_file = open(path_command, 'w')
command_file.write('')
command_file.close()


def get_link():
    try:
        queue_file = open(path_queue, 'r')
        queue = queue_file.read()
        queue_file.close()

        cut = queue.find('\n')

        if cut != -1:
            link = queue[0:cut]
            queue = queue[cut+1:]

            queue_file = open(path_queue, 'w')
            queue_file.write(queue)
            queue_file.close()

            return link

        else:
            return ''

    except:
        queue_file = open(path_queue, 'w')
        queue_file.close()
        link = ''

    return link


def play_music(link):
    video = pafy.new(link)
    best = video.getbest()
    playurl = best.url

    Media = Instance.media_new(playurl)
    Media.get_mrl()
    player.set_media(Media)
    player.play()


def main():
    if player.get_state() == vlc.State.NothingSpecial or player.get_state() == vlc.State.Ended:
        link = get_link()

        if link:
            play_music(link)

    else:
        command_file = open(path_command, 'r')
        command = command_file.read()
        command_file.close()

        if command != '':
            if command == "pause":
                player.set_pause(1)
            elif command == "resume":
                player.set_pause(0)
            elif command == "skip":
                link = get_link()
                if link:
                    play_music(link)
            elif "volume" in command:
                player.audio_set_volume(int(command[6:]))

            command_file = open(path_command, 'w')
            command_file.write('')
            command_file.close()


print("Player iniciado!")
while True:
    main()
    sleep(0.5)