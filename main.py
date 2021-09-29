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
  "Don't give up stay strong",
  "I believe"
]

# get a random quote from zenquotes
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

# DB Functions
def update_encouragements(encouraging_message):
  if "encouragements" in db.keys():
    encouragements = db["encouragements"]
    encouragements.append(encouraging_message)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [encouraging_message]

def delete_encouragement(index):
  encouragements = db["encouragements"]
  if len(encouragements) > index:
    del encouragements[index]
  db["encouragements"] = encouragements


# bot on ready func.
@client.event
async def on_ready():
    await client.change_presence(
        status=discord.Status.idle,
        activity=discord.Game(f"Watching in {len(client.guilds)} servers"),
    )
    print("bot logging in as {0.user.name}".format(client))


# bot reading chat
@client.event
async def on_message(message):
  if message.author == client.user:    
    return

  if message.content.startswith("$norris"):
    url = "https://api.chucknorris.io/jokes/random"
    res = requests.get(url)
    data = res.json()
    val = f"{data['value']}"
    await message.channel.send(val)
                       
  if message.content.startswith('$quote'):
    quote = get_quote()
    await message.channel.send(quote)

  options = starter_encouragements
  if "encouragements" in db.keys():
    options =  db["encouragements"]
    options = options

  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))


  if message.content.startswith("$new"):
    encouraging_message = message.content.split("$new ", 1)[1]
    update_encouragements(encouraging_message)
    await message.channel.send("New encouraging message added.")


  if message.content.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(message.content.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = db["encouragements"]
    await message.channel.send(f"{encouragements}")



client.run(os.getenv('TOKEN'))
