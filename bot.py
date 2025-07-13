import discord

# クライアント生成
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"We hav logged in as {client.user}")

@client.event
async def on_message(message):
    """何か受信したメッセージに対して反応するアクション"""
    #Bot自身からのメッセージには反応しない
    if message.author == client.user :
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

client.run('token')
