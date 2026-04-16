import discord
from flask import Flask, render_template
from flask_socketio import SocketIO
import threading

TOKEN = "YOUR_BOT_TOKEN"

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@app.route("/")
def index():
    return render_template("index.html")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author.bot and message.embeds:
        embed = message.embeds[0]

        data = {
            "sender": message.author.name,
            "title": embed.title or "",
            "description": embed.description or "",
            "fields": "\n".join(f"{f.name}: {f.value}" for f in embed.fields) if embed.fields else ""
        }

        socketio.emit("new_log", data)
        print("LOG:", data)

def run_bot():
    client.run(TOKEN)

threading.Thread(target=run_bot).start()

import os

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=port)
