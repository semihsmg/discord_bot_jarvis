import discord
import asyncio
import datetime

client = discord.Client()
isaret = '+'  # special character for commands

# written replies
liste_yazi = [['help', ''],
              ['correct', 'Initiating...']]

# voice replies [command, dir of sound, lenght of sound in sec]
liste_ses = [['jarvis', r'C:/.../x1.mp3', '2'],
             ['is it that time', r'C:/.../x2.mp3', '2.3']]


def liste_islemleri():
    global liste_ses, liste_yazi
    isaret_ekle(liste_yazi)
    isaret_ekle(liste_ses)


# add special character to begining of the all command
def isaret_ekle(liste):
    for i in range(len(liste)):
        liste[i][0] = isaret + liste[i][0]


# find index of command
def index_bul(liste, msg):
    x = [x for x in liste if msg in x][0]
    return liste.index(x)


def get_info(info):
    print(str(info.user_id) + '\n' + str(datetime.datetime.now()) + '\n')


# information about message owner
class GetInfo:
    def __init__(self, message):
        self.user_id = message.author
        self.user_voice_ch_id = message.author.voice_channel.id
        self.user_server_id = message.author.server.id
        self.message_content = message.content
        self.message = message
        self.channel = client.get_channel(self.user_voice_ch_id)


@client.event
async def on_ready():
    print('Giriş yapıldı:')
    print('Bot: ', client.user.name)
    print(client.user.id)
    print('------')
    # Change HERE for status of the bot in discord
    await client.change_presence(game=discord.Game(name='HERE'))
    liste_islemleri()


@client.event
async def on_message(message):
    global komutlar

    # Per the discord.py docs this is to not have the bot respond to itself
    if message.author == client.user:
        return

    info = GetInfo(message)
    get_info(info)

    msg = message.content.lower().strip()

    if str(msg).startswith(isaret):
        # check command message in voice answer list
        if any(msg in s for s in liste_ses):

            satir = index_bul(liste_ses, msg)
            await play_audio_file(liste_ses[satir][1], info.channel,
                                  float(liste_ses[satir][2]))

        # check command message in written answer list
        elif any(msg in s for s in liste_yazi):

            satir = index_bul(liste_yazi, msg)
            komutlar = None

            # help funtion
            if satir == 0 and not komutlar:
                komutlar = 'Sesli komutlar:\n\n' + \
                           '\n'.join(komut for i in liste_ses for komut in i if komut.startswith(isaret)) + \
                           '\n------------------\n\n' + \
                           'Yazılı komutlar:\n\n' + \
                           '\n'.join(komut for i in liste_yazi for komut in i if komut.startswith(isaret)) + \
                           '\n------------------\n\n' + \
                           'Sesli komutlar için sesli sohbet kanalında bulunmalısınız.'

            if komutlar:
                yazi = komutlar.format(message)
                await client.send_message(message.channel, yazi)

            if satir != 0:
                yazi = liste_yazi[satir][1].format(message)
                await client.send_message(message.channel, yazi)

        # if command starts with + but rest doesn't match it reply to use +help command.
        else:
            yanit = 'Sanırım komutunuzda sıkıntı var efendim!\n```+help``` komutunu tavsiye ederim.'.format(message)
            await client.send_message(message.channel, yanit)


async def play_audio_file(audio_file, get_voice_channel_id, audio_duration):
    try:
        voice = await client.join_voice_channel(get_voice_channel_id)
        player = voice.create_ffmpeg_player(audio_file)
        player.start()
        await asyncio.sleep(audio_duration)
        await voice.disconnect()

    except Exception as e:
        print('Exception: ', datetime.datetime.now())
        print(e)

# Replace the Token with your bot's token
client.run('TOKEN')
