"""
Accessing the chat bot using the Discord bot
Timothy Mwangi
"""
import discord
from model import prompt

class MyClient(discord.Client):
    """Class to represent the Client (bot user)"""

    def __init__(self) -> None:
        """This is the constructor. Sets the default 'intents' for the bot."""
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)

    async def on_ready(self) -> None:
        """Called when the bot is fully logged in."""
        print('Logged on as', self.user)

    async def on_message(self, message) -> None:
        """Called whenever the bot receives a message. The 'message' object
        contains all the pertinent information."""

        # don't respond to ourselves
        if message.author == self.user:
            return

        if self.user.mentioned_in(message):  # pyright: ignore[reportOptionalMemberAccess]
            utterance = { "role": "user", "content": message.content }
            await message.channel.send(prompt(utterance))

def read_file(file: str) -> str:
    """Reads txt files"""
    with open(file, 'r', encoding="utf-8") as f:
        return f.read()


## Set up and log in
def main() -> None:
    client = MyClient()
    with open("bot_token.txt") as file:
        token = file.read()

    client.run(token)

if __name__ == "__main__":
    main()