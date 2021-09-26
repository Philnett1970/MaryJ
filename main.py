import discord
import os
import json
import requests
import random
from replit import db


client = discord.Client()

sad_words = ["sad", "depressed", "depressing", "not happy", "mad"]

starter_encouragements = [
  "Cheer Up!",
  "Hang in there.",
  "Don't give up stay strong"
]

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game(f"Watching in {len(client.guilds)} servers"),
    )
    print("bot logging in as {0.user.name}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  msg = message.content

  if msg.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  if any(word in msg for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

client.run(os.getenv('TOKEN'))
