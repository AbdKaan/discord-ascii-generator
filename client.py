import discord
from discord import app_commands
from discord.ext import commands

from typing import Literal, Optional
from SECRET import token 


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is up!\nWe have logged in as {bot.user}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$ping'):
        await message.channel.send('pong!')

    if "best song" in message.content:
        await message.channel.send('<https://www.youtube.com/watch?v=dQw4w9WgXcQ>')
    
    if message.content == 'pog':
        await message.channel.send('<:pog:1284563646927736894>')

    await bot.process_commands(message)

@bot.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

@bot.tree.command()
@app_commands.allowed_installs(guilds=False, users=True) # users only, no guilds for install
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True) # all allowed
async def image_to_ascii(interaction: discord.Interaction, arg: str):
    await interaction.response.send_message(f"Given argument: {arg}")

bot.run(token)