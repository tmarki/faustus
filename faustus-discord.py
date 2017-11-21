#!/usr/bin/python3
import discord
import asyncio
import mods.cleverbot
import logging
from config import Config

TOKEN = Config.DISCORD_TOKEN


logger = logging.getLogger('discord')
logger.setLevel(Config.LOG_LEVEL)
hndl = logging.FileHandler(filename='faustus.log', encoding='utf-8', mode='w')
form = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')
hndl.setFormatter(form)
logger.addHandler(hndl)

client = discord.Client()

cb = mods.cleverbot.Session(Config.CLEVERBOT_API_KEY)

@client.event
@asyncio.coroutine
def on_ready():
    logger.log(logging.DEBUG, 'Logged in as'
        + client.user.name + " id: " + client.user.id)

def make_reply(author, question):
    return author + ": " + cb.Ask(question)

@client.event
@asyncio.coroutine
def on_message(message):
    if client.user in message.mentions:
        question = message.content.replace(client.user.mention, "")
        reply = make_reply(message.author.mention, question)
        yield from client.send_message(message.channel, reply)

client.run(TOKEN)
