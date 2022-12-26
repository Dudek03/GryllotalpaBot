import os
from dotenv import load_dotenv
import discord

load_dotenv()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')


def main():
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)

    client.run(os.getenv('DISCORD_TOKEN'))


if __name__ == "__main__":
    main()
