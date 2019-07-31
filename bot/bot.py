import discord
import os
from boggle import Boggle

mainboggle = Boggle()
client = discord.Client()


@client.event
async def on_ready():
    print("Logged in as: " + client.user.name)
    print("...")


@client.event
async def on_message(message):

    channel = message.channel
    if message.content.startswith("!boggle") :
        # Start a new game
        mainboggle.reset_game()
        await channel.send(mainboggle.get_chat_board())
    elif message.content.startswith("!show"):
        # Show the current game
        await channel.send(mainboggle.get_chat_board())
    elif len(message.content.split()) == 1 and mainboggle.is_valid(message.content) and \
            mainboggle.is_on_board(message.content):
        # Player guessed a word
        mainboggle.play_word(message.content,message.author.name)
        await channel.send(message.author.name + " played " +message.content.upper())
    elif message.content.startswith("!score"):
        # Show the current score
        score = mainboggle.get_score_string()
        if score:
            await channel.send(score)
    elif message.content.startswith("!remaining"):
        # Display the remaining playable words, this also makes the remaining words unpalyable
        remaining = mainboggle.get_remaining_words_string()
        await channel.send(remaining)

client.run(os.environ.get('BOT_TOKEN'))