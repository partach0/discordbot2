import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.messages = True
intents.guilds = True
intents.typing = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Predefined Gmail addresses and passwords
gmail_credentials = {
    'example1@gmail.com': 'password1',
    'example2@gmail.com': 'password2',
    'example3@gmail.com': 'password3'
}

# ID of the allowed channel
allowed_channel_id = 1126883364616548352

# Cooldown duration in seconds (12 hours = 12 * 60 * 60 seconds)
cooldown_duration = 12 * 60 * 60

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
@commands.cooldown(1, cooldown_duration, commands.BucketType.user)
async def gen3(ctx):
    if ctx.channel.id != allowed_channel_id:
        return  # Do nothing if the command is used in a different channel
    
    if gmail_credentials:
        gmail_address, password = gmail_credentials.popitem()
        try:
            dm_channel = await ctx.author.create_dm()
            await dm_channel.send(f'Gmail address: {gmail_address}\nPassword: {password}')
            await ctx.send(f'Uita-te in DM pentru a obtine detaliile contului, {ctx.author.mention}!')
        except discord.Forbidden:
            await ctx.send("I don't have permission to send you direct messages.")
        except discord.HTTPException:
            await ctx.send("An error occurred while trying to send you direct messages.")
    else:
        await ctx.send('Din pacate nu mai sunt conturi in stock momentan.')

@gen3.error
async def gen_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f'Inca nu au trecut cele 12 ore. Poti genera in {error.retry_after:.0f} secunde.')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot.run('MTEyNjg4Nzc3MDg0MTk1MjI2Ng.GO6NG4.xG8hg_Km-9AQyLh5YSGTycbvpfkVGoVbNIFdQ8')